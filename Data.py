import numpy as np
import pandas as pd
import os

TYPE_RR  = 1
TYPE_ECG = 2

TIME_UNINITIALIZED = -1

class Data:
  '''
  Data objects will store the data received from the device.
  '''

  def __init__(self, datatype):
    self.datatype = datatype
    if (datatype < TYPE_RR and datatype < TYPE_ECG):
      raise ValueError("Invalid datatype in Data constructor")
    self.t0 = TIME_UNINITIALIZED
    self.time = []
    #TYPE_RR
    self.values_hr = []
    self.values_rr = []
    #TYPE_ECG
    self.timestamp = []
    self.values_ecg = []

  def clear(self):
    self.time = []
    #TYPE_RR
    self.values_hr = []
    self.values_rr = []
    #TYPE_ECG
    self.timestamp = []
    self.values_ecg = []

  ## \brief Remove file if file exists.
  #
  #  @param filename File to be removed.
  @staticmethod
  def remove(filename):
    if os.path.exists(filename):
      os.remove(filename)

  def save_raw_data(self, filename):
    '''
    Save the all triples (time, hr, rr) received from the Polar H10.

    Parameters:
      filename (string): name from the output file
    '''
    if os.path.exists(filename):
      if self.time == []:
        return

    if (self.datatype == TYPE_RR):
      df = pd.DataFrame(data=[self.time, self.values_hr, self.values_rr])
      df = df.T
      df.columns = ['time', 'heart_rate', 'rr_interval']
    elif (self.datatype == TYPE_ECG):
      df = pd.DataFrame(data=[self.time, self.timestamp, self.values_ecg])
      df = df.T
      df.columns = ['time', 'timestamp', 'ecg']

    if not os.path.exists(filename):
      print (f'------ Save raw data in \"{filename}\" ------\n\n')
      df.to_csv(filename, sep = '\t', mode = "w", header = True)
    else:
      df.to_csv(filename, sep = '\t', mode = "a", header = False)



