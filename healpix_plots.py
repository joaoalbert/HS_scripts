# -*- coding: cp1252 -*-

'''
Created on 14/07/2020
Last update 07/2022

Author: João Alberto, Carlos Otobone
'''

import healpy as hp 
import matplotlib.pyplot as plt 
import numpy as np
import os
import astropy.io.fits as pyfits


def healpix_plot(map_file, fig_name, title, channel=0, unit =r'Temperature (mK)', mini=None, maxi=None):
	'''
	Takes a FITS file containing a sky cube and plots the map in the corresponding channel
	in a Mollweide projection and Gnomonic projection (zoom).
	
	map_file: str, FITS file.
	fig_name: str, name of the file for the PNG figure to be saved.
	title: str, title to appear on top of the map.
	channel: int, frequency channel to be plotted.
	unit: str, map unit to appear on the colorbar.
	
	Optional:
	mini: float, minimum range value.
	maxi: float, maximum range value.
	'''

	destination_path = "/".join(fig_name.split("/")[:-1]+[""])
	os.system("mkdir -p " + destination_path + "/")
	
	print("Collecting healpix data from {}...".format(map_file))
	maps = pyfits.getdata(map_file) 
	
	if mini == None and maxi == None: 
		hp.mollview(maps[channel], title=title, unit=unit, cmap='jet')  
	else: 
		hp.mollview(maps[channel], title=title, unit=unit, cmap='jet', min=mini, max=maxi)
	plt.savefig(fig_name)
	plt.close()
	
	hp.gnomview(maps[channel], title= title + " (zoom)", rot= (0,-17),reso= 5, xsize= 400, ysize= 200)
	plt.savefig(destination_path + title + "_zoom.png")
	plt.close()
	
	
	
def add_maps(map_list, final_fits):
	'''
	Takes a list of maps, adds them together and writes to a FITS file.
	All of the files must contain the same number of channels.
	
	map_list: list of str, contains the name of all the FITS files to be added.
	final_fits: str, name of the final FITS to be written 
	'''
	
	added_map = pyfits.getdata(map_list[0])
	
	print("Verifying Nside and Nchannels and adding maps...")
	for i in range(1,len(map_list)):
		map_i = pyfits.getdata(map_list[i])
		assert added_map.shape==map_i.shape
		added_map+=map_i

	destination_path = "/".join(final_fits.split("/")[:-1]+[""])
	os.system("mkdir -p " + destination_path )
	pyfits.writeto(final_fits, added_map)
	print("FITS files successfully written to {}".format(final_fits))



def h5_map_plot(path, map_file, title, channel=0):
	'''
	Plots a Healpix map from a HDF5 file.
	'''
	import h5py

	print("Making directory map_plots...")
	os.system('mkdir -p ' + path + 'map_plots/')
	
	print("Opening file ", map_file)
	fp = h5py.File(path + map_file, 'r')	
	mapa = fp['MAPS'][()]
	counts = fp['COUNTS'][()]
	fp.close()

	mapa[counts==0] = hp.UNSEEN

	plt.figure(0)
	hp.mollview(mapa[channel, 0, :], cmap="jet")
	plt.title(title)
	plt.savefig(path + "map_plots/" + title + ".png")
	plt.close()
		
	hp.gnomview(mapa[channel, 0, :], title= title + " (zoom)", unit="(K)", rot=(0,-17), cmap='jet', reso=5, xsize=400, ysize=200)
	#plt.show()
	plt.savefig(path + "map_plots/" + title + "_zoom.png")
	plt.close()




def combine_h5_horn_maps(path, map_file_format, title, horns, file_name=None, channel=0):
	'''
	This function takes individual maps from BINGO horns and generates one map which is the
	mean of the pixels weighted by its respective hits from each map. 
	'''
	
	import h5py

	print("Making directory map_plots...")
	os.system('mkdir -p ' + path + 'map_plots/')
	
	fp = h5py.File(path + map_file_format.format(0), 'r')
	mapa = fp['MAPS'][()]
	counts = fp['COUNTS'][()]
	fp.close()

	# Generating map
	maps = np.zeros(mapa[:,0,:].shape)
	counts_total = np.zeros(counts[0,0,:].shape)

	# Reading files
	for i in range(horns):
		print("Collecting data from horn {}".format(i))
		fp = h5py.File(path+map_file_format.format(i), 'r')
		mapa = fp['MAPS'][()]
		counts = fp['COUNTS'][()]
		fp.close()
		maps += mapa[:,0,:]
		counts_total += counts[0,0,:]
	
	#print(counts_total.shape)
	mask = np.where(counts_total==0, 1, counts_total)
	maps[channel, :][counts_total==0] = hp.UNSEEN

	# Creating the map file
	if file_name==None: file_name=title
	print("Generating file " + file_name + ".hdf")
	h5f = h5py.File(path + file_name + ".hdf", 'w')
	h5f.create_dataset('MAPS', data=maps)
	h5f.create_dataset('COUNTS', data=np.array([[counts_total, counts_total]]))
	h5f.close()
	
	# Plotting mollview and gnomview
	print("Plotando imagem do canal " + str(channel))
	plt.figure(0)
	hp.mollview(maps[channel, :], cmap="jet", title=title, unit="Temperature (K)")#, min=-0.02, max=10)
	plt.savefig(path + "map_plots/" + file_name + ".png")
	plt.close()
	
	hp.gnomview(maps[channel, :], title=title+" (zoom)", unit="(K)", rot=(0,-17), cmap='jet', reso=5, xsize=400, ysize=200)#, min=-0.06, max=0.06)
	plt.savefig(path + "map_plots/" + file_name + "_zoom.png")
	plt.close()
	
	return True
		
		
		
def residuals(map_path_1, map_path_2, title, figure_name, channel=0, rel=False):
	'''
	This funciton takes a general map (map1) and calculates
	its residuals given a reference map (map2).
	This excludes pixels with hp.UNSEEN.
	
	res = map_1 - map_2
	
	Picture is saved on the same path as map_1.
	
	The channel refers only to the plot.
	'''
	
	import h5py
	import astropy.io.fits as pyfits
	import numpy as np
	import matplotlib.pyplot as plt
	import healpy as hp
	
	
	type1 = map_path_1.split(".")[-1]
	type2 = map_path_2.split(".")[-1]
	
	if type1=="hdf":		map_1 = h5py.File(map_path_1, "r")["MAPS"][()][channel]
	elif type1=="fits": 	map_1 = pyfits.getdata(map_path_1)[channel]
	else: print("Invalid type: "+type1)
	
	if type2=="hdf":		map_2 = h5py.File(map_path_2, "r")["MAPS"][()][channel]
	elif type2=="fits":		map_2 = pyfits.getdata(map_path_2)[channel]
	else: print("Invalid type: "+type2)

	
	if rel: 
		residuals = (map_1 - map_2)/map_1
		label_unit = "Rel. Difference (%)"
		unit = "(%)"#"(K)"
	else: 
		residuals = (map_1 - map_2)
		label_unit = "Temp. Difference (K)"
		unit = "(K)"
	residuals[map_1==hp.UNSEEN] = hp.UNSEEN
	residuals[map_2==hp.UNSEEN] = hp.UNSEEN
	
	
	path = map_path_1[:len(map_path_1)-map_path_1[::-1].find("/")]
			
	hp.mollview(residuals, cmap="jet", unit=label_unit, title=title)#, max=1,min=-1)
	plt.savefig(path+figure_name+".png")
	plt.close()
	
	hp.gnomview(residuals, title=title+" (zoom)", unit=unit, rot=(0,-17), cmap='jet', reso=5, xsize=400, ysize=200)#, max=1,min=-1)
	plt.savefig(path+figure_name+"_zoom.png")
	plt.close()
		
	return True
	
		

if __name__=="__main__":

	if True:
	
		file_fmt = "bingo_maps_horn_{}.hdf"
		file_name = "bingo_maps_28_horns"
		
		file_path = "/home/joao/Documentos/cosmologia/hide_and_seek/resultados/healpix/gaussian/ame_128/ame_128_5days/"
		title = "AME - Gaussian Beam (2d)"
		
		combine_h5_horn_maps(file_path, file_fmt, title, 28, file_name)
		
		new_map = file_path + "bingo_maps_28_horns.hdf"
		orig_map = "/home/joao/Documentos/cosmologia/hide_and_seek/hide-master/hide/data/sky/ame_cube_hs_test_rot_kelvin.fits"
		title = "AME (2d) - Absolute Residuals"
		figure_name = "ame_5days_abs_residuals"
		residuals(new_map, orig_map, title, figure_name, rel=False)
		
		title = "AME (2d) - Relative Residuals"
		figure_name = "ame_5days_rel_residuals"
		residuals(new_map, orig_map, title, figure_name, rel=True)



	if False:
	
		displacements = ["-2d", "2d", "2d_10days"]
		mapmakings = ["filter_mapper"]
		
		std_maps = ["/home/joaoalb/Documents/Cosmologia/hide_and_seek/hide-master/hide/data/sky/free_free_cube_hs_test_rot_kelvin.fits",
					"/home/joaoalb/Documents/Cosmologia/hide_and_seek/resultados/healpix_seek/K/noiseless/FreeFree/simple_mapper/{}/bingo_maps_28_horns_convolved_beam.hdf"]
	
		map_path = "/home/joaoalb/Documents/Cosmologia/hide_and_seek/resultados/healpix_seek/K/1f_noise/FreeFree/Tsys_70_alpha_1_fknee_0_001/{}/{}/"
		
		title = "Residuals - Beam-Convolved Map Subtracted"
		figure_name = "residuals_noise"
		
		import os
		
		for mm in mapmakings:
			for d in displacements:
				path = map_path.format(mm,d)
				map_file = path + [ arq for arq in os.listdir(path) if "bingo_maps_horn" not in arq and arq.split(".")[-1]=="hdf" ][0]
				residuals(map_file, std_maps[1].format(d), title, figure_name)
		
		
