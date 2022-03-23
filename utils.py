import os
import numpy as np
from biosppy.signals import ecg


## \brief Replace extension with suffix.
#
#  @param filename Filename to be adjusted.
#  @param file_suffix Replace file extension.
def adjust_filename(filename, file_suffix):
  basename, file_extension = os.path.splitext(filename)
  result = basename + file_suffix
  return result

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
