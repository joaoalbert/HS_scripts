'''
This is a tutorial to show how to open FITS files (.fits) and HDF5 files (.h5).
'''
import numpy as np

#===============================================================
# 1) FITS files
# FITS files are usually used to contain images such as sky maps.
print(" 1) FITS files\n\n")
import astropy.io.fits as pyfits # library to handle FITS files


fits_path = "basic_tutorial/ame_cube_hs_test_rot_kelvin.fits"

fits_file = pyfits.open(fits_path) # --> this is a list of HDU objects, each one containing a header and its respective data

print("List of HDUs in {}:\n".format(fits_path))
print(fits_file.info())

for HDU in fits_file:
	# the information can be retrieved from the header as in a dictionary, 
	# e.g. using HDU.header["DATE"]
	print("\nHDU header:")
	HDU.header
	print("HDU data:")
	print(HDU.data) # the data can be extracted from each HDU this way

fits_file.close()


# An alternative way to easily get the data without having to open the file is the getdata function.
fits_data = pyfits.getdata(fits_path)



#===============================================================
# 1.5) HEALPix maps
# HEALPix (Hierarchical Equal Area isoLatitude Pixelation) maps are spherical maps pixelated in a way such that its pixels have the same area, and are disposed in strips with equal latitude.
# Pixelation scheme is such that the minimum number of pixels is 12, and each pixel can always be divided in 4, making four times more pixels than before. It follows the equation
# Npix = 12*Nside**2
# in which Nside is always a power of 2 (1, 2, 4, ..., 128, 256, 512, ...).
# The most usual Nsides on Cosmology are the ones among 128-1024.

print("\n\n 1.5) Sky maps as HEALPix maps\n\n")
import healpy as hp # library to handle sky maps in Healpix format
# Currently, Healpy is incompatible with Matplotlib, so to assure compatibility, have Matplotlib==3.2.1 installed.


# Let's make a simple map first, with Nside=1.
nside = 1
npix = hp.nside2npix(nside)
map0 = np.arange(npix) #0-11 vector

# Plotting the map
import matplotlib.pyplot as plt
hp.mollview(map0) # you can see it starts counting the pixels from the north pole and rotates in equal latitudes down to the south pole
plt.show()


# The FITS file containing the maps is called a cube, because it has multiple maps for different frequencies.

cube_size = fits_data.shape
print("Size of this cube = {}".format(cube_size)) # 1st index: frequency / 2nd index: pixels
npix = cube_size[1]
print("Number of pixels in each map = {}".format(npix))
nside = hp.npix2nside(npix)
print("Correspondent Nside = {}".format(nside))

# Let's plot the first map of the cube
hp.mollview(fits_data[0])
plt.show()




#===============================================================
# 2) HDF5 files
# HDF5 files are very useful because they are able to store numerical data more efficiently than other file extensions such as TXT, CSV or JSON. Due to its data storage scheme, one cannot easily open them with a text editor.

print("\n\n 2) HDF5 files\n\n")
import h5py

# HIDE TODs contain three datasets: FREQUENCY, P and TIME.
# FREQUENCY: frequency for the TOD data
# P: brightness temperature split between polarizations
# TIME: time for the TOD data

file_path = "./basic_tutorial/test_TOD/2018/01/01/bingo_tod_horn_0_20180101_000000.h5"
h5_file = h5py.File(file_path)

print("Datasets for {}:".format(file_path.split("/")[-1]))
for dataset in h5_file:
	print(dataset)

# We have two polarizations so there are two sets of data inside P. To access this data, one uses syntax such as dictionaries.
print("\nPolarization datasets:")
for pol in h5_file["P"]:
	print(pol)

# To retrieve the data:
Phase0 = h5_file["P"]["Phase0"][()] # or h5_file["P/Phase0"][()]
Phase1 = h5_file["P"]["Phase1"][()] # or h5_file["P/Phase1"][()]
print("\nData for each polarization:")
print("\nPhase0:")
print(Phase0)
print("\nPhase1:")
print(Phase1)

h5_file.close()

print()
