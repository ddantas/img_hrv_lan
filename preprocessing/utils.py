import os
import numpy as np
from biosppy.signals import ecg

def get_ecg_tuple(file):
	with open(file) as f:
		lines = f.readlines()[1:]
		raw_ecg = [int(line.split()[-1]) for line in lines]

		signal = np.array(raw_ecg)
		out = ecg.ecg(signal=signal, sampling_rate=130.0, show=False)

		return out

def get_hr_from_file(file):

  with open(file) as f:
    lines = f.readlines()[1:]
    lines = sorted(set(lines))
    hr_values = []
    for line in lines:
      _, hr, _ = line.split()
      hr_values.append(hr)

  return hr_values

def save_lines_to_file(lines_list, filename, file_suffix):

	dir_tree = filename.split('/')
	filename = dir_tree[-1]
	cur_dir = '/'.join(dir_tree[:-1])

	if not os.path.exists(cur_dir + '/processed'):
		os.mkdir(cur_dir + '/processed')

	new_file = filename[:-4] + file_suffix
	save_dir = cur_dir + '/processed/'

	content = 'time\theart_rate\trr_interval\n'
	for l in lines_list:
		new_line = str(l[0]) + '\t' + str(l[1]) + '\t' + str(l[2]) + '\n'
		content += new_line


	with open(save_dir + new_file, 'w') as f_w:
		print(f"Saving new file to {save_dir + new_file}")
		f_w.write(str(content))

