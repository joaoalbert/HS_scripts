import numpy as np
import healpy as hp
import matplotlib.pyplot as plt

beam_elevation = 5*0.011 # [rad]
beam_azimut = 5*0.011
beam_nside = 128

beam_area = beam_elevation * beam_azimut
pixel_area = hp.nside2pixarea(beam_nside, degrees=False)
pixels = int(np.floor(np.sqrt(beam_area / pixel_area)))
pixels = pixels if pixels%2==1 else pixels+1

pixel_size = hp.max_pixrad(beam_nside)
theta = (np.linspace(0, pixels, pixels*2+1)-pixels/2)*(pixel_size)
phi = theta

ra_grid, dec_grid = np.meshgrid(theta,phi)
plt.scatter(ra_grid,dec_grid)
plt.show()
