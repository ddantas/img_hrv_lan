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
from utils import get_ecg_tuple, get_hr_from_file
import sys

import rr_interpolation

# Import module from parent folder
filepath = os.path.dirname(__file__)
modpathrel = os.path.join(filepath, "..")
modpathabs = os.path.abspath(modpathrel)
sys.path.append(modpathabs)
import const as k

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

    for child in root:

      if root.tag == 'TIER':
        cur_tier = root.attrib['TIER_ID'].strip()
        tiers_dict[cur_tier] = {}

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
       filename_ecg1, filename_ecg2,
       filename_rr_linear1, filename_rr_linear2,
       filename_annot, filename_dataset):

  ecg_tuple1 = get_ecg_tuple(filename_ecg1)
  ecg_tuple2 = get_ecg_tuple(filename_ecg2)
  ecg_hr1 = ecg_tuple1[-1]
  ecg_hr2 = ecg_tuple2[-1]

  hr1 = get_hr_from_file(filename_rr_linear1)
  hr2 = get_hr_from_file(filename_rr_linear2)

  tiers_dict, time_end = construct_dict_from_eaf(filename_annot)

  with open(filename_dataset, 'w') as f:

    print('sec\t', end='', file=f)
    print('hr_subj1' + '\t', end='', file=f)
    print('hr_subj2' + '\t', end='', file=f)
    print('hr_subj1_ecg' + '\t', end='', file=f)
    print('hr_subj2_ecg' + '\t', end='', file=f)
    for tier in tiers_dict.keys():
      print(tier + '\t', end='', file=f)

    print('\n', end='', file=f)

    for i in range(time_end):

      content = {}

      for tier in tiers_dict.keys():

        for annot_id, annot_dict in tiers_dict[tier].items():

          begin_ts = annot_dict['TIME_SLOT_BEGIN']
          end_ts = annot_dict['TIME_SLOT_END']
          value = annot_dict['ANNOTATION_VALUE']

          if i >= int(begin_ts)//1000 and i <= int(end_ts)//1000:
            v = value
            break
          else:
            v = ''

        content[tier] = v

      print(str(i) + '\t', end='', file=f)

      try:
        print(hr1[i] + '\t', end='', file=f)
      except:
        print('hr1 not long enough')
        print('\t', end='', file=f)
      try:
        print(hr2[i] + '\t', end='', file=f)
      except:
        print('hr2 not long enough')
        print('\t', end='', file=f)

      print(str(ecg_hr1[i]) + '\t', end='', file=f)
      print(str(ecg_hr2[i]) + '\t', end='', file=f)
      
      for tier in tiers_dict.keys():
        print(content[tier] + '\t', end='', file=f)


      print('\n', end='', file=f)


"""#########################################################
############################################################
### Main function                                        ###
############################################################
#########################################################"""

def main(input_path,
       filename_ecg1, filename_ecg2,
       filename_rr_linear1, filename_rr_linear2,
       filename_annot, filename_dataset):

  folder_prep = os.path.join(input_path, k.FOLDER_PREP)
  if not os.path.exists(folder_prep):
    os.mkdir(folder_prep)

  #ecg_files = [os.path.join(input_path, file) if input_path not in file else file for file in ecg_files]
  #interp_rr_files = [os.path.join(input_path, file) if input_path not in file else file for file in interp_rr_files]
  #annotation_file = os.path.join(input_path, annotation_file) if input_path not in annotation_file else annotation_file

  create_data_file(input_path,
       filename_ecg1, filename_ecg2,
       filename_rr_linear1, filename_rr_linear2,
       filename_annot, filename_dataset)

if __name__ == "__main__":

  if (len(sys.argv)) < 3:
    print("Usage: preprocess.py <input_path> <annotation_file>")
    sys.exit()

  input_path = sys.argv[1]
  filename_annot = sys.argv[2]

  ## interpolate
  #subj1_rr.tsv
  filename_rr1 = os.path.join(input_path, k.FILENAME_RR_S1)
  #subj2_rr.tsv
  filename_rr2 = os.path.join(input_path, k.FILENAME_RR_S2)

  print(filename_rr1)
  print(filename_rr2)

  rr_interpolation.interpolate(filename_rr1)
  rr_interpolation.interpolate(filename_rr2)

  ## generate dataset.tsv
  #subj1_ecg.tsv
  filename_ecg1 = os.path.join(input_path, k.FILENAME_ECG_S1)
  #subj2_ecg.tsv
  filename_ecg2 = os.path.join(input_path, k.FILENAME_ECG_S2)
  #processed/subj1_rr_linear.tsv
  filename_rr_linear1 = os.path.join(input_path, k.FOLDER_PREP, "subj1_rr_linear.tsv")
  #processed/subj2_rr_linear.tsv
  filename_rr_linear2 = os.path.join(input_path, k.FOLDER_PREP, "subj2_rr_linear.tsv")
  #annotation.eaf
  filename_annot = os.path.join(input_path, filename_annot)
  #dataset.tsv
  filename_dataset = os.path.join(input_path, k.FOLDER_PREP, k.FILENAME_DATASET)

  main(input_path,
       filename_ecg1, filename_ecg2,
       filename_rr_linear1, filename_rr_linear2,
       filename_annot, filename_dataset)
