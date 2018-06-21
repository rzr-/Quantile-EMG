#! /usr/bin/env python3.5
# -*- coding: utf-8 -*-
#pip3.5 install numpy scipy matplotlib scikit-learn pgi pytest
#gsettings set org.gtk.Settings.FileChooser window-size '(800,600)'

import svm_rbf              as s
import svm_plot             as p
import svm_data_acquisition as d
import pgi; pgi.require_version('Gtk', '3.0')
from   pgi.repository       import Gtk, Gdk, GObject, GdkPixbuf

screen               = Gdk.Screen.get_default()
p.screen_width       = screen.get_width()
p.screen_height      = screen.get_height()
p.main_window_width  = p.screen_width-450
p.main_window_height = p.screen_height-150

def set_image (obj, f, w, h):
	obj.set_from_pixbuf(
		GdkPixbuf.Pixbuf.new_from_file_at_scale(
				filename=f, width=w, height=h, 
				preserve_aspect_ratio=True))

def train (button): 
	all_data_plot.clear()
	test_signal_plot.clear()
	test_result_image.clear()
	results_label.set_text("")
	train_results  = s.train(d.X, d.y)*100
	p.sizes[10][0] = train_results
	p.sizes[10][1] = 100.-train_results

	p.plot_train_test("train")
	set_image(all_data_plot, "data/plot_train.png", 640, 480)

	run_tests_button.set_sensitive(True)
	run_random_test_button.set_sensitive(True)
	results_label.set_markup(
		"\n<big>Точность обучения: <b><span foreground='green'>" +
		"{:.2f}".format(train_results) + "%</span></b></big>")

def run_tests (button):
	all_data_plot.clear()
	test_signal_plot.clear()
	test_result_image.clear()
	results_label.set_text("")

	tests_results  = s.test(d.x_test, d.y_test)*100
	p.sizes[10][0] = tests_results
	p.sizes[10][1] = 100.-tests_results
	p.plot_train_test("test")

	set_image(all_data_plot, "data/plot_tests.png", 640, 480)
	results_label.set_markup(
		"\n<big>Правильно классифицированы <b><span foreground='green'>" +
		"{:.2f}".format(tests_results) + "%</span></b> сигналов</big>")

def run_random_test (button):
	all_data_plot.clear()
	test_signal_plot.clear()
	test_result_image.clear()
	results_label.set_text("")

	test_number = d.np.random.randint(low=0, high=len(d.x_test)-1)
	test        = d.x_test[test_number]
	test_class  = d.y_test[test_number]
	prediction  = s.pred([test])[0]

	# i = 0
	# while (test_class==prediction):
	# 	test = d.x_test[i]
	# 	test_class = d.y_test[i]
	# 	prediction = s.pred([test])[0]
	# 	i += 1

	p.plot_single(test)
	set_image(test_signal_plot, "data/plot_single.png", 590, 444)
	test_signal_plot.set_sensitive(True)

	if (test_class == prediction):
		results_label.set_markup(
			"\n<big>Класс сигнала: <b>" + 
			d.classes_strings[test_class] + 
			"</b>\n" + "Результат классификации: <b>" + 
			d.classes_strings[prediction] + "</b>\n" 
			"<b><span foreground='green'>Сигнал " + 
			"классифицирован правильно</span></b></big>")
		set_image(test_result_image, 
				   "data/gestures/"+str(test_class)+".png",
				   210, 180)
	else:
		results_label.set_markup(
			"\n<big>Класс сигнала: <b>" + 
			d.classes_strings[test_class] + 
			"</b>\n" + "Результат классификации: <b>" + 
			d.classes_strings[prediction] + "</b>\n" 
			"<b><span foreground='red'>Сигнал " + 
			"классифицирован неправильно</span></b></big>")
		set_image(test_result_image, 
				   "data/gestures/wrong.png", 210, 180)
	test_result_image.set_sensitive(True)

def plot (button):
	all_data_plot.clear()
	test_signal_plot.clear()
	test_result_image.clear()
	results_label.set_text("")
	p.plot_data(d.test_data)
	set_image(all_data_plot, "data/plot_data.png", 640, 480)

def choose_file (button):
	dialog = Gtk.FileChooserDialog(
				"Пожалуйста, выберите файл", win,
				Gtk.FileChooserAction.OPEN,
				(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
				Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

	train_button.set_sensitive(False)
	run_tests_button.set_sensitive(False)
	run_random_test_button.set_sensitive(False)
	plot_button.set_sensitive(False)
	param_input_grid.set_sensitive(False)
	c_entry.set_text("");     gamma_entry.set_text("")
	split_entry.set_text(""); classes_entry.set_text("")
	# config_combo.set_sensitive(False)
	results_label.set_text("")
	test_signal_plot.clear()
	test_result_image.clear()
	set_image(all_data_plot, "data/plot_data.png", 640, 480)

	response = dialog.run()
	if (response == Gtk.ResponseType.OK):
		d.data_file_location = dialog.get_filename()
		param_input_grid.set_sensitive(True)
		# config_combo.set_sensitive(True)
	dialog.destroy()

# def on_config_combo_changed (combo):
# 	c = combo.get_active_text()
# 	if c is not None:
# 		c_entry.set_text(str(configs[c][0])) 
# 		gamma_entry.set_text(str(configs[c][1]))
# 		split_entry.set_text(str(configs[c][2]))
# 		classes_entry.set_text(str(configs[c][3]))
# 		set_parameters(combo)

def set_parameters (button):
	if (c_entry.get_text_length()       == 0 and \
		gamma_entry.get_text_length()   == 0 and \
		split_entry.get_text_length()   == 0 and \
		classes_entry.get_text_length() == 0):
			c_entry.set_text("3")
			gamma_entry.set_text("0.02")
			split_entry.set_text("0.35")
			classes_entry.set_text("0,1,4,5,6")
	msg_dialog = Gtk.MessageDialog(
					win, 0, Gtk.MessageType.INFO,
					Gtk.ButtonsType.OK, 
					"Параметры RBF должны соответствовать " +
					"следующим ограничениям:\n\tC > 0\n\t" +
					"0 < gamma < 1\n\t0 < split < 1\n\t" +
					"Классы: от 0 до 9 через \",\"")
	test_signal_plot.clear()
	test_result_image.clear()
	set_image(all_data_plot, "data/plot_data.png", 640, 480)

	def verify_classes_entry(c):
		try:
			d.classes = [int(x) for x in c.split(",")]
		except:
			return False
		for i in d.classes:
			if i > 9 or i < 0:
				return False
		return True

	try:
		d.c     = float(c_entry.get_text()) 
		d.gamma = float(gamma_entry.get_text())
		d.split = float(split_entry.get_text())

		if (d.split > 0. and d.split < 1.\
			and d.gamma > 0. and d.gamma < 1. and d.c > 0. \
			and verify_classes_entry(classes_entry.get_text())):
			
			is_data_processed = d.init_data_acquisition()
			if (is_data_processed == True):
				train_button.set_sensitive(True)
				plot_button.set_sensitive(True)
				run_tests_button.set_sensitive(False)
				run_random_test_button.set_sensitive(False)
				results_label.set_text("")
				s.init_model (d.c, d.gamma)
			elif (is_data_processed == "data_not_organised"):
				train_button.set_sensitive(False)
				run_tests_button.set_sensitive(False)
				run_random_test_button.set_sensitive(False)
				plot_button.set_sensitive(False)
				param_input_grid.set_sensitive(False)
				# config_combo.set_sensitive(False)
				results_label.set_text("")
				set_image(all_data_plot, "data/plot_data.png", 640, 480)

				msg_dialog = Gtk.MessageDialog(
								win, 0, Gtk.MessageType.INFO,
								Gtk.ButtonsType.OK, 
								"Данные в файле организованы неправильно")
				msg_dialog.run()
				msg_dialog.destroy()
		else:
			train_button.set_sensitive(False)
			plot_button.set_sensitive(False)
			run_tests_button.set_sensitive(False)
			run_random_test_button.set_sensitive(False)
			results_label.set_text("")
			msg_dialog.run()
			msg_dialog.destroy()

	except ValueError:
		msg_dialog.run()
		msg_dialog.destroy()

win = Gtk.Window()
win.set_position(Gtk.WindowPosition.CENTER)
win.set_title("Классификация сигналов ЭМГ")		
win.set_default_size(p.main_window_width, p.main_window_height)
win.timeout_id = None
win.connect("delete-event", Gtk.main_quit)

file_chooser_button = Gtk.Button("Выбрать файл")
file_chooser_button.connect("clicked", choose_file)

# configs = {'100% - 0,1,3':      [1, 0.07, 0.47, "0,1,3"],	
# 		   '94.94% - 0,1,4,5,6':[2, 0.02, 0.35, "0,1,4,5,6"],
# 		   '96.50% - 0,1,3,4,5':[2, 0.04, 0.64, "0,1,3,4,5"]}
# config_combo = Gtk.ComboBoxText()
# config_combo.set_entry_text_column(0)
# config_combo.connect("changed", on_config_combo_changed)
# for key, value in configs.items():
# 	config_combo.append_text(str(key))
# config_combo.set_sensitive(False)

c_label       = Gtk.Label(label="C: ");       c_label.set_alignment(0, 0.5)
gamma_label   = Gtk.Label(label="Gamma: ");   gamma_label.set_alignment(0, 0.5)
split_label   = Gtk.Label(label="Split: ");   split_label.set_alignment(0, 0.5)
classes_label = Gtk.Label(label="Classes: "); split_label.set_alignment(0, 0.5)
c_entry       = Gtk.Entry(); c_entry.set_placeholder_text("C")
gamma_entry   = Gtk.Entry(); gamma_entry.set_placeholder_text("Gamma")
split_entry   = Gtk.Entry(); split_entry.set_placeholder_text("Split")
classes_entry = Gtk.Entry(); classes_entry.set_placeholder_text("Classes")

c_entry.set_width_chars (10);
gamma_entry.set_width_chars (10);
split_entry.set_width_chars (10);
classes_entry.set_width_chars (10);

set_parameters_button = Gtk.Button(label="Установить параметры")
set_parameters_button.connect("clicked", set_parameters)

param_input_grid = Gtk.Grid(column_homogeneous=True, 
							column_spacing=10,
							row_spacing=5)
param_input_grid.set_sensitive(False)
param_input_grid.attach(c_entry, 0, 0, 1, 1) #col, row, width, height
param_input_grid.attach(gamma_entry, 1, 0, 1, 1)
param_input_grid.attach(split_entry, 0, 1, 1, 1)
param_input_grid.attach(classes_entry, 1, 1, 1, 1)
param_input_grid.attach(set_parameters_button, 0, 2, 2, 1)

train_button = Gtk.Button.new_with_label("Oбучить классификатор")	
train_button.connect("clicked", train)
train_button.set_size_request(150,75)
train_button.set_sensitive(False)

run_tests_button = Gtk.Button.new_with_label(
							"Тестировать классификатор на\n" +
							"испытательном наборе данных")
run_tests_button.connect("clicked", run_tests)
run_tests_button.set_size_request(150,75)
run_tests_button.set_sensitive(False)

run_random_test_button = Gtk.Button.new_with_label(
							"Тестировать на случайном сигнале\n" +
							"из испытательного набора данных")
run_random_test_button.connect("clicked", run_random_test)
run_random_test_button.set_size_request(150,75)
run_random_test_button.set_sensitive(False)

results_label = Gtk.Label()
results_label.set_justify(Gtk.Justification.LEFT)

plot_button = Gtk.Button.new_with_label("Показать данные")
plot_button.connect("clicked", plot)
plot_button.set_sensitive(False)

test_signal_plot  = Gtk.Image()
test_signal_plot.set_sensitive(False)
test_result_image = Gtk.Image()
test_result_image.set_sensitive(False)

all_data_plot = Gtk.Image()
set_image(all_data_plot, "data/plot_data.png", 640, 480)

# vbox1  = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
# vbox1.pack_start(file_chooser_button, True, True, 0)
# vbox1.pack_start(config_combo, True, True, 0)

hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
hbox1.pack_start(file_chooser_button, True, False, 0)
# hbox1.pack_start(vbox1, False, False, 0)
hbox1.pack_start(param_input_grid, False, False, 2)
hbox1.pack_start(train_button, True, False, 1) # expand, fil, padding
hbox1.pack_start(run_tests_button, True, False, 1)
hbox1.pack_start(run_random_test_button, True, False, 1)

hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
hbox2.pack_start(test_signal_plot, False, False, 0)
hbox2.pack_start(test_result_image, True, True, 0)

vbox  = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
vbox.pack_start(hbox1, False, False, 0)
vbox.pack_start(results_label, True, False, 0)
vbox.pack_start(hbox2, False, False, 2)
vbox.pack_start(all_data_plot, False, False, 0)
vbox.pack_end(plot_button, False, False, 0)

win.add(vbox)  
win.show_all()
Gtk.main()
