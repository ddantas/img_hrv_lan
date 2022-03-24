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

import const as k

TIME_UNINITIALIZED = -1

class Data:
  '''
  Data objects will store the data received from the device.
  '''

  def __init__(self, datatype):
    self.datatype = datatype
    if (datatype != k.TYPE_RR and datatype != k.TYPE_ECG):
      raise ValueError("Invalid datatype in Data constructor")
    self.t0 = TIME_UNINITIALIZED
    self.time = []
    #TYPE_RR
    self.heart_rate = []
    self.rr_interval = []
    #TYPE_ECG
    self.timestamp = []
    self.values_ecg = []

  def clear(self):
    self.time = []
    #TYPE_RR
    self.heart_rate = []
    self.rr_interval = []
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
  # Save the Polar H10 data to file. If file does not exist, it is created.
  # If file exists, data is appended to the end.
  #
  # When obtaining data from streaming, first
  # call remove() to reset the file, then, inside a loop, call save_raw_data()
  # and clear() afterwards.
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
  # @param overwrite If nonzero, remove file before writing.
  def save_raw_data(self, filename, overwrite=0):
    if os.path.exists(filename):
      if self.time == []:
        return

    if (overwrite != 0):
      self.remove(filename)

    df = self.as_dataframe()

    # print(df)

    if not os.path.exists(filename):
      print (f'------ Save raw data in \"{filename}\" ------\n\n')
      df.to_csv(filename, sep = '\t', index=False, mode = "w", header = True)
    else:
      df.to_csv(filename, sep = '\t', index=False, mode = "a", header = False)


  ## \brief Return data as dataframe.
  #
  # Return data in dataframe format compatible with pandas.
  #
  #
  def as_dataframe(self):
    if (self.datatype == k.TYPE_RR):
      df = pd.DataFrame(data = {"time": self.time,
                                "heart_rate": self.heart_rate,
                                "rr_interval": self.rr_interval})
    elif (self.datatype == k.TYPE_ECG):
      df = pd.DataFrame(data = {"time": self.time,
                                "timestamp": self.timestamp,
                                "ecg": self.values_ecg})
    return df


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
      data = Data(k.TYPE_RR)
      data.time        = df.loc[:, "time"].tolist()
      data.heart_rate  = df.loc[:, "heart_rate"].tolist()
      data.rr_interval = df.loc[:, "rr_interval"].tolist()

    elif (df.columns[2] == "ecg"):
      data = Data(k.TYPE_ECG)
      data.time        = df.loc[:, "time"].tolist()
      data.timestamp   = df.loc[:, "timestamp"].tolist()
      data.ecg         = df.loc[:, "ecg"].tolist()
    else:
      raise ValueError("Unable to detect datatype from column name: " + df.column[2])

    return data

  ## \brief Find list of ECG packet times.
  #
  # Find list of ECG packet times. The number of items corresponds to
  # the number of packages received from the Polar sensor.
  #
  # The object must have datatype == TYPE_ECG.
  def find_ecg_packet_times(self):
    if self.datatype != k.TYPE_ECG:
      return None
    from collections import Counter
    dic = Counter(self.time)
    packet_times = list(dic.keys())
    return packet_times

  ## \brief Find average packet time interval.
  #
  # Find average packet time interval of ECG data. The
  # object must have datatype == TYPE_ECG.
  #
  # The object must have datatype == TYPE_ECG.
  def find_ecg_avg_packet_interval(self):
    if self.datatype != k.TYPE_ECG:
      return None
    packet_times = self.find_ecg_packet_times()
    avg_packet_interval = (packet_times[-1] - packet_times[0]) / (len(packet_times) - 1)
    return avg_packet_interval

  ## \brief Find ECG full length.
  #
  # Find full time length of ECG data, equals to the maximum timestamp
  # minus the minimum timestamp plus an averate packet interval.
  #
  # The object must have datatype == TYPE_ECG.
  def find_ecg_time_length(self):
    if self.datatype != k.TYPE_ECG:
      return None
    avg_packet_interval = self.find_ecg_avg_packet_interval()
    packet_times = self.find_ecg_packet_times()
    full_length = (packet_times[-1] - packet_times[0]) + avg_packet_interval
    return full_length

  ## \brief Find ECG sampling rate.
  #
  # Find ECG sampling rate as quotient of number of samples by
  # full time length.
  #
  # The object must have datatype == TYPE_ECG.
  def find_ecg_sampling_rate(self):
    if self.datatype != k.TYPE_ECG:
      return None
    time_length = self.find_ecg_time_length()
    return len(self.ecg) / time_length
