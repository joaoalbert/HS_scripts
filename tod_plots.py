# -*- coding: cp1252 -*-
'''
Created on 07/2020
Last update 07/2022

Author: Carlos Otobone, João Alberto
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as trans
import os
import h5py


TOD_FILE_FORMAT = 'bingo_tod_horn_{horn}_{yyyy}{mm}{dd}_{{hh:02d}}0000.h5'


def collect_tod_data(path_time_fmt, hi=0, hf=23):
	
	tods_matrix = np.array([])
	times_matrix = np.array([])
	print("Collecting data from {} TODs...".format(hf-hi))
	for hh in range(hi,hf+1):
		arx = path_time_fmt.format(hh=hh)
		with h5py.File(arx, "r" ) as tod_file:
			tods = tod_file["P/Phase1"][()]
			times = tod_file["TIME"][()]
		tods_matrix = np.hstack((tods_matrix,tods)) if tods_matrix.size else tods
		times_matrix = np.hstack((times_matrix,times)) if times_matrix.size else times
	
	return tods_matrix, times_matrix


def date_split(date):

	year = date.split()[0].split('-')[0]
	month = date.split()[0].split('-')[1]
	day = date.split()[0].split('-')[2]
	
	return year, month, day


def plot_tod(tods_path, date, horn, hi=0, hf=23,title=None): 
	'''
	Generates the plot for a TOD from hourly divided files, 
	which names must follow the format:
	'bingo_tod_horn_{HORN}_{YEAR}{MONTH}{DAY}_{HOUR}0000.h5'
	
	tods_path: TODs path (only the paths).
	date: date in format 'yyyy-mm-dd'.
	horns: horns quantity.
	'''
	
	year, month, day = date_split(date)
	path = os.path.join(tods_path, year, month, day)
		
	file_time_fmt = TOD_FILE_FORMAT.format(horn=horn, yyyy=year, mm=month, dd=day)
	path_time_fmt = os.path.join(path, file_time_fmt)
	tods_matrix, times_matrix = collect_tod_data(path_time_fmt, hi, hf)

	print("Creating directory tod_plots...")
	os.system('mkdir -p ' + path + 'tod_plots/')
	
	print ("Generating horn image --> " + str(horn))
	title = "Horn " + str(horn) + " " + year + "/" + month + "/" + day if title==None else title
	plt.imshow(tods_matrix, aspect="auto", origin="lower", extent=(hi,hf, 980, 1260))
	plt.title(title)
	plt.xlabel("Time (h)")
	plt.ylabel("Frequency (MHz)")	   
	plt.colorbar(label="Temperature (K)")
	plt.savefig(path + "tod_plots/" + '24_bingo_tod_horn_' + str(horn) + '_' + year + month + day + ".png")
	plt.close()
	


def plot_channel(tods_path, date, horn, channel=0, hi=0, hf=24, title=None):
	'''
	Generates the plot for a specific frequency channel from hourly divided files, 
	which names must follow the format:
	'bingo_tod_horn_{HORN}_{YEAR}{MONTH}{DAY}_{HOUR}0000.h5'
	
	tods_path: TODs path (only the paths).
	date: date in format 'yyyy-mm-dd'.
	horns: horns quantity.
	'''
	
	year, month, day = date_split(date)
	path = os.path.join(tods_path, year, month, day)
	
	file_time_fmt = TOD_FILE_FORMAT.format(horn=horn, yyyy=year, mm=month, dd=day)
	path_time_fmt = os.path.join(path, file_time_fmt)
	tods_matrix, times_matrix = collect_tod_data(path_time_fmt, hi, hf)	

	print("Creating directory tod_plots...")
	os.system('mkdir -p ' + path + 'tod_plots/')
	title = "Horn {horn} Channel {channel} {year}/{month}/{day}".format(horn=horn,
																		channel=channel,
																		year=year,
																		month=month,
																		day=day) \
															if title==None else title
	
	temp_plot = True
	db_plot = False
	print ("Generating horn image --> " + str(horn))
	figname = os.path.join(path, "tod_plots/", '24_bingo_tod_horn_{}_channel_{}_{}{}{}.png'.format(horn, channel, year, month, day))
	if temp_plot:
		seconds = np.linspace(hi,hf,len(tods_matrix[channel]))
		plt.plot(seconds, tods_matrix[channel])
		plt.title(title)
		plt.xlabel("Time (h)")
		#plt.xlim(5.1,5.5)
		plt.ylabel("Temperature (K)")
		plt.savefig(figname)
		plt.close()
		
	if db_plot:
		seconds = np.linspace(hi,hf,len(tods_matrix[channel]))
		plt.plot(seconds, 20*np.log10(abs(tods_matrix[channel])))
		plt.title(title)
		plt.xlabel("Time (h)")
		#plt.xlim(5.1,5.5)
		plt.ylabel("Amplitude (dB)")
		plt.savefig(figname)
		plt.close()


def plot_diff(tod_path_1, tod_path_2, date, horn, output_file, title, hi=0, hf=23):
	'''
	Plots the difference between two TODs for a specific date.
	'''
	
	year, month, day = date_split(date)
	path1 = tod_path_1 + year + "/" + month + "/" + day + "/"
	path2 = tod_path_2 + year + "/" + month + "/" + day + "/"
	
	file_time_fmt = TOD_FILE_FORMAT.format(horn=horn, yyyy=year, mm=month, dd=day)
	#file_time_fmt2 = TOD_FILE_FORMAT.format(horn=horn, yyyy=year, mm=month, dd=day)
	
	path_time_fmt1 = os.path.join(path1, file_time_fmt)
	tods_matrix1, times_matrix1 = collect_tod_data(path_time_fmt1, hi, hf)

	path_time_fmt2 = os.path.join(path, file_time_fmt)
	tods_matrix2, times_matrix2 = collect_tod_data(path_time_fmt2, hi, hf)
	
	tod_diff = tods_matrix1 - tods_matrix2
	
	print ("Generating image...")
	plt.imshow(tod_diff, aspect="auto", origin="lower", extent=(0,24 ,980, 1260))
	plt.title(title)
	plt.xlabel("Time (h)")
	plt.ylabel("Frequency (MHz)")	   
	plt.colorbar(label="Temperature (K)")
	plt.savefig(output_file)
	plt.close()


if __name__=="__main__":


	date = '2018-01-01'
	horn = 0
	
	tod_path = "/scratch/bingo/joao.barretos/hide_and_seek/resultados/TOD/teste/"
	plot_tod(tod_path, date, horn)
	#plot_channel(tod_path, date, horn, hi=5,hf=6)
	

	
