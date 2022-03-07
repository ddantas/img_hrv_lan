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
  

def get_duration_ideal(filename):

  if not(os.path.exists(filename)):
    print("Error opening file: " + filename)

  f = open(filename)
  routine_lines = f.readlines()
  # First line stores timestamp
  routine_lines[0] = "#" + routine_lines[0]

  max_time = 0.0
  for l in routine_lines:
    if l[0] == "#":
      continue

    cols = l.split(";")
    t = float(cols[0])
    if t > max_time:
      max_time = t

  print("Ideal duration: %f" % max_time)
  return max_time
  

def synchronize(input_routine, input_filename, output_filename):

  print(input_filename)
  actual = get_duration(input_filename)
  ideal  = get_duration_ideal(input_routine)
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
  
  input_filename1 = os.path.join(input_path, "subj1.mp4")
  input_filename2 = os.path.join(input_path, "subj2.mp4")
  output_filename1 = os.path.join(input_path, "subj1_sync.mp4")
  output_filename2 = os.path.join(input_path, "subj2_sync.mp4")
  input_routine = os.path.join(input_path, "routine.txt")

  synchronize(input_routine, input_filename1, output_filename1)
  synchronize(input_routine, input_filename2, output_filename2)

  
  pass


if __name__ == "__main__":

  #print('Number of arguments: {}'.format(len(sys.argv)))
  #print('Argument(s) passed: {}'.format(str(sys.argv)))
  if (len(sys.argv)) < 2:
    print("Usage: sync.py <input_path>")
    sys.exit()

  input_path = sys.argv[1]
  print("Input path: " + input_path)

  main(input_path)
