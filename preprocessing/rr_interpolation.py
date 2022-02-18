import sys

def save_lines_to_file(lines_list, filename, file_suffix):

	new_file = filename[:-4] + file_suffix
	content = 'time\theart_rate\trr_interval\n'
	for l in lines_list:
		new_line = str(l[0]) + '\t' + str(l[1]) + '\t' + str(l[2]) + '\n'
		content += new_line

	with open(new_file, 'w') as f_w:
		print(f"Saving new file to {new_file}")
		f_w.write(str(content))

def nearest_neighbor():
	files = sys.argv[1:]

	for f in files:
		with open(f) as f_read:
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

			save_lines_to_file(nn_lines, f, '_nn.tsv')


def linear_preprocess():

	def linear_interpolate(x_values, y_values):
		return lambda x: (y_values[0]*(x_values[1] - x) + y_values[1]*(x - x_values[0]))/(x_values[1] - x_values[0])

	files = sys.argv[1:]
	for f in files:
		with open(f) as f_read:

			lines = f_read.readlines()[1:]
			lines = sorted(set(lines))
			interp_lines = []
			t0 = float(lines[0].split()[0])

			for i in range(len(lines)):
				line = lines[i]

				if i == len(lines)-1:
					next_line = lines[0]

				else:
					next_line = lines[i+1]

				time0, hr0, rr0 = line.split()
				time1, hr1, rr1 = next_line.split()

				x_values = [float(time0) - t0, float(time1) - t0]
				y_values = [int(rr0), int(rr1)]

				interp = linear_interpolate(x_values, y_values)
				x = round(float(time0) - t0)
				# print(x_values, y_values, x, interp(x))
				time = x
				hr = hr0
				rr = interp(x)
				interp_lines.append([time, hr, rr])

			save_lines_to_file(interp_lines, f, '_linear.tsv')

if __name__ == '__main__':

	if len(sys.argv) < 2:
		print("Usage: `python preprocessing.py <data_file.tsv>`")
		print("\tYou can pass in one or more files.")
		exit(1)

	print("Preprocessing RR intervals using nearest neighbor logic")
	nearest_neighbor()
	print("Preprocessing RR intervals with linear interpolation")
	linear_preprocess()