#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""#########################################################
############################################################
### Generate statistics about Polar H10 data.            ###
###                                                      ###
### Author: Daniel Dantas                                ###
### Last edited: Apr 2022                                ###
############################################################
#########################################################"""

import os
import sys

# Import module from parent folder
filepath = os.path.dirname(__file__)
modpathrel = os.path.join(filepath, "..")
modpathabs = os.path.abspath(modpathrel)
sys.path.append(modpathabs)

import Data
import const as k
#import utils

## \brief Weighted average of given list.
#
# Find arithmetic average of data in a list weighted by a second list.
def avg_weighted_list(l, w):
  total = 0.0
  for i in range(len(w)):
    total += l[i] * w[i]
  avg = total / sum(w)
  return avg

## \brief Arithmetic average of given list.
#
# Find arithmetic average of data stored in a list.
def avg_arithmetic_list(l):
  total = 0.0
  for i in range(len(l)):
    total += l[i]
  avg = total / len(l)
  return avg


## \brief Average heart rate.
#
# Find arithmetic average heart rate.
#
# Use interpolated RR data.
def avg_hr_arithmetic(data):
  return avg_arithmetic_list(data.heart_rate)

## \brief Average heart rate weighted by rr interval.
#
# Find average heart rate. The heart rate is weighted by each
# respective RR interval.
#
# Use non interpolated RR data as received from Polar.
def avg_hr_weighted(data):
  return avg_weighted_list(data.heart_rate, data.rr_interval)

## \brief Average heart rate from beat count / total time.
#
# Find average heart rate by dividing total number of beats
# by total time.
#
# Use non interpolated RR data as received from Polar.
def avg_hr_count(data):
  count = len(data.heart_rate)
  dt = data.find_time_length()
  avg = count / dt * 60.0
  return avg
  
def print_stats_file(filename, interp=-1):
  data = Data.Data.load_raw_data(filename)
  print(filename)
  print_stats_data(data, interp)

def strike(string, flag=-1):
  if (flag == 1):
    return "XXX" + string
  else:
    return "   " + string
  
def print_stats_data(data, interp=-1):
  if (interp == 1):
    flag_interp = 0
    flag_rr = 1
  elif (interp == 0):
    flag_interp = 1
    flag_rr = 0
  else:
    flag_interp = 0
    flag_rr = 0
  
  avg_c = avg_hr_count(data)
  print(strike("count %f" % avg_c, flag_rr))

  avg_w = avg_hr_weighted(data)
  print(strike("weigh %f" % avg_w, flag_rr))
  
  avg_a = avg_hr_arithmetic(data)
  print(strike("arith %f" % avg_a, flag_interp))
  
  
  


"""#########################################################
############################################################
### Main function                                        ###
############################################################
#########################################################"""

def main(input_path, path_prep):

  ## Generate filenames
  # subj%d_rr.tsv
  filename_rr1 = os.path.join(input_path, k.FILENAME_RR_S1)
  filename_rr2 = os.path.join(input_path, k.FILENAME_RR_S2)
  
  # 02_preprocess/subj%d_rr_inferred_from_ecg.tsv
  filename_ecg_rr1 = os.path.join(path_prep, k.FILENAME_ECG_RR_S1)
  filename_ecg_rr2 = os.path.join(path_prep, k.FILENAME_ECG_RR_S2)

  # 02_preprocess/subj%d_rr_linear.tsv
  filename_rr_linear1 = os.path.join(path_prep, k.FILENAME_RR_LIN_S1)
  filename_rr_linear2 = os.path.join(path_prep, k.FILENAME_RR_LIN_S2)
  # 02_preprocess/subj%d_rr_nn.tsv
  filename_rr_nn1 = os.path.join(path_prep, k.FILENAME_RR_NN_S1)
  filename_rr_nn2 = os.path.join(path_prep, k.FILENAME_RR_NN_S2)
  # 02_preprocess/subj%d_ecg_inferred_rr_linear.tsv
  filename_ecg_rr_linear1 = os.path.join(path_prep, k.FILENAME_ECG_RR_LIN_S1)
  filename_ecg_rr_linear2 = os.path.join(path_prep, k.FILENAME_ECG_RR_LIN_S2)
  # 02_preprocess/subj%d_ecg_inferred_rr_nn.tsv
  filename_ecg_rr_nn1 = os.path.join(path_prep, k.FILENAME_ECG_RR_NN_S1)
  filename_ecg_rr_nn2 = os.path.join(path_prep, k.FILENAME_ECG_RR_NN_S2)

  interp = 0
  print_stats_file(filename_rr1, interp)
  print_stats_file(filename_ecg_rr1, interp)
  interp = 1
  print_stats_file(filename_rr_linear1, interp)
  print_stats_file(filename_rr_nn1, interp)
  print_stats_file(filename_ecg_rr_linear1, interp)
  print_stats_file(filename_ecg_rr_nn1, interp)
  print()
  interp = 0
  print_stats_file(filename_rr2, interp)
  print_stats_file(filename_ecg_rr2, interp)
  interp = 1
  print_stats_file(filename_rr_linear2, interp)
  print_stats_file(filename_rr_nn2, interp)
  print_stats_file(filename_ecg_rr_linear2, interp)
  print_stats_file(filename_ecg_rr_nn2, interp)

  



if __name__ == "__main__":

  if (len(sys.argv)) < 2:
    print("Usage: stats.py <input_path>")
    sys.exit()

  input_path = sys.argv[1]
  path_prep = os.path.join(input_path, k.FOLDER_PREP)

  main(input_path, path_prep)
