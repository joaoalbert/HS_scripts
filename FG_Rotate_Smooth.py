# encoding: utf-8
##############################################################################
## Script for Rotating, Smoothing and Tempretature Subtration in loop
# over 30 maps 
##																	   #####
## ## Authors: Karin Fornazier, Alessando Marins and Filipe Abdala
## Email: karin.fornazier@gmail.com
## Supervisor: F.B. Abdalla
##
## Last modified by: Joao Alberto & CArlos Otobone
## Latest Version February 2022
###########################################################################
###########################################################################
import healpy as hp
import numpy as np
from astropy.io import fits as pyfits
import matplotlib.pyplot as plt
plt.switch_backend('agg')


input_file = "/home/joao/Documentos/cosmologia/hide_and_seek/hide-master/hide/data/sky/ame_cube_hs_test_galactico_1024.fits"
output_file = "/home/joao/Documentos/cosmologia/hide_and_seek/hide-master/hide/data/sky/ame_cube_hs_test_celestial_1024.fits"
rotate = True
smooth = False

#FWHM = np.radians(0.0116355)
#SIGMA = np.radians(5)


def map_rotation(m = None, coord_in = "G", coord_out = "C"):
   
# Basic HEALPix parameters
   coord = [coord_in,coord_out]
   npix  = m.shape[-1]
   nside = hp.npix2nside(npix)
   ang   = hp.pix2ang(nside, np.arange(npix))  
 # Select the coordinate transformation
   rot = hp.Rotator(coord=reversed(coord))

   # Convert the coordinates
   ang = rot(*ang)
   pix = hp.ang2pix(nside, *ang)

   return m[..., pix]



FG = pyfits.getdata(input_file)
rot_cube = np.zeros(FG.shape)

for i in range(len(FG)):
	a = i
	# hp.mollview(FG[a,:],title="Added Components", unit=r'Temperature (mK)')
	# plt.savefig('/home/otobone/Documentos/ic/projeto_karin/exercicios/plots_healpix/plots_sky/soma_delta_foreground/rotsmooth/delta_'+ str(i) + '.png')
	# pyfits.writeto('delta_'+str(i)+ '.fits', FG[a,:], overwrite=True) 
		
	# #Apply rotation
	if rotate:
		FGr = map_rotation(FG[i,:])
		#hp.mollview(FGr,title="Added Components", unit=r'Temperature (mK)')
		#plt.savefig('/home/otobone/Documentos/ic/projeto_karin/exercicios/plots_healpix/plots_sky/delta/rotsmooth/rotame_'+ str(i) + '.png')
		#pyfits.writeto('delta_'+ str(i) + 'rot.fits', FGr) 
	
		#Apply Smooth
		if smooth:
			FGrsm = hp.sphtfunc.smoothing(FGr,fwhm=FWHM)
			#hp.mollview(FGrsm,title="Added Components", unit=r'Temperature (mK)')
			#plt.savefig('/home/otobone/Documentos/ic/projeto_karin/exercicios/plots_healpix/plots_sky/soma_delta_foreground/rotsmooth/rotsmoothdelta_'+ str(i) + '.png')
			#pyfits.writeto('delta_'+str(i)+ 'rot_smooth.fits', FGrsm)
		else:
			FGrsm = FGr
	
	rot_cube[i] = FGrsm

pyfits.writeto(output_file, rot_cube)
