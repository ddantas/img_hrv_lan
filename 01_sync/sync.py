#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""#########################################################
############################################################
### Synchronize two videos of equal length by            ###
### maching speed and duration.                          ###
###                                                      ###
### Author: Daniel Dantas                                ###
### Last edited: Feb 2022                                ###
############################################################
#########################################################"""

import os
import sys
import re
import shlex
import subprocess

# Import module from parent folder
filepath = os.path.dirname(__file__)
modpathrel = os.path.join(filepath, "..")
modpathabs = os.path.abspath(modpathrel)
sys.path.append(modpathabs)
import const as k

def get_duration(filename):

  if not(os.path.exists(filename)):
    print("Error opening file: " + filename)
    
  process = subprocess.Popen(["ffprobe", filename], stderr=subprocess.PIPE)
  (output, err) = process.communicate()
  exit_code = process.wait()
  #print("OUTPUT: " + str(output))
  #print("ERR: " + str(err))

  r = re.search("Duration: ([\d:\.]+)", err.decode())
  duration_str = r.groups()[0]
  duration_arr = duration_str.split(":")
  duration_sec = float(duration_arr[2]) +          \
                 float(duration_arr[1]) * 60.0 +   \
                 float(duration_arr[0]) * 3600.0
  print("Duration: %s = %f " % (duration_str, duration_sec))
  
  return duration_sec
  

def synchronize(input_routine, input_filename, output_filename):

  print(input_filename)
  actual = get_duration(input_filename)
  ideal  = get_duration_ideal(input_routine)
  print("Ideal duration: %f" % ideal)
  r = ideal / actual

  cmd = 'ffmpeg -i %s -filter:v "setpts=%f*PTS" %s' % (input_filename, r, output_filename)
  print(cmd)
  process = subprocess.Popen(shlex.split(cmd), stderr=subprocess.PIPE)
  (output, err) = process.communicate()
  exit_code = process.wait()
  print(err.decode())


"""#########################################################
############################################################
### Main function                                        ###
############################################################
#########################################################"""

def main(input_path):
  
  filename_input1 = os.path.join(input_path, k.FILENAME_VIDEO_S1)
  filename_input2 = os.path.join(input_path, k.FILENAME_VIDEO_S2)
  filename_output1 = os.path.join(input_path, k.FOLDER_SYNC, k.FILENAME_VIDEO_SYNC_S1)
  filename_output2 = os.path.join(input_path, k.FOLDER_SYNC, k.FILENAME_VIDEO_SYNC_S2)
  input_routine = os.path.join(input_path, k.FILENAME_ROUTINE)

  folder_sync = os.path.join(input_path, k.FOLDER_SYNC)
  if not os.path.exists(folder_sync):
    os.mkdir(folder_sync)

  synchronize(input_routine, filename_input1, filename_output1)
  synchronize(input_routine, filename_input2, filename_output2)


if __name__ == "__main__":

  #print('Number of arguments: {}'.format(len(sys.argv)))
  #print('Argument(s) passed: {}'.format(str(sys.argv)))
  if (len(sys.argv)) < 2:
    print("Usage: sync.py <input_path>")
    sys.exit()

  input_path = sys.argv[1]
  print("Input path: " + input_path)

  main(input_path)
