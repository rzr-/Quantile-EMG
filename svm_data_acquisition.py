#! /usr/bin/env python3.5
# -*- coding: utf-8 -*-
#file  -- svm_data_acquisition.py --

import numpy as np
from   scipy.io import loadmat
from   sklearn.model_selection import train_test_split

test_data = []; left = 130; right  = 220
c         = 0.; gamma              = 0.
split     = 0.; data_file_location = "data/data10mov_raw.mat"
classes   = []
datasets  = []; data_length        = 0 
X         = []; x_test             = []	
y         = []; y_test             = []

classes_strings = ["Кисть Вверх", "Кисть Вниз", "Сжатие", "Сжатие указ. пальца", \
				  "Сжатие среднего пальца", "Сжатие безымянного пальца", \
				  "Щелчок", "Разжимание всех пальцев", \
				  "Поворот кисти влево", "Поворот кисти вправо"]

def init_data_acquisition():
	global X, x_test, y, y_test
	global data_length, test_data
	
	if (process_data (data_file_location) == True):
		test_data = np.vstack ((datasets[classes[0]]))
		target_data = [classes[0]] * data_length 
		for c in range(1, len(classes)):
			test_data    = np.vstack ((test_data, datasets[classes[c]]))
			target_data += [classes[c]] * data_length
		
		X, x_test, y, y_test = train_test_split(test_data, 
												target_data, 
												train_size=split, 
												test_size=1-split, 
												random_state=0)
		return True
	else:
		return "data_not_organised"


def process_data (data_file_location):
	global datasets, test_data, data_length
	global X, x_test, y, y_test

	def first_index(k):
		k_min = 0;   k_max = 999
		k_min_i = 0; k_max_i = 0
		for i in range(0, len(k)):
			if (k[i] < k_max) : 
				k_max = k[i]; k_max_i = i
			if (k[i] > k_min) : 
				k_min = k[i]; k_min_i = i
		return min(k_min_i, k_max_i)

	def get_k_data (k):
		index = max(first_index(data[0][k].T[0]), left)
		l = index-left; r = index+right
		s = np.vstack(( np.array(data[0][k][l:r].T) ))
		for i in range (1, data_length, 1):
			index = max(first_index(data[i][k].T[0]), left)
			l = index-left; r = index+right
			s = np.vstack (( s, np.array(data[i][k][l:r].T) ))
		return s

	try:
		data        = loadmat(data_file_location)
		data        = np.array(data["data_tmp"])
		data_length = len(data)
		n_classes = len(data[0])
		for i in range(0, n_classes):
			datasets.append(get_k_data(i))

	except:
		return "data_not_organised"
	
	return True