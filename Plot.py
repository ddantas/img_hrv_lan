#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""#########################################################
############################################################
### Plot data from Polar H10 sensor.                     ###
###                                                      ###
### Thanks to                                            ###
### https://github.com/mmuramatsu/Heart-rate-collector   ###
###                                                      ###
### Author: Daniel Dantas                                ###
### Last edited: Jan 2022                                ###
############################################################
#########################################################"""

import matplotlib.pyplot as plt

import const as k

DATA_MAX_LEN = 500

class Plot():
  def __init__(self):
    self.fig = None
    self.ax_rr = None
    self.ax_ecg = None
    self.data_rr = []
    self.data_ecg = []

  def clear_rr(self):
    self.ax_rr.clear()
    self.ax_rr.set_title("Heart rate (BPM)")
    self.ax_rr.set_xlim([0, DATA_MAX_LEN])
      
  def clear_ecg(self):
    self.ax_ecg.clear()
    self.ax_ecg.set_title("ECG")
    self.ax_ecg.set_xlim([0, DATA_MAX_LEN])  

  def init(self):
    plt.ion()
    self.fig, (self.ax_rr, self.ax_ecg) = plt.subplots(2, 1)
    self.clear_rr()
    self.clear_ecg()
    
  def plot_incremental(self, data, datatype):
    if (datatype == k.TYPE_RR):
      if (len(self.data_rr) + len(data) > DATA_MAX_LEN):
        #self.data_rr = self.data_rr[-DATA_MAX_LEN]
        self.clear_rr()
        self.data_rr = []
        self.data_rr.extend(data)
      else:
        self.data_rr.extend(data)
      line_rr, = self.ax_rr.plot(self.data_rr, color="red")
    elif (datatype == k.TYPE_ECG):
      if (len(self.data_ecg) + len(data) > DATA_MAX_LEN):
        #self.data_ecg = self.data_ecg[-DATA_MAX_LEN]
        self.clear_ecg()
        self.data_ecg = []
        self.data_ecg.extend(data)
      else:
        self.data_ecg.extend(data)
      line_ecg, = self.ax_ecg.plot(self.data_ecg, color="blue")
    #plt.subplots_adjust(top = 0.9)
    self.fig.tight_layout(pad=1.0)
    plt.pause(0.1)

  def close(self):
    plt.close(self.fig)

def main():
  plt.ion()
  fig = plt.figure()

  data_rr = [None] * 100
  data_y = [55,40,76,34,50,20]
  i_rr = 0
  data_rr[i_rr:i_rr+len(data_y)] = data_y
  
  plot_rr = fig.add_subplot(211)
  plot_ecg = fig.add_subplot(212)

  line_rr, = plot_rr.plot(data_rr, color="red")
  plt.pause(0.02)
  line_ecg, = plot_ecg.plot(data_y, color="blue")
  plt.pause(0.02)


if __name__ == '__main__':
  main()
