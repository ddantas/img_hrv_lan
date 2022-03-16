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


def create_data_file(ecg_files, hr_files, eaf_file, output_file):

  tiers_dict, time_end = construct_dict_from_eaf(eaf_file)
  hr1 = get_hr_from_file(hr_files[0])
  hr2 = get_hr_from_file(hr_files[1])

  ecg_tuple1 = get_ecg_tuple(ecg_files[0])
  ecg_tuple2 = get_ecg_tuple(ecg_files[1])

  ecg_hr1 = ecg_tuple1[-1]
  ecg_hr2 = ecg_tuple2[-1]

  with open(output_file, 'w') as f:

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

def main(input_path, ecg_files, interp_rr_files, annotation_file, output_file):

  ecg_files = [os.path.join(input_path, file) if input_path not in file else file for file in ecg_files]
  interp_rr_files = [os.path.join(input_path, file) if input_path not in file else file for file in interp_rr_files]
  annotation_file = os.path.join(input_path, annotation_file) if input_path not in annotation_file else annotation_file

  create_data_file(ecg_files, interp_rr_files, annotation_file, output_file)

if __name__ == "__main__":

  input_path = sys.argv[1]
  ecg_files = [f for f in sys.argv[2:] if 'ecg' in f]
  interp_rr_files = [f for f in sys.argv[len(ecg_files)+2:-2]]
  annotation_file = sys.argv[-2]
  output_file = sys.argv[-1]

  main(input_path, ecg_files, interp_rr_files, annotation_file, output_file)
