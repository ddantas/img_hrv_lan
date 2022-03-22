import sys
import pandas as pd
import math as m
import os

import utils

filepath = os.path.dirname(__file__)
modpathrel = os.path.join(filepath, "..")
modpathabs = os.path.abspath(modpathrel)
sys.path.append(modpathabs)
import Data
import const as k

def nearest_neighbor(filename):

	data = Data.Data.load_raw_data(filename)

	df = pd.DataFrame({'time' : data.time, 'heart_rate' : data.heart_rate,\
										 'rr_interval' : data.rr_interval})
	df = df.drop_duplicates(ignore_index=True)
	df['time'] = df['time'] - df['time'].iat[0]

	new_data = Data.Data(k.TYPE_RR)

	if data.datatype != k.TYPE_RR:
		print(f"File {filename} is not of TYPE_RR")
		return

	j = 0
	len_time = round(df['time'].iat[-1] - df['time'].iat[0])+1

	for i in range(len_time):

		min_diff = abs(df['time'].iat[j] - i)
		changed = True
		j_min = j
		j += 1
		while changed and j < len_time:
			diff = abs(df['time'].iat[j] - i)
			if diff < min_diff:
				min_diff = diff
				j_min = j
				j = j+1

			else:
				changed = False

			if j == len_time:
				break

		nn = j_min
		j-=1

		new_data.time.append(nn)
		new_data.heart_rate.append(df['heart_rate'].iat[i])
		new_data.rr_interval.append(df['rr_interval'].iat[i])

	new_data.save_raw_data(utils.adjust_filename(filename, '_nn.tsv'))

def linear_preprocess(filename):

	def linear_interpolate(x_values, y_values):
		return lambda x: (y_values[0]*(x_values[1] - x) + y_values[1]*(x - x_values[0]))/(x_values[1] - x_values[0])

	data = Data.Data.load_raw_data(filename)
	time = [val - data.time[0] for val in data.time]

	time = [-0.5] + time + [time[-1] + 0.5]
	heart_rate = [data.heart_rate[0]] + data.heart_rate + [data.heart_rate[-1]]
	rr_interval = [data.rr_interval[0]] + data.rr_interval + [data.rr_interval[-1]]

	df = pd.DataFrame({'time' : time, 'heart_rate' : heart_rate,\
										 'rr_interval' : rr_interval})
	df = df.drop_duplicates(ignore_index=True)

	new_data = Data.Data(k.TYPE_RR)

	if data.datatype != k.TYPE_RR:
		print(f"File {filename} is not of TYPE_RR")
		return

	for i in range(len(df['time'])-1):

		cur, nxt = df['time'].iat[i], df['time'].iat[i+1]

		ints = range(m.ceil(cur), m.floor(nxt)+1)

		if len(ints) > 0:

			x_values = [cur, nxt]
			y_values_hr = [df['heart_rate'].iat[i], df['heart_rate'].iat[i+1]]
			y_values_rr = [df['rr_interval'].iat[i], df['rr_interval'].iat[i+1]]

			interp_hr = linear_interpolate(x_values, y_values_hr)
			interp_rr = linear_interpolate(x_values, y_values_rr)

			for n in ints:
				hr = interp_hr(n)
				rr = interp_rr(n)
				new_data.time.append(i)
				new_data.heart_rate.append(hr)
				new_data.rr_interval.append(rr)

	new_data.save_raw_data(utils.adjust_filename(filename, '_linear.tsv'))

def interpolate(filename):
	print(f"Preprocessing RR intervals using nearest neighbor strategy for file {filename}")
	nearest_neighbor(filename)
	print(f"Preprocessing RR intervals with linear interpolation for file {filename}")
	linear_preprocess(filename)


if __name__ == '__main__':

	if len(sys.argv) < 2:
		print("Usage: `python rr_interpolation.py <data_file.tsv>`")
		print("\tYou can pass in one or more files.")
		exit(1)

	for f in sys.argv[1:]:

		if 'rr' in f:
                   interpolate(f)
		else:
			print(f'All files should contain RR values, ignoring file {f}.')

