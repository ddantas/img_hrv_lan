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
import re

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

## \brief Converts routine to elan annotation file
#
#  Converts routine text to annotation in TSV format to be imported by ELAN software.
#  The annotation is defined by routine label command.
#
#  @param self The object pointer.
#  @param routine_filename Name of routine file
#  @param output_path Folder where elan_import.txt wil be saved.
def routine_to_tsv(routine_filename, output_path, duration):
    
    try:
        with open(routine_filename) as f:
            routine_lines = f.readlines()
    except:
        tk.messagebox.showerror(title="Error in routine_to_tsv", message="Unable to open routine file %s" % routine_filename)
        return

    arr_label_time = []
    arr_label_str = []
    arr_slide_time = []
    arr_slide_str = []
    max_time = 0.0
    for l in routine_lines:
        if l[0] == "#":
            continue

        cols = l.split(";")
        for i in range(len(cols)):
            cols[i] = cols[i].strip("\n ")

        t = float(cols[0])
        if len(arr_label_time) and t > arr_label_time[-1]:
            max_time = t

        if ("images/slides/Slide" in cols[3]):
            slide = re.search("\d+", cols[3])
            slide = slide[0]
            arr_label_time.append(t)
            arr_label_str.append("slide")
            #arr_slide_time.append(t)
            arr_slide_str.append(slide)

        if ("pause" in cols[3]):
            label = "pause"
            arr_label_time.append(t)
            arr_label_str.append(label)
            #arr_slide_time.append(t)
            arr_slide_str.append(label)

    arr_label_time.append(max_time)
    #arr_slide_time.append(max_time)

    output_filename = os.path.join(output_path, k.FILENAME_SLIDE)
    try:
        of = open(output_filename, "w")
    except:
        tk.messagebox.showerror(title="Error in routine_to_tsv", message="Unable to open output file %s" % (output_filename))
        return

    of.write("time\tblock\tslide\n")

    print(arr_label_time)
    print(arr_label_str)
    print(arr_slide_str)
    j = 0
    for i in range(int(duration) + 1):
      if (i == arr_label_time[j+1] and i < max_time):
        j = j + 1
      of.write("%d\t%s\t%s\n" % (i, arr_label_str[j], arr_slide_str[j]))
    of.close()


def create_data_file(input_path,
       filename_rr_linear1, filename_rr_linear2,
       filename_rr_nearest1, filename_rr_nearest2,
       filename_ecg_rr_linear1, filename_ecg_rr_linear2,
       filename_ecg_rr_nearest1, filename_ecg_rr_nearest2,
       filename_slides, filename_dataset, duration):
  
  print("Dataset filename: " + filename_dataset)
  print("Slides filename: " + filename_slides)

  data_slides = pd.read_csv(filename_slides, sep="\t")
  block = data_slides.block
  slide = data_slides.slide

  data_hr1_linear = Data.Data.load_raw_data(filename_rr_linear1)
  data_hr2_linear = Data.Data.load_raw_data(filename_rr_linear2)
  hr1_linear = data_hr1_linear.heart_rate
  rr1_linear = data_hr1_linear.rr_interval
  hr2_linear = data_hr2_linear.heart_rate
  rr2_linear = data_hr2_linear.rr_interval

  data_hr1_nearest = Data.Data.load_raw_data(filename_rr_nearest1)
  data_hr2_nearest = Data.Data.load_raw_data(filename_rr_nearest2)
  hr1_nearest = data_hr1_nearest.heart_rate
  rr1_nearest = data_hr1_nearest.rr_interval
  hr2_nearest = data_hr2_nearest.heart_rate
  rr2_nearest = data_hr2_nearest.rr_interval

  data_hr1_ecg_linear = Data.Data.load_raw_data(filename_ecg_rr_linear1)
  data_hr2_ecg_linear = Data.Data.load_raw_data(filename_ecg_rr_linear2)
  hr1_ecg_linear = data_hr1_ecg_linear.heart_rate
  rr1_ecg_linear = data_hr1_ecg_linear.rr_interval
  hr2_ecg_linear = data_hr2_ecg_linear.heart_rate
  rr2_ecg_linear = data_hr2_ecg_linear.rr_interval

  data_hr1_ecg_nearest = Data.Data.load_raw_data(filename_ecg_rr_nearest1)
  data_hr2_ecg_nearest = Data.Data.load_raw_data(filename_ecg_rr_nearest2)
  hr1_ecg_nearest = data_hr1_ecg_nearest.heart_rate
  rr1_ecg_nearest = data_hr1_ecg_nearest.rr_interval
  hr2_ecg_nearest = data_hr2_ecg_nearest.heart_rate
  rr2_ecg_nearest = data_hr2_ecg_nearest.rr_interval

  time = []
  annotator = []
  content = {}
  for i in range(int(duration) + 1):
    time.append(i)

  folder = os.path.basename(os.path.normpath(input_path))

  content['time'] = time
  content['block'] = block
  content['slide'] = slide
  content['folder'] = [folder for i in range(len(content['time']))]

  content['hr_subj1_linear'] = hr1_linear
  content['hr_subj2_linear'] = hr2_linear
  content['hr_subj1_nearest'] = hr1_nearest
  content['hr_subj2_nearest'] = hr2_nearest

  content['hr_subj1_ecg_linear'] = hr1_ecg_linear
  content['hr_subj2_ecg_linear'] = hr2_ecg_linear
  content['hr_subj1_ecg_nearest'] = hr1_ecg_nearest
  content['hr_subj2_ecg_nearest'] = hr2_ecg_nearest

  content['rr_subj1_linear'] = rr1_linear
  content['rr_subj2_linear'] = rr2_linear
  content['rr_subj1_nearest'] = rr1_nearest
  content['rr_subj2_nearest'] = rr2_nearest

  content['rr_subj1_ecg_linear'] = rr1_ecg_linear
  content['rr_subj2_ecg_linear'] = rr2_ecg_linear
  content['rr_subj1_ecg_nearest'] = rr1_ecg_nearest
  content['rr_subj2_ecg_nearest'] = rr2_ecg_nearest

  dfs = []

  for h in k.DATASET_HEADERS:
    print(h)
    if (h == "msg1" or h == "msg2"):
      for i in range(len(content[h])):
        content[h][i] = content[h][i].replace('"', '')
    dfs.append(pd.Series(content[h], name=h))

  df = pd.concat(dfs, axis=1)
  
  df.to_csv(filename_dataset, sep = '\t', index=False, mode = "w", header = True)

def write_to_dataset(input_path, path_prep, filename_dataset):

  filename_routine = os.path.join(input_path, k.FILENAME_ROUTINE)
  filename_start_time = os.path.join(input_path, k.FILENAME_START_TIME)
  t0 = utils.get_time_start(filename_start_time)
  duration = utils.get_duration_ideal(filename_routine)

  routine_to_tsv(filename_routine, path_prep, duration)

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

  ## Linear and NN interpolation
  rr_interpolation.interpolate(filename_rr1, filename_rr_nearest1, filename_rr_linear1, t0, duration)
  rr_interpolation.interpolate(filename_rr2, filename_rr_nearest2, filename_rr_linear2, t0, duration)

  rr_interpolation.interpolate(filename_ecg_rr1, filename_ecg_rr_nearest1, filename_ecg_rr_linear1, t0, duration)
  rr_interpolation.interpolate(filename_ecg_rr2, filename_ecg_rr_nearest2, filename_ecg_rr_linear2, t0, duration)

  # subj%d_rr_inferred_from_ecg.tsv
  filename_slides = os.path.join(path_prep, k.FILENAME_SLIDE)

  ## Generate dataset.tsv
  print("Generating complete dataset...")
  create_data_file(input_path,
       filename_rr_linear1, filename_rr_linear2,
       filename_rr_nearest1, filename_rr_nearest2,
       filename_ecg_rr_linear1, filename_ecg_rr_linear2,
       filename_ecg_rr_nearest1, filename_ecg_rr_nearest2,
       filename_slides, filename_dataset, duration)
  print("Done.")

"""#########################################################
############################################################
### Main function                                        ###
############################################################
#########################################################"""

def main(dir_list):

  for d in dir_list:
    input_path = d

    path_prep = os.path.join(input_path, k.FOLDER_PREP)
    if not os.path.exists(path_prep):
      os.mkdir(path_prep)

    files = os.listdir(input_path)
    filename_ds = "dataset.tsv"
    filename_dataset = os.path.join(d, k.FOLDER_PREP, filename_ds)
    print(filename_dataset)
    write_to_dataset(input_path, path_prep, filename_dataset)

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

  main(dir_list)
