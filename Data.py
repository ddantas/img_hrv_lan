#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""#########################################################
############################################################
### Save data from Polar H10 sensor.                     ###
###                                                      ###
### Thanks to                                            ###
### https://github.com/mmuramatsu/Heart-rate-collector   ###
###                                                      ###
### Author: Daniel Dantas                                ###
### Last edited: Jan 2022                                ###
############################################################
#########################################################"""

import numpy as np
import pandas as pd
import os

TYPE_RR  = "R"
TYPE_ECG = "E"

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

  ## \brief Save data to file.
  #
  # Save the Polar H10 data to file. When obtaining data from streaming, first
  # call remove() to reset the file, then, inside a loop, call save_raw_data() and
  # clear() afterwards.
  #
  # If self.datatype == TYPE_RR then columns are
  #   time: computer timestamp in seconds.
  #   heart_rate: heart rate in beats per minute.
  #   rr_interval: interval between two R peaks in mis (1/1024 s).
  #
  # If self.datatype == TYPE_ECG then columns are
  #   time: computer timestamp in seconds.
  #   timestamp: timestamp from Polar internal clock.
  #   ecg: ECG potential in microvolts.
  #
  # @param filename File where data will be stored.
  def save_raw_data(self, filename):
    if os.path.exists(filename):
      if self.time == []:
        return

    if (self.datatype == TYPE_RR):
      df = pd.DataFrame(data = {"time": self.time,
                                "heart_rate": self.values_hr,
                                "rr_interval": self.values_rr})
    elif (self.datatype == TYPE_ECG):
      df = pd.DataFrame(data = {"time": self.time,
                                "timestamp": self.timestamp,
                                "ecg": self.values_ecg})

    # print(df)

    if not os.path.exists(filename):
      print (f'------ Save raw data in \"{filename}\" ------\n\n')
      df.to_csv(filename, sep = '\t', index=False, mode = "w", header = True)
    else:
      df.to_csv(filename, sep = '\t', index=False, mode = "a", header = False)

  ## \brief Load data from file.
  #
  # Load Polar H10 data from file.
  #
  # Tries to autodetect the datatype from column names. Returns with error if
  # unable to detect the datatype.
  #
  # @param filename File where data will be stored.
  @staticmethod
  def load_raw_data(filename):
    if not os.path.exists(filename):
      raise FileNotFoundError("File does not exixt: " + filename)

    df = pd.read_csv(filename, sep="\t")

    if len(df.columns) < 3:
      raise ValueError("At least three columns expected.")

    if (df.columns[2] == "rr_interval"):
      data = Data(TYPE_RR)
      data.time        = df.loc[:, "time"].tolist()
      data.heart_rate  = df.loc[:, "heart_rate"].tolist()
      data.rr_interval = df.loc[:, "rr_interval"].tolist()
    elif (df.columns[2] == "ecg"):
      data = Data(TYPE_ECG)
      data.time        = df.loc[:, "time"].tolist()
      data.timestamp   = df.loc[:, "timestamp"].tolist()
      data.ecg         = df.loc[:, "ecg"].tolist()
    else:
      raise ValueError("Unable to detect datatype from column name: " + df.column[2])

    return data


