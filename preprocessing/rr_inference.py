import sys

from biosppy.signals import ecg
import numpy as np

from utils import *

def infer_rr_intervals_from_ecg(file):

	with open(file) as f_read:

		lines = f_read.readlines()[1:]
		print(file)

		raw_ecg = [int(line.split()[-1]) for line in lines]

		signal = np.array(raw_ecg)
		out = ecg.ecg(signal=signal, sampling_rate=130.0, show=False)

		rpeaks = out[2]
		heart_rate = out[-1]

		print(len(set(heart_rate)), len(rpeaks))

		t0 = lines[0].split()[0]

		rr_lines = []

		last_peak = rpeaks[0]

		for i in range(1, len(rpeaks)-1):

			peak_index = rpeaks[i]

			time, _, _ = lines[peak_index].split()
			last_time, _, _ = lines[last_peak].split()

			hr = heart_rate[i]
			rr = (float(time) - float(last_time))*1000/1.024
			time = float(time)

			rr_lines.append([time, hr, rr])
			last_peak = peak_index

		# use rr standard filename string
		filename = file[:-7] + 'rr.tsv'
		save_lines_to_file(rr_lines, filename, '_inferred_from_ecg.tsv')

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