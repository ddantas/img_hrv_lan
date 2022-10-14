import os
import numpy as np
from biosppy.signals import ecg
import const as k

## \brief Remove file if file exists.
#
#  @param filename File to be removed.
def remove(filename):
  if os.path.exists(filename):
    os.remove(filename)

## \brief Replace extension with suffix.
#
#  @param filename Filename to be adjusted.
#  @param file_suffix Replace file extension.
def adjust_filename(filename, file_suffix):
  basename, file_extension = os.path.splitext(filename)
  result = basename + file_suffix
  return result

## \brief Get the time of start of the specified routine file.
#
#  Get the time of start of the specified routine file. It is
#  stored in the first line of the file
#
#  @param filename_routine File where a copy of the routine was
#    saved. Contains the timestamp for when the capture started.
def get_time_start(filename_timestamp):

  if not(os.path.exists(filename_timestamp)):
    print("Error opening file: " + filename_timestamp)

  with open(filename_timestamp) as f:
    lines = f.readlines()
    # first line of the routine file is the timestamp of the start of the routine
    start_timestamp = float(lines[0])
    return start_timestamp


## \brief Get the maximum time in routine file.
#
#  Get the maximum time in routine file. Commented lines are
#  ignored.
#
#  @param filename_routine File where a copy of the routine was saved.
def get_duration_ideal(filename_routine):

  if not(os.path.exists(filename_routine)):
    print("Error opening file: " + filename_routine)

  f = open(filename_routine)
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

  return max_time

## \brief Print exception message preceded with file and function name.
#
#  @param msg Exception message.
#  @param func Function name.
#  @param file File name. Caller may use __file__.
def print_exception(msg, func, file):
  print("Exception at %s: %s: %s" % (os.path.basename(file), func, msg))

## \brief Print message preceded with file and function name.
#
#  @param msg Message.
#  @param func Function name.
#  @param file File name. Caller may use __file__.
def print_message(msg, func, file):
  print("%s: %s: %s" % (os.path.basename(file), func, msg))

## \brief Print message preceded with file and function name.
#
#  @param msg Message.
#  @param func Function name.
#  @param file File name. Caller may use __file__.
def test_message():
  print_message("Hello, world!", test_message.__name__, __file__)

"""#########################################################
############################################################
### Main function                                        ###
############################################################
#########################################################"""


if __name__ == "__main__":

  test_message()
