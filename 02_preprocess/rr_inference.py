import sys
from biosppy.signals import ecg
import numpy as np
import os

filepath = os.path.dirname(__file__)
modpathrel = os.path.join(filepath, "..")
modpathabs = os.path.abspath(modpathrel)
sys.path.append(modpathabs)
import Data
import const as k
import utils


def process_ecg_signal(data):
	ECG_SAMPLING_FREQ = 130
	if data.datatype != k.TYPE_ECG:
		return None
	signal = data.ecg
	#rate = 130.0
	#rate = 140.0
	rate = data.find_ecg_sampling_rate()
	#rate = (rate - ECG_SAMPLING_FREQ) * 2.0 + ECG_SAMPLING_FREQ
	out = ecg.ecg(signal=signal, sampling_rate=rate, show=False)
	return out

def infer_rr_intervals_from_ecg(filename_input, filename_output):

	data = Data.Data.load_raw_data(filename_input)

	new_data = Data.Data(k.TYPE_RR)
	signal = data.ecg
	file_t0 = data.time[0]

	out = process_ecg_signal(data)

	time_intervals = out[0]
	rpeaks = out[2]
	heart_rate = out[-1]
	last_peak = rpeaks[0]

	for i in range(1, len(heart_rate)):

		peak_index = rpeaks[i]
		time = time_intervals[peak_index] + file_t0
		last_time = time_intervals[last_peak] + file_t0
		hr = heart_rate[i]
		rr = (float(time) - float(last_time))*1024
		time = float(time)

		new_data.time.append(time)
		new_data.heart_rate.append(hr)
		new_data.rr_interval.append(rr)

		last_peak = peak_index

	overwrite = 1
	new_data.save_raw_data(filename_output, overwrite)

if __name__ == '__main__':

	if len(sys.argv) < 2:
		print("Usage: `python rr_inference.py <data_file.tsv>`")
		print("\tYou can pass in one or more files.")

	files = sys.argv[1:]

	for f in sys.argv[1:]:

		if 'ecg' in f:
			print(f"Inferring RR intervals from ECG values of the file {f}.")
			infer_rr_intervals_from_ecg(f)

		else:
			print(f'All files should contain ECG values, ignoring file {f}.')
