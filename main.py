#! /usr/bin/env python3.5
# -*- coding: utf-8 -*-
#pip3.5 install numpy scipy matplotlib scikit-learn

import svm_rbf              as s
import svm_data_acquisition as d

def verify_classes (c):
	try:
		d.classes = [int(x) for x in c.split(",")]
	except:
		return False
	for i in d.classes:
		if i > 9 or i < 0:
			return False
	return True

def run_random_test ():
	test_number = d.np.random.randint(low=0, high=len(d.x_test)-1)
	test        = d.x_test[test_number]
	test_class  = d.y_test[test_number]
	# prediction
	return s.pred([test])[0] == test_class

if __name__ == "__main__":
	
	# set C, gamma parameters of SVM with RBF kernel
	d.C     = 3
	d.gamma = 0.02
	# set train/test split ratio
	d.split = 0.35
	# set gestures for classsification
	classes = "0,1,4,5,6"

	if (verify_classes(classes)): 
		
		d.init_data_acquisition()
		s.init_model (d.C, d.gamma)
		
		train_results = s.train(d.X, d.y)*100
		tests_results = s.test(d.x_test, d.y_test)*100

		print ("Train results: {0:.3f}".format(train_results))
		print ("Verification results: {0:.3f}".format(tests_results))
		print ("Random signal test result: {0}".format(run_random_test()))

	



