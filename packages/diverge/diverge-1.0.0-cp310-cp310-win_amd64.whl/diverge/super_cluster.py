from Bio import Phylo,AlignIO
import pandas as pd
import numpy as np
import os
import itertools
from tqdm import tqdm
from Bio.Phylo.TreeConstruction import DistanceCalculator
from Bio.Phylo.TreeConstruction import DistanceMatrix
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor
from .utils import create_temp_folder,write_temp_tree,remove_temp_folder
from .binding import Gu99
import shutil
import atexit
calculator = DistanceCalculator('identity')
constructor = DistanceTreeConstructor()
temp_folder = create_temp_folder()
def aln_read(aln_file):
  try:
    aln = AlignIO.read(aln_file, 'clustal')
  except ValueError:
    aln = AlignIO.read(aln_file, 'fasta')
  return aln

def tree_construct(aln):
  dm = calculator.get_distance(aln)
  tree = constructor.nj(dm)
  return dm,tree

def sub_dm(dm,c_list):
  clades_name = pd.Index(dm.names)[np.where(c_list)].to_list()
  sub_dm = DistanceMatrix(clades_name)
  for clade_name1,clade_name2 in itertools.combinations(clades_name,2):
    sub_dm[clade_name1,clade_name2] = dm[clade_name1,clade_name2]
  return sub_dm

def get_group_list(group_num):
  n = group_num
  nums = list(range(1, n + 1))
  num_range = range(1, n//2+1)
  group_list = []
  for num in num_range:
    combos = itertools.combinations(nums, num)
    for combo in combos:
        group1 = list(combo)
        group2 = list(set(nums) - set(combo))
        if([group2,group1] in group_list):
          continue
        else:
          group_list.extend([[group1, group2]])
  return group_list

def sep_cluster(tree_cluster,cluster_num):
  group_list = get_group_list(cluster_num)
  cluster_list = []
  for group in group_list:
    cluster = np.zeros(len(tree_cluster))
    group1,gourp2 = group[0],group[1]
    cluster[np.isin(tree_cluster,group1)] = 1
    cluster[np.isin(tree_cluster,gourp2)] = 2
    cluster_list.extend([cluster])
  return cluster_list,group_list

def tree_reconstruct(dm,cluster):
  cluster1_list = np.isin(cluster,1)
  cluster2_list = np.isin(cluster,2)
  sub_dm1 = sub_dm(dm,cluster1_list)
  sub_dm2 = sub_dm(dm,cluster2_list)
  tree1 = constructor.nj(sub_dm1)
  tree2 = constructor.nj(sub_dm2)
  return tree1,tree2

def get_cluster(aln_file,*tree_files):
  try:
    aln = AlignIO.read(aln_file,'clustal')
  except ValueError:
    aln = AlignIO.read(aln_file,'fasta')
  dm,tree = tree_construct(aln)
  tree_cluster = [0]*len(dm.names)
  i = 1
  tree_dict = {}
  for tree_file in tree_files:
    tree = Phylo.read(tree_file,'newick')
    tree_id = os.path.basename(tree_file).split('.')[0]
    tree_dict[i] = tree_id
    tree_terminal = [i.name for i in tree.get_terminals()]
    t_list = [dm.names.index(j) for j in tree_terminal]
    for k in t_list: 
      tree_cluster[k] = i
    i +=1
  return tree_cluster,i-1,tree_dict

def re_clean_tree(tree):
  for clade in tree.get_nonterminals():
    clade.name = None
  # return tree.root_at_midpoint()
  return tree

def get_super_cluster_list(aln_file,*tree_files):
  tree_cluster,cluster_num,tree_dict = get_cluster(aln_file,*tree_files)
  cluster_list,group_list = sep_cluster(tree_cluster,cluster_num)
  aln = aln_read(aln_file)
  dm,_ = tree_construct(aln)
  super_cluster_list = []
  for cluster in cluster_list:
    tree1,tree2 = tree_reconstruct(dm,cluster)
    tree1 = re_clean_tree(tree1)
    tree2 = re_clean_tree(tree2)
    super_cluster_list.extend([[tree1,tree2]])
  return super_cluster_list,group_list,tree_dict

def write_tree_file(super_cluster_list):
  tree_path_list = []
  for i in range(len(super_cluster_list)):
    tree1,tree2 = super_cluster_list[i][0],super_cluster_list[i][1]
    tree1_path = write_temp_tree(tree1,temp_folder,'cluster1',str(i))
    tree2_path = write_temp_tree(tree2,temp_folder,'cluster2',str(i))
    tree_path_list.extend([[tree1_path,tree2_path]])
  
  return tree_path_list

# def get_super_cluster_pp2(aln_file,*tree_files):
#   """
#   Make a composite Q-site plotting: each site has M number of Q values, denoted by Q1,…, QM.
#   Let Qmax=max(Q1,…, QM), which is used to represent in the composite Q-site plotting.
#   """
#   super_cluster_list = get_super_cluster_list(aln_file,*tree_files)
#   tree_path_list = write_tree_file(super_cluster_list)
#   results_list = []
#   for tree_path in tree_path_list:
#     tree1_path = tree_path[0]
#     tree2_path = tree_path[1]
#     gu2001 = Gu2001(aln_file,tree1_path,tree2_path)
#     results = gu2001.results().iloc[:,0]
#     results_list.extend([[results]])
#   results_array = np.reshape(np.array(results_list),(3, -1))
#   return results_array,super_cluster_list

import numpy as np
from concurrent.futures import ThreadPoolExecutor

def get_super_cluster_pp(aln_file, *tree_files):
    """
    Make a composite Q-site plotting: each site has M number of Q values, denoted by Q1,…, QM.
    Let Qmax=max(Q1,…, QM), which is used to represent in the composite Q-site plotting.
    """
    super_cluster_list,group_list,tree_dict = get_super_cluster_list(aln_file, *tree_files)
    tree_path = write_tree_file(super_cluster_list)
    results_list = []
    position_list = []
    param_list = []
    def process_tree_path(tree1_path, tree2_path):
        gu99 = Gu99(aln_file, tree1_path, tree2_path)
        summary = gu99.summary()
        position = gu99.results().index.values.tolist()
        #test by gu99
        z_score = summary.loc["MFE z score",:].values
        se = summary.loc["MFE se",:].values
        theta = summary.loc["MFE Theta",:].values
        results = gu99.results().values.tolist()
        param = [theta,se,z_score]
        return results,position,param
        # if abs(z_score) > 1.96:
        #   return results,position
        # else:
        #   return [[0]]*len(results),position

    # with ThreadPoolExecutor() as executor:
    #     for result in executor.map(process_tree_path, [t[0] for t in tree_path], [t[1] for t in tree_path]):
    #         results_list.extend([result])
    # results_array = np.reshape(np.array(results_list), (len(super_cluster_list), -1))
    # return results_array, super_cluster_list ,group_list , tree_dict
    
    #add progress bar
    with ThreadPoolExecutor() as executor:
      progress_bar = tqdm(total=len(tree_path), desc="Processing super cluster groups", unit="groups")
      futures = [executor.submit(process_tree_path, t[0], t[1]) for t in tree_path]
      for future in futures:
          results_list.extend([future.result()[0]])
          param_list.extend([future.result()[2]])
          if position_list == []:
            position_list = future.result()[1]
          else:
            pass
          
          progress_bar.update(1)

    results_array = np.reshape(np.array(results_list), (len(super_cluster_list), -1))
    # try:
    #   # remove temp folder
    #   # shutil.rmtree(temp_folder.name)
    #   temp_folder.cleanup()
    #   print("temp folder cleaned")
    # except Exception as e:
    #   print(e,"temp folder can't cleaned")
    return results_array, super_cluster_list, group_list, tree_dict,position_list,param_list

def super_cluster(aln_file,*tree_files):
  pp_list,tree_list,group_list,tree_dict,position_list,param_list = get_super_cluster_pp(aln_file,*tree_files)
  max_group = np.argmax(np.bincount(np.argmax(pp_list,axis=0)))
  trees = tree_list[max_group]
  group = group_list[max_group]
  group1 = [tree_dict[i] for i in group[0]]
  group2 = [tree_dict[i] for i in group[1]]
  return trees,group1,group2,pp_list

class SuperCluster():
    def __init__(self, aln_file, *tree_files):
        self.pp_list, self.tree_list, self.group_list, self.tree_dict , self.position_list,self.param_list = get_super_cluster_pp(aln_file, *tree_files)
    # def get_trees(self):
    #     max_group = np.argmax(np.bincount(np.argmax(self.pp_list, axis=0)))
    #     return self.tree_list[max_group]

    # def get_groups(self):   
    #     max_group = np.argmax(np.bincount(np.argmax(self.pp_list, axis=0)))
    #     group = self.group_list[max_group]
    #     group1 = [self.tree_dict[i] for i in group[0]]
    #     group2 = [self.tree_dict[i] for i in group[1]]
    #     return group1, group2

    def get_pp_list(self):
        return self.pp_list
      
    def get_group_list(self):
        return self.group_list
    
    def get_position_list(self):
        return self.position_list
    
    def get_summary(self):
        col_name = [f"{i}" for i in self.group_list]
        summary_df = pd.DataFrame(index=["θ±SE","z_score","Qk>0.5","Qk>0.67","Qk>0.9"],columns=col_name)
        for i in range(len(self.group_list)):
          summary_df.iloc[0,i] = f"{round(self.param_list[i][0][0],2)}±{round(self.param_list[i][1][0],2)}"
          summary_df.iloc[1,i] = round(self.param_list[i][2][0],2)
          summary_df.iloc[2,i] = sum(self.pp_list[i,:]>0.5)
          summary_df.iloc[3,i] = sum(self.pp_list[i,:]>0.67)
          summary_df.iloc[4,i] = sum(self.pp_list[i,:]>0.9)
        return summary_df




import psutil 
def cleanup():
  dirname = temp_folder.name
  if os.path.exists(dirname):
      for proc in psutil.process_iter():
          try:
              for path in proc.open_files():
                  if dirname in path.path:
                      proc.kill()
          except Exception as e:
              print(f"Failed to kill process: {e}")
      try:
          shutil.rmtree(dirname)
      except OSError as e:
          print(f"Failed to delete directory: {e}")

atexit.register(cleanup)