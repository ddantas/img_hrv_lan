import os
import numpy as np
from biosppy.signals import ecg


# Remove?
def adjust_filename_old(filename, file_suffix):

	dir_tree = filename.split('/')
	filename = dir_tree[-1]
	cur_dir = '/'.join(dir_tree[:-1])

	if not os.path.exists(cur_dir + '/02_preprocess') and '02_preprocess' not in cur_dir:
		os.mkdir(cur_dir + '/02_preprocess')

	new_file = filename[:-4] + file_suffix
	if '02_preprocess' in cur_dir:
		save_dir = cur_dir + '/'

	else:
		save_dir = cur_dir + '/02_preprocess/'

	return save_dir + new_file

def adjust_filename(filename, file_suffix):
        basename, file_extension = os.path.splitext(filename)
        result = basename + file_suffix
        return result
