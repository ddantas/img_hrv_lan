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

def create_file_from_template(video1, video2, template_file, time_values):

  xml_file = et.parse(template_file)

  root = xml_file.getroot()
  q = []
  q.append(root)
  annotations_dict = {}
  while len(q) > 0:

    # print(q, q.pop())
    root = q.pop()
    # print(root.text, root.tag, root.attrib)
    first_time = 0
    for child in root:

      if child.tag == 'TIME_SLOT':
        # do something
        pass
      elif child.tag == 'ALIGNABLE_ANNOTATION':
        print(child.attrib, child.text)

      q.append(child)

def annotate_from_routine_file(routine_file):
  pass

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
  # print_tree(tree)
  # create_file_from_template('../data/a003/subj1.mp4', '', './default.eaf', [])
  create_file_from_template('../data/a003/subj1.mp4', '', '../data/a003/annotation.eaf', [])
  #root = tree.getroot()
  #for child in root:
  #  print(child.tag, child.attrib)  
