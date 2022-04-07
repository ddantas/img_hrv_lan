#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""#########################################################
############################################################
### Preprocess Polar H10 and annotation data.            ###
###                                                      ###
### Author: Daniel Dantas                                ###
### Last edited: Fev 2022                                ###
############################################################
#########################################################"""

import os
import xml.etree.ElementTree as et
from queue import Queue
import sys
import pandas as pd

import rr_interpolation
import rr_inference

# Import module from parent folder
filepath = os.path.dirname(__file__)
modpathrel = os.path.join(filepath, "..")
modpathabs = os.path.abspath(modpathrel)
sys.path.append(modpathabs)

import Data
import const as k
import utils

def print_tree_level(level, root):
  space = ""
  for i in range(level):
    space = space + "  .  "
    
  for child in root:
    text = child.text
    if isinstance(text, str):
      text = text.strip(" \n")
    else:
      text = ""
    if text != "":
      text = "<<" + text + ">>"
      
    print(space, child.tag, child.attrib, text)
    print_tree_level(level + 1, child)
    
def print_tree(tree):
  root = tree.getroot()
  level = 0
  print_tree_level(level, root)

def construct_dict_from_eaf(eaf_file):

  tree = et.parse(eaf_file)

  root = tree.getroot()

  q = []
  q.append(root)
  tiers_dict = {}
  time_slots_dict = {}
  while len(q) > 0:

    root = q.pop()
    first_time = 0

    if root.tag == 'TIER':
      cur_tier = root.attrib['TIER_ID'].strip()
      tiers_dict[cur_tier] = {}

    for child in root:

      if child.tag == 'TIME_SLOT':
        time_slots_dict[child.attrib['TIME_SLOT_ID']] = child.attrib['TIME_VALUE']

      elif child.tag == 'ALIGNABLE_ANNOTATION':

        for c in child:
          value = c.text

        tiers_dict[cur_tier][child.attrib['ANNOTATION_ID']] = {'TIME_SLOT_BEGIN': child.attrib['TIME_SLOT_REF1'], \
                                                                    'TIME_SLOT_END': child.attrib['TIME_SLOT_REF2'], \
                                                                    'ANNOTATION_VALUE': value}

      q.append(child)

  for tier, tier_dict in tiers_dict.items():
    for annot_id in tier_dict.keys():
      annot_dict = tiers_dict[tier][annot_id]
      begin_ts_id = annot_dict['TIME_SLOT_BEGIN']
      end_ts_id = annot_dict['TIME_SLOT_END']
      annot_dict['TIME_SLOT_BEGIN'] = time_slots_dict[begin_ts_id]
      annot_dict['TIME_SLOT_END'] = time_slots_dict[end_ts_id]

  time_end = max(time_slots_dict.values())
  time_end = int(time_end)//1000+1

  return tiers_dict, time_end


def create_data_file(input_path,
       filename_rr_linear1, filename_rr_linear2,
       filename_rr_nearest1, filename_rr_nearest2,
       filename_ecg_rr_linear1, filename_ecg_rr_linear2,
       filename_ecg_rr_nearest1, filename_ecg_rr_nearest2,
       filename_annot, filename_dataset):

  data_hr1_linear = Data.Data.load_raw_data(filename_rr_linear1)
  data_hr2_linear = Data.Data.load_raw_data(filename_rr_linear2)
  hr1_linear = data_hr1_linear.heart_rate
  hr2_linear = data_hr2_linear.heart_rate

  data_hr1_nearest = Data.Data.load_raw_data(filename_rr_nearest1)
  data_hr2_nearest = Data.Data.load_raw_data(filename_rr_nearest2)
  hr1_nearest = data_hr1_nearest.heart_rate
  hr2_nearest = data_hr2_nearest.heart_rate

  data_hr1_ecg_linear = Data.Data.load_raw_data(filename_ecg_rr_linear1)
  data_hr2_ecg_linear = Data.Data.load_raw_data(filename_ecg_rr_linear2)
  hr1_ecg_linear = data_hr1_ecg_linear.heart_rate
  hr2_ecg_linear = data_hr2_ecg_linear.heart_rate

  data_hr1_ecg_nearest = Data.Data.load_raw_data(filename_ecg_rr_nearest1)
  data_hr2_ecg_nearest = Data.Data.load_raw_data(filename_ecg_rr_nearest2)
  hr1_ecg_nearest = data_hr1_ecg_nearest.heart_rate
  hr2_ecg_nearest = data_hr2_ecg_nearest.heart_rate

  tiers_dict, time_end = construct_dict_from_eaf(filename_annot)

  time = []
  content = {}
  for i in range(time_end):
    time.append(i)

    for tier in tiers_dict.keys():

      v = ''
      for annot_id, annot_dict in tiers_dict[tier].items():

        begin_ts = annot_dict['TIME_SLOT_BEGIN']
        end_ts = annot_dict['TIME_SLOT_END']
        value = annot_dict['ANNOTATION_VALUE']

        if i >= int(begin_ts)//1000 and i <= int(end_ts)//1000:
          v = value
          break
        else:
          v = ''
      try :
        content[tier].append(v)
      except:
        content[tier] = [v]

  folder = os.path.basename(os.path.normpath(input_path))

  content['time'] = time
  content['folder'] = [folder for i in range(len(content['time']))]
  content['hr_subj1_linear'] = hr1_linear
  content['hr_subj2_linear'] = hr2_linear

  content['hr_subj1_nearest'] = hr1_nearest
  content['hr_subj2_nearest'] = hr2_nearest

  content['hr_subj1_ecg_linear'] = hr1_ecg_linear
  content['hr_subj2_ecg_linear'] = hr2_ecg_linear

  content['hr_subj1_ecg_nearest'] = hr1_ecg_nearest
  content['hr_subj2_ecg_nearest'] = hr2_ecg_nearest

  dfs = []
  for key in tiers_dict.keys():
    content[key] = [val.strip() for val in content[key]]

  for h in k.DATASET_HEADERS:
    print(h)
    dfs.append(pd.Series(content[h], name=h))

  df = pd.concat(dfs, axis=1)
  
  df.to_csv(filename_dataset, sep = '\t', index=False, mode = "a", header = False)

"""#########################################################
############################################################
### Main function                                        ###
############################################################
#########################################################"""

def write_to_dataset(input_path, path_prep, filename_dataset, filename_annot):

  filename_routine = os.path.join(input_path, k.FILENAME_ROUTINE)
  t0 = utils.get_time_start(filename_routine)
  duration = utils.get_duration_ideal(filename_routine)

  ## interpolate
  # subj%d_rr.tsv
  filename_rr1 = os.path.join(input_path, k.FILENAME_RR_S1)
  filename_rr2 = os.path.join(input_path, k.FILENAME_RR_S2)

  # subj%d_rr_inferred_from_ecg.tsv
  filename_ecg1 = os.path.join(input_path, k.FILENAME_ECG_S1)
  filename_ecg2 = os.path.join(input_path, k.FILENAME_ECG_S2)

  # subj%d_rr_inferred_from_ecg.tsv
  filename_ecg_rr1 = os.path.join(path_prep, k.FILENAME_ECG_RR_S1)
  filename_ecg_rr2 = os.path.join(path_prep, k.FILENAME_ECG_RR_S2)

  print("Input files:")
  print(filename_rr1)
  print(filename_rr2)
  print(filename_ecg1)
  print(filename_ecg2)

  print("Output files:")
  print(filename_ecg_rr1)
  print(filename_ecg_rr2)

  ## Infer RR intervals from ECG
  print("Inferring intervals from ECG...")
  rr_inference.infer_rr_intervals_from_ecg(filename_ecg1, filename_ecg_rr1)
  rr_inference.infer_rr_intervals_from_ecg(filename_ecg2, filename_ecg_rr2)
  print("Done.")

  ## Generate filenames
  # subj%d_ecg.tsv
  filename_ecg1 = os.path.join(input_path, k.FILENAME_ECG_S1)
  filename_ecg2 = os.path.join(input_path, k.FILENAME_ECG_S2)
  # 02_preprocess/subj%d_rr_linear.tsv
  filename_rr_linear1 = os.path.join(path_prep, k.FILENAME_RR_LIN_S1)
  filename_rr_linear2 = os.path.join(path_prep, k.FILENAME_RR_LIN_S2)
  # 02_preprocess/subj%d_rr_nearest.tsv
  filename_rr_nearest1 = os.path.join(path_prep, k.FILENAME_RR_NN_S1)
  filename_rr_nearest2 = os.path.join(path_prep, k.FILENAME_RR_NN_S2)
  # 02_preprocess/subj%d_ecg_inferred_rr_linear.tsv
  filename_ecg_rr_linear1 = os.path.join(path_prep, k.FILENAME_ECG_RR_LIN_S1)
  filename_ecg_rr_linear2 = os.path.join(path_prep, k.FILENAME_ECG_RR_LIN_S2)
  # 02_preprocess/subj%d_ecg_inferred_rr_nearest.tsv
  filename_ecg_rr_nearest1 = os.path.join(path_prep, k.FILENAME_ECG_RR_NN_S1)
  filename_ecg_rr_nearest2 = os.path.join(path_prep, k.FILENAME_ECG_RR_NN_S2)
  # annotation.eaf
  filename_annot = os.path.join(input_path, filename_annot)

  ## Linear and NN interpolation
  rr_interpolation.interpolate(filename_rr1, filename_rr_nearest1, filename_rr_linear1, t0, duration)
  rr_interpolation.interpolate(filename_rr2, filename_rr_nearest2, filename_rr_linear2, t0, duration)

  rr_interpolation.interpolate(filename_ecg_rr1, filename_ecg_rr_nearest1, filename_ecg_rr_linear1, t0, duration)
  rr_interpolation.interpolate(filename_ecg_rr2, filename_ecg_rr_nearest2, filename_ecg_rr_linear2, t0, duration)

  ## Generate dataset.tsv
  print("Generating complete dataset...")
  create_data_file(input_path,
       filename_rr_linear1, filename_rr_linear2,
       filename_rr_nearest1, filename_rr_nearest2,
       filename_ecg_rr_linear1, filename_ecg_rr_linear2,
       filename_ecg_rr_nearest1, filename_ecg_rr_nearest2,
       filename_annot, filename_dataset)
  print("Done.")

def main(dir_list, filename_dataset, filename_annot):

  # create empty dataframe file for appending
  df = pd.DataFrame(columns=k.DATASET_HEADERS)
  df.to_csv(filename_dataset, sep = '\t', index=False, mode = "w", header = True)

  for d in dir_list:
    input_path = d

    path_prep = os.path.join(input_path, k.FOLDER_PREP)
    if not os.path.exists(path_prep):
      os.mkdir(path_prep)

    write_to_dataset(input_path, path_prep, filename_dataset, filename_annot)

if __name__ == "__main__":

  # data/output
  print(sys.argv)
  if len(sys.argv) < 2:
    print(f"Usage: python3 preprocess.py <dir(s)_to_preprocess>") 
    exit(1)

  dir_list = sys.argv[1:]

  path_dataset = os.path.join(k.FOLDER_DATA, k.FOLDER_OUTPUT)
  if not os.path.exists(path_dataset):
    os.mkdir(path_dataset)

  # data/output/dataset.tsv
  filename_dataset = os.path.join(path_dataset, k.FILENAME_DATASET)

  main(dir_list, filename_dataset, k.FILENAME_ANNOTATION)
