#! /usr/bin/env python3.5
# -*- coding: utf-8 -*-
#file  -- svm_rbf.py --

import svm_data_acquisition  as d
from   sklearn               import svm
from   sklearn.preprocessing import QuantileTransformer

model      = svm.SVC()
quantile_f = QuantileTransformer()

def init_model (c, gamma):
	global model
	model = svm.SVC(kernel='rbf', C=c, gamma=gamma)

def train (X, y):
	global quantile_f
	X = quantile_f.fit_transform(X)
	model.fit(X, y)
	return model.score(X, y)

def test (x_test, y_test):
	global quantile_f
	return model.score(quantile_f.transform(x_test), y_test)

def pred (p):
	global quantile_f
	return model.predict(quantile_f.transform(p))