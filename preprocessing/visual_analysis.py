import matplotlib.pyplot as plt
from biosppy.signals import ecg
import pandas as pd
import numpy as np

from rr_inference import *


def construct_xy_from_file(file):
  x = []
  y = []

  with open(file) as f_read:

    lines = f_read.readlines()[1:]
    t0 = float(lines[0].split()[0])
    for line in lines:
      time, _, value = line.split()
      x.append(float(time) - t0)
      y.append(float(value))

  return x, y

def construct_xy_from_file_ecg(file):
  x = []
  y = []
  with open(file) as f_read:

    lines = f_read.readlines()[1:]

    raw_ecg = [int(line.split()[-1]) for line in lines]
    signal = np.array(raw_ecg)

    out = ecg.ecg(signal=signal, sampling_rate=130.0, show=False)
    time_intervals = out[0]

    for i in range(len(lines)):
      _, _, value = lines[i].split()
      x.append(time_intervals[i])
      y.append(float(value))

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

  axs[2].plot(x[:521], derivative_rr[:521], color='red')
  axs[2].plot(x[:521], derivative_i_rr[:521], color='black')

  axs[0].plot(time_ecg, values, lw=4)
  axs[1].plot(time_ecg, values, lw=4)
  axs[0].vlines(x=i_rr_sliced, ymin=min(values), ymax=max(values), color='black')
  #axs[1].vlines(x=rr_sliced, ymin=min(values), ymax=max(values), color='red')

  skip = 0
  dt = i_rr_sliced[skip] - i_rr_sliced[0]
  dt = 4.0
  rr_sliced = [x - dt for x in rr_sliced]

  axs[1].vlines(x=rr_sliced, ymin=min(values), ymax=max(values), color='red')

  plt.show()

if __name__ == '__main__':

  rr_values = construct_xy_from_file('../data/a003/subj2_rr.tsv')

  infer_rr_intervals_from_ecg('../data/a003/subj2_ecg.tsv')
  inferred_rr_values = construct_xy_from_file('../data/a003/processed/subj2_rr_inferred_from_ecg.tsv')
  ecg_values = construct_xy_from_file_ecg('../data/a003/subj2_ecg.tsv')
  plot_inferred_vs_real_rr(rr_values, inferred_rr_values, ecg_values)


