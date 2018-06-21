#! /usr/bin/env python3.5
# -*- coding: utf-8 -*-
#file  -- svm_plot.py --

import numpy                  as np
import matplotlib.pyplot      as plt
import matplotlib.animation   as animation
from   mpl_toolkits.mplot3d   import Axes3D
from   matplotlib.collections import PolyCollection
from   matplotlib             import colors as mcolors

sizes = [[0, 100], [10, 90], [20, 80], [30, 70],
	     [40, 60], [50, 50], [60, 40], [70, 30],
		 [80, 20], [90, 10], [-1, -1]]
screen_width  = 0; main_window_width  = 0
screen_height = 0; main_window_height = 0

def plot_single (data):
	fig1 = plt.figure(dpi=100) 
	plt.plot(data)
	fig1.savefig('data/plot_single.png', transparent=True)
	plt.clf()
	plt.close()

def plot_train_test (do):
	global sizes

	if (do == "train"):
		labels   = 'Точность обучения', 'Погрешность'
		filename = 'data/plot_train.png'
		fig1 = plt.figure(num='Обучение', dpi=100) 
		
	if (do == "test"):
		labels   = 'Kлассифировано\nправильно', \
				   'Классифицировано\nнеправильно'
		filename = 'data/plot_tests.png'
		fig1     = plt.figure(num='Тестирование', dpi=100)

	center =  "+"+str(int(screen_width/2-640/2))
	center += "+"+str(int(screen_height/2-480/2))
	plt.get_current_fig_manager().window.wm_geometry(center)

	ax1 = fig1.add_subplot(1,1,1)
	def animate (i):
	    ax1.clear()
	    ax1.pie(i, explode=(0, 0.1), labels=labels, 
	    		   colors=['yellowgreen', 'lightcoral'], 
	    		   autopct='%1.1f%%', shadow=True, startangle=80)
	    ax1.axis('equal')
	    return ax1, 
	ani = animation.FuncAnimation(fig1, animate, sizes, interval=200, 
								  repeat=False, save_count=1)
	plt.pause(0.02*120)
	fig1.savefig(filename, transparent=True)
	plt.clf()
	plt.close()

def plot_data (data):
	def cc (arg):
		return mcolors.to_rgba(arg, alpha=0.6)

	fig    = plt.figure(num='Сигналы ЭМГ')
	center =  "+"+str(int(screen_width/2-640/2))
	center += "+"+str(int(screen_height/2-580/2))
	plt.get_current_fig_manager().window.wm_geometry(center)
	# 'TKAgg' backend
	mng   = plt.get_current_fig_manager()
	mng.resize(*mng.window.maxsize())
	ax     = fig.gca(projection='3d')
	xs     = np.arange(0, len(data[0]), 1)
	verts  = []
	zs     = np.arange(0, len(data), 1)
	for z in zs:
	    ys = data[z]
	    verts.append(list(zip(xs, ys)))

	cmap   = plt.get_cmap('rainbow') #viridis
	colors = cmap(np.linspace(0, 1, len(data)))
	poly   = PolyCollection(verts, facecolors=colors)
	poly.set_alpha(0.7)
	ax.add_collection3d(poly, zs=zs, zdir='y')
	ax.set_xlabel('X')
	ax.set_xlim3d(0, len(data[0]))
	ax.set_ylabel('samples')
	ax.set_ylim3d(0, len(data))
	ax.set_zlabel('Z')
	ax.set_zlim3d(np.min(data), np.max(data))
	fig.savefig('data/plot_data.png', transparent=True)
	plt.show()