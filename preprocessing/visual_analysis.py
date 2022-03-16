import matplotlib.pyplot as plt
from biosppy.signals import ecg
import pandas as pd
import numpy as np

from rr_inference import *

import sys
sys.path.append('../')
import Data


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
  out = ecg.ecg(signal=y, sampling_rate=130.0, show=False)

  #x_test = np.linspace(0.0, dt, len(y))
  x = out[0].tolist()

  return x, y, out

def plot_inferred_vs_real_rr(rr_values, inferred_rr_values, ecg_values):

  fig, axs = plt.subplots(3, figsize=(5,5))

  out = ecg_values[2]
  rpeaks = out[2]
  time_intervals = out[0]

  rr = [v/(1024.0) for v in rr_values[1]]
  rr = np.array([sum(rr[:i]) for i in range(len(rr))])
  rr += time_intervals[rpeaks[0]]
  i_rr = [v/(1024.0) for v in inferred_rr_values[1]]
  i_rr = np.array([sum(i_rr[:i]) for i in range(len(i_rr))])
  i_rr += time_intervals[rpeaks[0]]

  print(rr, i_rr)

  delta_t = 470
  time_ecg = [x for x in ecg_values[0] if x <= delta_t]
  i_rr_sliced = [x for x in i_rr if x <= delta_t]
  rr_sliced = [x for x in rr if x <= delta_t]
  values = ecg_values[1][:len(time_ecg)]

  x = [i for i in range(len(rr))]

  derivative_rr = []
  derivative_i_rr = []

  for i in range(len(i_rr)-1):
    x1 = rr[i+1] - rr[i]/(i+1 - i)
    x2 = i_rr[i+1] - i_rr[i]/(i+1 - i)
    derivative_rr.append(x1)
    derivative_i_rr.append(x2)

  m = len(derivative_rr)
  axs[2].plot(x[:m], derivative_rr[:m], color='red')
  n = len(derivative_i_rr)
  axs[2].plot(x[:n], derivative_i_rr[:n], color='black')

  axs[0].plot(time_ecg, values, lw=4)
  axs[1].plot(time_ecg, values, lw=4)
  axs[0].vlines(x=i_rr_sliced, ymin=min(values), ymax=max(values), color='black')
  #axs[1].vlines(x=rr_sliced, ymin=min(values), ymax=max(values), color='red')

  skip = 0
  dt = i_rr_sliced[skip] - i_rr_sliced[0]
  #dt = 4.0
  dt = 0.0
  rr_sliced = [x - dt for x in rr_sliced]

  axs[1].vlines(x=rr_sliced, ymin=min(values), ymax=max(values), color='red')

  plt.show()

if __name__ == '__main__':

  path = "../data/a003"
  subj = 2
  filename_rr  = "%s/subj%d_rr.tsv" % (path, subj)
  filename_ecg = "%s/subj%d_ecg.tsv" % (path, subj)
  filename_from_ecg = "%s/processed/subj%d_rr_inferred_from_ecg.tsv" % (path, subj)

  rr_values = construct_xy_from_file(filename_rr)
  infer_rr_intervals_from_ecg(filename_ecg)

  inferred_rr_values = construct_xy_from_file(filename_from_ecg)
  ecg_values = construct_xy_from_file_ecg(filename_ecg)

  plot_inferred_vs_real_rr(rr_values, inferred_rr_values, ecg_values)


