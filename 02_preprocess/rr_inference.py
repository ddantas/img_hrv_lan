import sys

from biosppy.signals import ecg
import numpy as np
import os

import utils

filepath = os.path.dirname(__file__)
modpathrel = os.path.join(filepath, "..")
modpathabs = os.path.abspath(modpathrel)
sys.path.append(modpathabs)

import Data
import const as k

def infer_rr_intervals_from_ecg(filename):

	data = Data.Data.load_raw_data(filename)

	new_data = Data.Data(k.TYPE_RR)
	signal = data.ecg
	out = ecg.ecg(signal=signal, sampling_rate=130.0, show=False)

	time_intervals = out[0]
	rpeaks = out[2]
	heart_rate = out[-1]

	last_peak = rpeaks[0]
	for i in range(1, len(heart_rate)):

		peak_index = rpeaks[i]
		time = time_intervals[peak_index]
		last_time = time_intervals[last_peak]
		hr = heart_rate[i]
		rr = (float(time) - float(last_time))*1024
		time = float(time)

		new_data.time.append(time)
		new_data.heart_rate.append(hr)
		new_data.rr_interval.append(rr)

		last_peak = peak_index

	new_data.save_raw_data(utils.adjust_filename(filename, '_inferred_from_ecg.tsv'))

if __name__ == '__main__':

	if len(sys.argv) < 2:
		print("Usage: `python rr_inference.py <data_file.tsv>`")
		print("\tYou can pass in one or more files.")
		exit(1)

	files = sys.argv[1:]

	for f in sys.argv[1:]:

		if 'ecg' in f:
			print(f"Inferring RR intervals from ECG values of the file {f}.")
			infer_rr_intervals_from_ecg(f)

		else:
			print(f'All files should contain ECG values, ignoring file {f}.')
