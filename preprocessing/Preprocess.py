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
    # print(root.text, root.tag, root.attrib)
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

def create_file_from_dict(file):

  tiers_dict, time_end = construct_dict_from_eaf(file)
  with open('teste.tsv', 'w') as f:

    print('sec\t', end='', file=f)
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
      for tier in tiers_dict.keys():
        print(content[tier] + '\t', end='', file=f)
      print('\n', end='', file=f)

"""#########################################################
############################################################
### Main function                                        ###
############################################################
#########################################################"""

def main(input_path):
  pass


if __name__ == "__main__":
  input_path = "../data/a003"
  #main(input_path)
  elan_filename = os.path.join(input_path, "annotation.eaf")
  tree = et.parse(elan_filename)
  create_file_from_dict('annotation.eaf')
  #root = tree.getroot()
  #for child in root:
  #  print(child.tag, child.attrib)  
