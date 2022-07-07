# -*- coding: cp1252 -*-
'''
Created on 13/07/2020
Last update 22/02/2022

Author: Carlos Otobone, João Alberto
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as trans
import os
import h5py



def plot_tod(w_path, date, horn, ti=0, tf=24,title=None): 
	'''
	Generates the plot for a TOD from hourly divided files, 
	which names must follow the format:
	'bingo_tod_horn_{HORN}_{YEAR}{MONTH}{DAY}_{HOUR}0000.h5'
	
	w_path: TODs path (only the paths).
	date: date in format 'yyyy-mm-dd'.
	horns: horns quantity.
	'''
	
	tods_matrix = []
	times_matrix = []
	tods = []
	times = []
	
	year = date.split()[0].split('-')[0]
	month = date.split()[0].split('-')[1]
	day = date.split()[0].split('-')[2]
	path = w_path + year + "/" + month + "/" + day + "/"
		
	print("Collecting data from all TODs...")
	for i in range(tf-ti):
		t = ti+i
		arx = 'bingo_tod_horn_' + str(horn) + '_' + year + month + day + '_{:02d}0000.h5'.format(t)				  
		tod_file = h5py.File( path + arx, "r" )  
		tods.append(tod_file["P/Phase1"][()])
		times.append(tod_file["TIME"][()])
		tod_file.close()
		tods_matrix.append(tods)
		times_matrix.append(times)
	
	# Concatanating TODs
	conc_tods = tods_matrix[horn][0]
	for i in range(1,tf-ti):
		tod = tods_matrix[horn][i]
		conc_tods = np.concatenate((conc_tods,tod), axis = 1)

	print("Creating directory tod_plots...")
	os.system('mkdir -p ' + path + 'tod_plots/')
	
	print ("Generating horn image --> " + str(horn))
	if title==None: title = "Horn " + str(horn) + " " + year + "/" + month + "/" + day
	plt.imshow(conc_tods, aspect="auto", origin="lower", extent=(ti,tf,980,981))#,980, 1260))
	plt.title(title)
	plt.xlabel("Time (h)")
	plt.ylabel("Frequency (MHz)")	   
	plt.colorbar(label="Temperature (K)")
	plt.savefig(path + "tod_plots/" + '24_bingo_tod_horn_' + str(horn) + '_' + year + month + day + ".png")
	plt.close()
	


def plot_channel(w_path, date, horn, channel=0, ti=0, tf=24, title=None):
	'''
	Generates the plot for a specific frequency channel from hourly divided files, 
	which names must follow the format:
	'bingo_tod_horn_{HORN}_{YEAR}{MONTH}{DAY}_{HOUR}0000.h5'
	
	w_path: TODs path (only the paths).
	date: date in format 'yyyy-mm-dd'.
	horns: horns quantity.
	'''
	
	mini = []
	maxi = []
	tods_matrix = []
	times_matrix = []
	tods = []
	times = []
	
	year = date.split()[0].split('-')[0]
	month = date.split()[0].split('-')[1]
	day = date.split()[0].split('-')[2]
	path = w_path + year + "/" + month + "/" + day + "/"
		
	print("Collecting data from all TODs...")
	for i in range(tf-ti):
		t = ti+i
		arx = 'bingo_tod_horn_' + str(horn) + '_' + year + month + day + '_{:02d}0000.h5'.format(t)				  
		tod_file = h5py.File( path + arx, "r" )  
		tods.append(tod_file["P/Phase1"][()])
		times.append(tod_file["TIME"][()])
		tod_file.close()
		mini.append(np.min(tods[i]))		
		maxi.append(np.max(tods[i]))
		tods_matrix.append(tods)
		times_matrix.append(times)
		
	mini = np.min(mini)
	maxi = np.max(maxi)			
	
	# Concatanating TODs
	conc_tods = tods_matrix[0][0]
	for i in range(tf-ti-1):
		tod = tods_matrix[0][i+1]
		conc_tods = np.concatenate((conc_tods,tod), axis = 1)

	print("Creating directory tod_plots...")
	os.system('mkdir -p ' + path + 'tod_plots/')
	if title==None: 
		title = ("Horn " + str(horn) + " Channel " + str(channel) + " " + 
				 year + "/" + month + "/" + day)
	
	temp_plot = True
	db_plot = False
	print ("Generating horn image --> " + str(horn))
	if temp_plot:
		plt.plot(np.linspace(ti,tf,len(conc_tods[channel])), 
				 conc_tods[channel])
		plt.title(title)
		plt.xlabel("Time (h)")
		plt.xlim(5.1,5.5)
		plt.ylabel("Temperature (K)")
		plt.savefig(path + "tod_plots/" + '24_bingo_tod_horn_' + str(horn) + 
					'_channel_' + str(channel) + '_' + year + month + day + ".png")
		plt.close()
		
	if db_plot:
		plt.plot(np.linspace(ti,tf,len(conc_tods[channel])),
				 20*np.log10(abs(conc_tods[channel])))
		plt.title(title)
		plt.xlabel("Time (h)")
		plt.xlim(5.1,5.5)
		plt.ylabel("Amplitude (dB)")
		plt.savefig(path + "tod_plots/" + '24_bingo_tod_amplitude_horn_' + str(horn) + 
					'_channel_' + str(channel) + '_' + year + month + day + ".png")
		plt.close()


def plot_diff(tod_path_1, tod_path_2, date, horn, output_file, title):
	'''
	Plots the difference between two TODs for a specific date.
	'''
	year = date.split()[0].split('-')[0]
	month = date.split()[0].split('-')[1]
	day = date.split()[0].split('-')[2]
	path1 = tod_path_1 + year + "/" + month + "/" + day + "/"
	path2 = tod_path_2 + year + "/" + month + "/" + day + "/"
	
	tods_matrix = []
	times_matrix = []
	tods = []
	times = []
	print("Collecting data from all TODs...")
	for i in range(24):
		arx = 'bingo_tod_horn_' + str(horn) + '_' + year + month + day + '_{:02d}0000.h5'.format(i)
		with h5py.File(path1 + arx, "r" ) as tod_file:			
			tods.append(tod_file["P/Phase1"][()])
			times.append(tod_file["TIME"][()])
		tods_matrix.append(tods)
		times_matrix.append(times)
		
	tod_1 = tods_matrix[horn][0]
	for i in range(23):
		tod = tods_matrix[horn][i+1]
		tod_1 = np.concatenate((tod_1,tod), axis=1)
		
	tods_matrix = []
	times_matrix = []
	tods = []
	times = []
	for i in range(24):
		arx = 'bingo_tod_horn_' + str(horn) + '_' + year + month + day + '_{:02d}0000.h5'.format(i)
		with h5py.File(path2 + arx, "r" ) as tod_file:			
			tods.append(tod_file["P/Phase1"][()])
			times.append(tod_file["TIME"][()])
		tods_matrix.append(tods)
		times_matrix.append(times)  
			  
	tod_2 = tods_matrix[horn][0]
	for i in range(23):
		tod = tods_matrix[horn][i+1]
		tod_2= np.concatenate((tod_2,tod), axis=1)
	
	tod_diff = tod_1 - tod_2
	
	print ("Generating image...")
	plt.imshow(tod_diff, aspect="auto", origin="lower", extent=(0,24 ,980, 1260))
	plt.title(title)
	plt.xlabel("Time (h)")
	plt.ylabel("Frequency (MHz)")	   
	plt.colorbar(label="Temperature (K)")
	plt.savefig(output_file)
	plt.close()


def plotdisp(txt_path, perfil, displacement, d_path=None):
	'''
	Recebe um txt com o numero da corneta, o RA e a DEC,
	e plota a disposição para um displacement especifico.
	(Não tem a ver com TOD.)
	
	txt_path: diretorio com o txt.
	perfil: "hexagonal", "rectangular", "drectangular".
	displacement: -2, -1, 0, 1, 2.
	d_path: destination path.
	'''
	
	if d_path==None: d_path = txt_path
	
	print ("Coletando RA (deg) e DEC (deg)...")
	lines = np.loadtxt(txt_path + perfil + '.txt')
	lines = lines[lines[:,0].argsort()] # Organizando por numero da corneta
	
	RA = []
	DEC = []
	NUMBER = []	
	
	if (perfil == 'hexagonal'):
		displacement = 0 
		for line in lines:
			RA.append(line[1])
			DEC.append(line[2])
			NUMBER.append(line[0])
	   
	else:
		resto = ((displacement + 3) % 5)
		for line in lines:
			if (line[0] % 5 == resto):
				RA.append(line[1])
				DEC.append(line[2])
				NUMBER.append(line[0] // 5 + 1)
							
	print("Plotando gráfico...")			
	fig, ax = plt.subplots() 
	ax.scatter(RA, DEC, s=1000)

	for i in range (len(NUMBER)):
		ax.annotate(int(NUMBER[i]), (RA[i], DEC[i]))
	
	
	if (perfil == 'hexagonal'):
	
		plt.title(perfil.title())
		plt.xlabel('RA (deg)')
		plt.ylabel('DEC (deg)')
		plt.savefig(d_path + perfil + '.png')

	elif (perfil == 'rectangular'):
	
		plt.title(perfil.title() + ' ' + str(displacement) + 'd')
		plt.xlabel('RA (deg)')
		plt.ylabel('DEC (deg)')
		plt.savefig(d_path + perfil + str(displacement) + 'd.png')

	else:
	
		plt.title("Double Rectangular " + str(displacement) + 'd')
		plt.xlabel('RA (deg)')
		plt.ylabel('DEC (deg)')
		plt.savefig(d_path + perfil + str(displacement) + 'd.png')


if __name__=="__main__":


	# l = ['hexagonal', 'drectangular', 'rectangular']
	# for elements in l:

	#	 if (elements == 'hexagonal'):
	#		 plotdisp("/home/otobone/Documentos/ic/projeto_karin/exercicios/optical/", 'hexagonal', 0)
	#	 else:
	#		 for d in range(-2,3):
				# plotdisp("/home/otobone/Documentos/ic/projeto_karin/exercicios/optical/", elements, d)
				
	#plotdisp("/home/joaoalb/Documents/Cosmologia/hide_and_seek/resultados/TOD/optical/", "rectangular", -2, "/home/joaoalb/Documents/Cosmologia/hide_and_seek/resultados/")


	date = '2018-01-01'
	horn = 0
	
	tod_path = '/home/joao/Documentos/cosmologia/hide_and_seek/resultados/TOD/normalization_tests/nside512/zernike_cubic_cut/'
	#plot_channel(tod_path, date, horn, ti=5,tf=6)
	
	paths = ["/home/joao/Documentos/cosmologia/hide_and_seek/resultados/TOD/normalization_tests/nside{}/gaussian_cut_norm/",
			 "/home/joao/Documentos/cosmologia/hide_and_seek/resultados/TOD/normalization_tests/nside{}/gaussian_cut_not_norm/",
			 "/home/joao/Documentos/cosmologia/hide_and_seek/resultados/TOD/normalization_tests/nside{}/zernike_cubic_cut/",
			 "/home/joao/Documentos/cosmologia/hide_and_seek/resultados/TOD/normalization_tests/nside{}/zernike_linear_cut/",
			 "/home/joao/Documentos/cosmologia/hide_and_seek/resultados/TOD/normalization_tests/nside{}/zernike_nearest_cut/"]
	for tod_path in paths:
		plot_tod(tod_path.format(256), date, horn, ti=5, tf=6)
		plot_channel(tod_path.format(256), date, horn, ti=5, tf=6)

#	path1 = "/home/joao/Documentos/cosmologia/hide_and_seek/resultados/TOD/ame_zernike/zernike_30_MINUS304_nside512_nearest/"
#	path2 = "/home/joao/Documentos/cosmologia/hide_and_seek/resultados/TOD/ame_zernike/gaussian_512/"
#	date = "2018-01-01"
#	horn = 0
#	output_file = "/home/joao/Documentos/cosmologia/hide_and_seek/resultados/TOD/ame_zernike/tod_sym_beam_gaussian_difference.png"
#	title = "(30, -304) - Gauss , nside512, nearest"
#	
#	plot_diff(path1, path2, date, horn, output_file, title)
	
