import sys

from utils import *

def nearest_neighbor(filename):

	with open(filename) as f_read:
		lines = f_read.readlines()[1:]
		lines = sorted(set(lines))
		nn_lines = []
		t0 = float(lines[0].split()[0])
		for line in lines:
			time, hr, rr = line.split()
			time = round(float(time) - t0)
			hr = int(hr)
			rr = int(rr)
			nn_lines.append([time, hr, rr])

		save_lines_to_file(nn_lines, filename, '_nn.tsv')

def linear_preprocess(filename):

	def linear_interpolate(x_values, y_values):
		return lambda x: (y_values[0]*(x_values[1] - x) + y_values[1]*(x - x_values[0]))/(x_values[1] - x_values[0])

	with open(filename) as f_read:

		lines = f_read.readlines()[1:]
		lines = sorted(set(lines))
		interp_lines = []
		t0 = float(lines[0].split()[0])

		for i in range(len(lines)):

			line = lines[i]

			if i >= len(lines)-1:
				next_line = lines[i-1]

			else:
				next_line = lines[i+1]

			time0, hr0, rr0 = line.split()
			time1, hr1, rr1 = next_line.split()

			x_values = [float(time0) - t0, float(time1) - t0]
			y_values_rr = [int(rr0), int(rr1)]
			y_values_hr = [int(hr0), int(hr1)]


			interp_rr = linear_interpolate(x_values, y_values_rr)
			interp_hr = linear_interpolate(x_values, y_values_hr)
			x = round(float(time0) - t0)
			# print(x_values, y_values, x, interp(x))
			time = x
			hr = interp_hr(x)
			rr = interp_rr(x)
			interp_lines.append([time, hr, rr])

		save_lines_to_file(interp_lines, filename, '_linear.tsv')

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

