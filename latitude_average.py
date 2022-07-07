# -*- coding: cp1252 -*-
'''
Author: João Alberto

Created on: October, 2021
Updated on:
'''

import healpy as hp
import numpy as np
import matplotlib.pyplot as plt
import h5py



def lat_average(mapa, channel=0):
	'''
	Takes the average from each stripe (pixels with
	the same latitude) of a map.
	'''

	mapa = mapa[channel]
	mapa = np.where(mapa!=hp.UNSEEN, mapa, 0)
	npix = len(mapa)

	averages = [mapa[0]]
	thetas = hp.pix2ang(128,np.arange(npix))[0]

	last_pix = 0 # last pixel in the previous stripe
	nrows = 1


	for i in range(1,len(mapa)):

		if thetas[i]!=thetas[i-1]:
		
			averages[nrows-1] /= i-last_pix
			averages.append(mapa[i])
			
			last_pix = i
			nrows+=1
			
		else: averages[nrows-1]+=mapa[i]

	averages[-1] /= i-last_pix+1
	
	# optional: rad to degrees (-90,90)
	latitudes = np.degrees(np.unique(thetas)) - 90

	return averages, latitudes
	
	
	
if __name__=="__main__":
	
	
	# Estrutura geral das listas: [ [(-2d 1), (-2d 2), ...],
	#								[( 2d 1), ( 2d 2), ...]]
	
	
	file_paths = [["/home/joaoalb/Documents/Cosmologia/hide_and_seek/resultados/healpix_seek/K/1f_noise/FreeFree/Tsys_70_alpha_1_fknee_0_001/simple_mapper/variance/-2d/bingo_maps_28_horns_-2d_simple_mapper.hdf",
				   "/home/joaoalb/Documents/Cosmologia/hide_and_seek/resultados/healpix_seek/K/1f_noise/FreeFree/Tsys_70_alpha_1_fknee_0_001/simple_mapper/variance/2d/bingo_maps_28_horns_2d_simple_mapper.hdf",
				   "/home/joaoalb/Documents/Cosmologia/hide_and_seek/resultados/healpix_seek/K/1f_noise/FreeFree/Tsys_70_alpha_1_fknee_0_001/simple_mapper/variance/2d_10days/bingo_maps_28_horns_10days_simple_mapper.hdf"],
				  ["/home/joaoalb/Documents/Cosmologia/hide_and_seek/resultados/healpix_seek/K/1f_noise/FreeFree/Tsys_70_alpha_1_fknee_0_001/filter_mapper/variance/-2d/bingo_maps_28_horns_-2d_filter_mapper.hdf",
				   "/home/joaoalb/Documents/Cosmologia/hide_and_seek/resultados/healpix_seek/K/1f_noise/FreeFree/Tsys_70_alpha_1_fknee_0_001/filter_mapper/variance/2d/bingo_maps_28_horns_2d_filter_mapper.hdf",
				   "/home/joaoalb/Documents/Cosmologia/hide_and_seek/resultados/healpix_seek/K/1f_noise/FreeFree/Tsys_70_alpha_1_fknee_0_001/filter_mapper/variance/2d_10days/bingo_maps_28_horns_10days_filter_mapper.hdf"]]
	
	titles = [["Simple Mapper - 1 day (-2d)",
			   "Simple Mapper - 5 days (2d)",
			   "Simple Mapper - 10 days (2d)"],
			  ["Filter Mapper - 1 day (-2d)",
			   "Filter Mapper - 5 days (2d)",
			   "Filter Mapper - 10 days (2d)"]]

	
	mapas = []
	
	for i in range(len(file_paths)):
		mapas.append([])
		for k in range(len(file_paths[0])):
			mapas[i].append(h5py.File(file_paths[i][k], "r")["MAPS"][()])
	
	
	avs = []
	
	for i in range(len(mapas)):
		avs.append([])
		for k in range(len(mapas[0])):
			avs[i].append(lat_average(mapas[i][k]))


	nrows = len(file_paths)
	ncols = len(file_paths[0])
	fig, axs = plt.subplots(nrows=nrows, ncols=ncols, sharex=True, sharey=True)
	
	for row in range(nrows):
		for col in range(ncols):
			
			print(row,col)
			axs[row][col].plot(avs[row][col][1], avs[row][col][0])
			axs[row][col].set_title(titles[row][col])
			axs[row][col].set_xlabel("Latitude (deg)")
			axs[row][col].set_ylabel("Average Temp (K)")
			
	axs[0][0].set_xlim(0,30)
	
	fig.suptitle("Latitude Average Variance")
	plt.show()
	
