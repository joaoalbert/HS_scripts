import zmod.zernike_fit as zfit
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import healpy as hp



coeffs = np.array([[10,0,0],
				   [0.5,1,-1],
				   [-1.3,1,1],
				   [10,2,0],
				   [-15,6,0],
				   [1.2,9,-5]])

nside = 128
area = (6*0.011)**2


npix = int(np.sqrt(area/hp.nside2pixarea(nside)))
npix = npix if npix%2==1 else npix+1
pixsize = hp.max_pixrad(nside)
angs = pixsize * np.linspace(-npix/2,npix/2,2*npix+1)
ra, dec = map(np.ndarray.flatten, np.meshgrid(angs,angs))
beam = zfit.radec_beam(coeffs,ra,dec,R=3*0.011)

smaller_angs = pixsize * np.linspace(-npix/2,npix/2,int(npix))
i,j = map(np.ndarray.flatten, np.meshgrid(smaller_angs,smaller_angs))
beam_interp = interpolate.griddata((ra,dec),beam,(i,j),method="nearest")

plt.figure(0)
plt.scatter(ra,dec)
plt.scatter(i,j)
plt.figure(1)
plt.title("original")
plt.scatter(ra,dec,c=beam,s=16*20)
plt.title("interp")
plt.scatter(i,j,c=beam_interp,s=16*20)
plt.show()
