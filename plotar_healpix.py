# -*- coding: cp1252 -*-

'''
Created on 14/07/2020
Last update 10/2021

Author: Carlos Otobone, João Alberto
'''

import healpy as hp 
import matplotlib.pyplot as plt 
import numpy as np
import os
import astropy.io.fits as pyfits



def gsm_plot():
		
	source_path = "/home/otobone/Documentos/ic/projeto_karin/hide/hide/data/gms/maps/"
	destination_path = "/home/otobone/Documentos/ic/projeto_karin/exercicios/plots_healpix/plots_gsm/"
	
	# lista = ["16","32"]
	# freqs = [980]
	lista = ["16","32","64"]
	freqs = np.linspace(980,1280,61,endpoint=True)		
	for i in lista:
		for j in freqs:
			
			file_name = "gsm_" + str(int(j)) + ".0.fits"
									
			path_map = os.path.join(source_path + i, file_name)	
			#print(path_map)
			map0 = hp.read_map(path_map)
			#hp.mollview(map0)
			plt.savefig(destination_path + i + "/gsm_" + str(int(j)) + ".0.png")
			# plt.show()
			plt.close()

			#os.system("chmod a+rwx " + destination_path + i + "/gsm_" + str(int(j)) + ".0.png")

	# map0 = hp.read_map("/home/otobone/Documentos/ic/projeto_karin/hide/hide/data/gsm/maps/16/gsm_980.0.fits")
	# hp.mollview(map0)
	# plt.show()



def sky_plot(map_file, destination_path, titulo, channel = 0, mini = None, maxi = None, unidade =r'Temperature (mK)'):

	os.system("mkdir " + destination_path + "/")
	maps = pyfits.getdata(map_file) 
	print("Salvando imagens do healpix {0}...".format(map_file.split("/")[-1]))
	
	if mini == None and maxi == None: hp.mollview(maps[channel], title= titulo, unit=unidade, cmap ='jet')  
	else: hp.mollview(maps[channel], title= titulo, unit=unidade, cmap ='jet', min = mini, max = maxi)

	plt.savefig(destination_path + titulo + ".png")
	# plt.show()
	plt.close()
	hp.gnomview(maps[channel], title= titulo + " (zoom)", rot= (0,-17),reso= 5, xsize= 400, ysize= 200)
	plt.savefig(destination_path + titulo + "_zoom.png")
	plt.close()
		
	# print("\nImagens salvas no diretorio {0}".format(destination_path))



def data_prints():
    
	source_path = "/home/otobone/Documentos/ic/projeto_karin/hide-master/hide/data/sky/"
	destination_path = "/home/otobone/Documentos/ic/projeto_karin/exercicios/plots_healpix/foregrounds/"

	
	file_names = ["freqs_foregrounds_test", "maps_foregrounds_test"]
	
	for file_name in file_names:
		path_map = os.path.join(source_path, file_name + ".fits")
		map0 = pyfits.getdata(path_map)
		hdul = pyfits.open(os.path.join(source_path, file_name + ".fits"))

		print(map0.shape)
		# print(hdul.data)
	
	
	
def soma_comp():
	
	source_path = "/home/otobone/Documentos/ic/projeto_karin/hide-master/hide/data/sky/"
	destination_path = "/home/otobone/Documentos/ic/projeto_karin/exercicios/plots_healpix/plots_sky/"

	# os.system("cd " + source_path)
	file_names = ["freqs_foregrounds_test.fits","delta_Nside_128_Nseed_10001.fits","foreground_cube_hs_test.fits"]
	# file_names = os.listdir(os.getcwd())
	# print(file_names)
	# file_names = ["freqs_foregrounds_test.fits", "ame_cube_hs_test.fits"]
	freq_name = file_names.pop(0) # O metodo pop arranca o elemento escolhido da lista.
	freq_list = pyfits.getdata(source_path + freq_name)
	# print(freq_list)
	map_soma = np.zeros(pyfits.getdata(source_path + file_names[1]).shape)
	
	titulo = "soma"
	for file_name in file_names:
		tira_ = file_name.split("_")[0]

		titulo = titulo + "_" + tira_

	Npix = hp.nside2npix(128)
	soma_cube = np.zeros((30,Npix))

	os.system("mkdir " + destination_path+ titulo + "/" )
	for i in range (len(freq_list)):
		for file_name in file_names:
			maps = pyfits.getdata(source_path + file_name)
			map_soma[i] += maps[i]

		soma_cube[i,:] = map_soma[i]				
		
		print ("lendo-->", i)  
		

	# hp.mollview(map_soma[i])
	# plt.savefig(destination_path + titulo + "/" + titulo + "_" + str(freq_list[i]) + ".png")
	# plt.close()
	
	pyfits.writeto(source_path + 'components_maps_cube.fits', soma_cube)
		
	print("Imagens salvas com sucesso no diretorio {0}".format(destination_path))



def h5_map_plot(path, map_file, title):
	'''
	Plota o mapa de um único HDF5.
	'''
	import h5py

	print("Criando diretorio map_plots...")
	os.system('mkdir -p ' + path + 'map_plots/')
	print("Abrindo arquivo ", map_file)
	fp = h5py.File(path + map_file, 'r')	
	mapa = fp['MAPS'][()]
	counts = fp['COUNTS'][()]
	fp.close()

	mapa[counts==0] = hp.UNSEEN

	plt.figure(0)
	hp.mollview(mapa[0, 0, :], cmap="jet")
	plt.title(title)
    #plt.show()
	plt.savefig(path + "map_plots/" + title + ".png")
	plt.close()
		
	hp.gnomview(mapa[0, 0, :], title= title + " (zoom)", unit="(K)", rot=(0,-17), cmap='jet', reso=5, xsize=400, ysize=200)
	#plt.show()
	plt.savefig(path + "map_plots/" + title + "_zoom.png")
	plt.close()




def combine_h5_horn_maps(path, map_file_format, title, horns, file_name=0, channel=0):
	'''
	Essa funcao pega diversos mapas individuais das cornetas do Bingo
	e gera um mapa que é a soma ponderada pelas contagens (hits) desses
	mapas.
	'''
	
	import h5py

	# Reading files

	print("Criando diretorio map_plots...")
	os.system('mkdir -p ' + path + 'map_plots/')
	
	fp = h5py.File(path + map_file_format.format(0), 'r')
	mapa = fp['MAPS'][()]
	counts = fp['COUNTS'][()]
	fp.close()


	# Generating map

	maps = np.zeros(mapa[:,0,:].shape)
	counts_total = np.zeros(counts[0,0,:].shape)

	for i in range(horns):
		print("Coletando dados da corneta {}".format(i))
		fp = h5py.File(path+map_file_format.format(i), 'r')
		mapa = fp['MAPS'][()]
		counts = fp['COUNTS'][()]
		fp.close()

		maps += mapa[:,0,:]
		counts_total += counts[0,0,:]
	
	print(counts_total.shape)
	mask = np.where(counts_total == 0, 1, counts_total)
	maps[channel, :][counts_total==0] = hp.UNSEEN


	# Creating the map file

	if file_name==0: file_name=title

	print("Criando arquivo " + file_name + ".hdf")
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
        
	if False:
	                 
		for i in range(28):
			h5_map_plot("/home/otobone/Documentos/ic/projeto_karin/resultados/healpix_seek/drectangular/2d/", "bingo_maps_horn_{}.hdf".format(i), "bingo_maps_horn_{}".format(i))


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
		
		
