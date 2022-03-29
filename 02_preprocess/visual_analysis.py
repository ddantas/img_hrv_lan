import matplotlib.pyplot as plt
from biosppy.signals import ecg
import pandas as pd
import numpy as np
import sys
import os

import rr_inference

# Import module from parent folder
filepath = os.path.dirname(__file__)
modpathrel = os.path.join(filepath, "..")
modpathabs = os.path.abspath(modpathrel)
sys.path.append(modpathabs)
import Data
import const as k


## \brief Read RR data from TSV file.
#
#  Read RR data from TSV file, and return two vectors, x and y: x has the time a packet
#  was received by the computer, and; y has the RR peak intervals in mis (1/1024 * s)
#
#  @param file TSV filename with RR data.
def construct_xy_from_file(file):
  data = Data.Data.load_raw_data(file)
  x = [val - data.time[0] for val in data.time]
  y = data.rr_interval
  return x, y

def construct_xy_from_file_ecg(file):
  data = Data.Data.load_raw_data(file)
  y = data.ecg

  #from collections import Counter
  #dic = Counter(data.time)
  #packet_times = list(dic.keys())
  #avg_packet_time = (packet_times[-1] - packet_times[0]) / (len(packet_times) - 1)
  #dt = (packet_times[-1] - packet_times[0]) + avg_packet_time

  #rate = len(y) / dt
  #out = ecg.ecg(signal=y, sampling_rate=130.0, show=False)
  out = rr_inference.process_ecg_signal(data)

  #x_test = np.linspace(0.0, dt, len(y))
  x = out[0].tolist()

  return x, y, out

def plot_inferred_vs_real_rr(rr_values, inferred_rr_values, ecg_values):

  fig, axs = plt.subplots(3, figsize=(5,5))

  out = ecg_values[2]
  rpeaks = out[2]
  time_intervals = out[0]

  ## Multiply by 60.0 to obtain beats per minute.
  del_rr   = [(v / 1024) for v in rr_values[1]]
  del_irr = [(v / 1024) for v in inferred_rr_values[1]]

  rr = np.array([sum(del_rr[:i]) for i in range(len(del_rr)+1)]) # rr is missing a beat in t = 0.0
  rr += time_intervals[rpeaks[0]]
  i_rr = np.array([sum(del_irr[:i]) for i in range(len(del_irr)+1)])
  i_rr += time_intervals[rpeaks[0]]

  print(rr, i_rr)

  time_ecg = [x for x in ecg_values[0]]
  i_rr_sliced = [x for x in i_rr]
  rr_sliced = [x for x in rr]
  values = ecg_values[1][:len(time_ecg)]

  x = [i for i in range(len(rr))]

  m = len(del_rr)
  axs[2].plot(x[:m], del_rr[:m], color='red')
  n = len(del_irr)
  axs[2].plot(x[:n], del_irr[:n], color='black')

  axs[0].plot(time_ecg, values, lw=4)
  axs[1].plot(time_ecg, values, lw=4)
  axs[0].vlines(x=i_rr_sliced, ymin=min(values), ymax=max(values), color='black')
  #axs[1].vlines(x=rr_sliced, ymin=min(values), ymax=max(values), color='red')

  skip = 5
  dt = i_rr_sliced[skip] - i_rr_sliced[0]
  #dt = 4.0
  #dt = 0.0
  rr_sliced = [x - dt for x in rr_sliced]

  axs[1].vlines(x=rr_sliced, ymin=min(values), ymax=max(values), color='red')

  plt.show()

if __name__ == '__main__':

  path = "../data/a003"
  subj = 2
  filename_rr       = os.path.join(path, k.FILENAME_RR % subj)
  filename_ecg      = os.path.join(path, k.FILENAME_ECG % subj)
  filename_from_ecg = os.path.join(path, k.FOLDER_PREP, k.FILENAME_ECG_RR % subj)

  rr_values = construct_xy_from_file(filename_rr)
  rr_inference.infer_rr_intervals_from_ecg(filename_ecg, filename_from_ecg)

  inferred_rr_values = construct_xy_from_file(filename_from_ecg)
  ecg_values = construct_xy_from_file_ecg(filename_ecg)

  plot_inferred_vs_real_rr(rr_values, inferred_rr_values, ecg_values)


