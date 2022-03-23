import os
import numpy as np
from biosppy.signals import ecg
import const as k

## \brief Replace extension with suffix.
#
#  @param filename Filename to be adjusted.
#  @param file_suffix Replace file extension.
def adjust_filename(filename, file_suffix):
  basename, file_extension = os.path.splitext(filename)
  result = basename + file_suffix
  return result

## \brief Get the time of start of the specified routine file and its duration.
#
#  @param routinefile File where a copy of the routine was saved. Contains the timestamp for when the capture started.
def get_t0_and_duration(routinefile):

  with open(routinefile) as f:
    lines = f.readlines()
    # first line of the routine file is the timestamp of the start of the routine
    start_timestamp = float(lines[0])
    # get last line, first value
    duration = float(lines[-1].strip(';')[0])

    return start_timestamp, duration

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
