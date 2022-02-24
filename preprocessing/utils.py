import os

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

