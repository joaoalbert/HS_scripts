'''
Esse programa eu escrevi,
tem que pegar a versao que eu e o
carlos escrevemos juntos.

att,
joao
'''

import numpy as np
import matplotlib.pyplot as plt
import healpy as hp
import h5py
import astropy.io.fits as pyfits


def cl(map_path, channel=0):

	
	type0 = map_path.split(".")[-1]
	if   type0=="hdf":		map_0 = h5py.File(map_path, "r")["MAPS"][()][channel]
	elif type0=="fits": 	map_0 = pyfits.getdata(map_path)[channel]
	else: print("Invalid type: "+type0)
	
	counts = len(map_0)-np.sum(map_0==hp.UNSEEN)
	cls = (len(map_0)/counts) * hp.anafast(map_0)
	
	return cls
	
	
if __name__=="__main__":

		
		if False:

			displacements = ["-2d", "2d", "2d_10days"]
			mapmakings = ["simple_mapper", "filter_mapper"]
			
			std_maps = ["/home/joaoalb/Documents/Cosmologia/hide_and_seek/hide-master/hide/data/sky/free_free_cube_hs_test_rot_kelvin.fits",
						"/home/joaoalb/Documents/Cosmologia/hide_and_seek/resultados/healpix_seek/K/noiseless/FreeFree/simple_mapper/{}/bingo_maps_28_horns_convolved_beam.hdf"]
		
			map_path = "/home/joaoalb/Documents/Cosmologia/hide_and_seek/resultados/healpix_seek/K/1f_noise/FreeFree/Tsys_70_alpha_1_fknee_0_001/{}/{}/"
			
			
			maps = { std_maps[1].format(d):"beam_convolved_map_{}".format(d) for d in displacements }
			maps[std_maps[0]] = "original_map"
			
			
			import os
			
			for mm in mapmakings:
				for d in displacements:
					path = map_path.format(mm,d)
					maps[path + [ arq for arq in os.listdir(path) if "bingo_maps_horn" not in arq and arq.split(".")[-1]=="hdf" ][0]] = mm+"_"+d
				
				
		if True:
			
			maps = {"/home/joao/Documentos/cosmologia/hide_and_seek/hide-master/hide/data/sky/delta_Nside_128_Nseed_10001_rot_kelvin.fits":"Before SEEK (original)",
					"/home/joao/Documentos/cosmologia/hide_and_seek/resultados/healpix/gaussian/delta_128/delta_128_1day/bingo_maps_28_horns.hdf": "After SEEK (gaussian -2d)",
					"/home/joao/Documentos/cosmologia/hide_and_seek/resultados/healpix/gaussian/delta_128/delta_128_5days/bingo_maps_28_horns.hdf": "After SEEK (gaussian 2d)",
					"/home/joao/Documentos/cosmologia/hide_and_seek/hide-master/hide/data/sky/delta_smooth_gaussian.fits": "Smooth Map (original+healpix smoothing)"}
				
				
		plt.figure(1)	
		for map0 in maps:
			plt.loglog(cl(map0),label=maps[map0])
			#plt.legend(maps[map0])
			
		plt.title("21 cm Nside=128")
		plt.xlabel("l")
		plt.ylabel("Cl")
		plt.legend()
		plt.show()
	

				
