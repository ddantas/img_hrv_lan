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
### Last edited: Sep 2022                                ###
############################################################
#########################################################"""

import matplotlib.pyplot as plt

import const as k

DATA_MAX_LEN = 500
DATA_MAX_LEN_AUDIO = 5000

COLOR_RR    = "red"
COLOR_ECG   = "blue"
COLOR_AUDIO = "gray"

class Plot():
  def __init__(self, with_audio=False):
    self.fig = None
    self.ax_rr = None
    self.ax_ecg = None
    self.data_rr = []
    self.data_ecg = []
    self.with_audio = with_audio
    if (self.with_audio):
      self.ax_audio = None
      self.data_audio = []
      self.idrop = 0
      self.maxdrop = 20

  def clear_rr(self):
    self.ax_rr.clear()
    self.ax_rr.set_title("Heart rate (BPM)")
    self.ax_rr.set_xlim([0, DATA_MAX_LEN])
      
  def clear_ecg(self):
    self.ax_ecg.clear()
    self.ax_ecg.set_title("ECG")
    self.ax_ecg.set_xlim([0, DATA_MAX_LEN])

  def clear_audio(self):
    self.ax_audio.clear()
    self.ax_audio.set_title("Audio")
    self.ax_audio.set_xlim([0, DATA_MAX_LEN_AUDIO])
    self.ax_audio.set_ylim([0, 255])

  def init(self):
    print("PLot.init")
    plt.ion()
    if (self.with_audio):
      self.fig, self.ax_audio = plt.subplots()
      self.fig.set_size_inches(3, 1)
      self.clear_audio()
    else:
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
      line_rr, = self.ax_rr.plot(self.data_rr, color=COLOR_RR)
    elif (datatype == k.TYPE_ECG):
      if (len(self.data_ecg) + len(data) > DATA_MAX_LEN):
        #self.data_ecg = self.data_ecg[-DATA_MAX_LEN]
        self.clear_ecg()
        self.data_ecg = []
        self.data_ecg.extend(data)
      else:
        self.data_ecg.extend(data)
      line_ecg, = self.ax_ecg.plot(self.data_ecg, color=COLOR_ECG)
    elif (datatype == k.TYPE_AUDIO):
      self.idrop = self.idrop + 1
      if (self.idrop >= self.maxdrop):
        self.idrop = 0
        data_new = list(data)
        data_new = [(x + 128) % 256 for x in data_new]
        if (len(self.data_audio) + len(data) > DATA_MAX_LEN_AUDIO):
          #self.data_audio = self.data_audio[-DATA_MAX_LEN]
          self.clear_audio()
          self.data_audio = []
          self.data_audio.extend(data_new)
        else:
          self.data_audio.extend(data_new)
        line_audio, = self.ax_audio.plot(self.data_audio, color=COLOR_AUDIO)
        print(".", end="")
        plt.pause(0.05)
    #plt.subplots_adjust(top = 0.9)
    if (datatype == k.TYPE_RR or datatype == k.TYPE_ECG):
      self.fig.tight_layout(pad=1.0)
      plt.pause(0.1)

  def close(self):
    plt.close(self.fig)

def main(with_audio):
  plt.ion()

  data_rr = [None] * 100
  data_y = [55,40,76,34,50,20]
  i_rr = 0
  data_rr[i_rr:i_rr+len(data_y)] = data_y

  if (with_audio):
    plot_audio = plt.axes()
  else:
    fig = plt.figure()
    plot_rr = fig.add_subplot(211)
    plot_ecg = fig.add_subplot(212)

  if (with_audio):
    line_audio, = plot_audio.plot(data_y, color=COLOR_AUDIO)
    plt.pause(0.02)
  else:
    line_rr, = plot_rr.plot(data_rr, color=COLOR_RR)
    plt.pause(0.02)
    line_ecg, = plot_ecg.plot(data_y, color=COLOR_ECG)
    plt.pause(0.02)



if __name__ == '__main__':
  with_audio = True
  main(with_audio)
