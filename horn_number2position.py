import numpy as np

xOr=[  510.,   270.,	30.,  -210.,  -450.,  -690.,  -930.,
	   390.,   150.,   -90.,  -330.,  -570.,  -810., -1050.,   
	   330.,    90.,  -150.,  -390.,  -630.,  -870., -1110.,   
	   450.,   210.,   -30.,  -270.,  -510.,  -750.,  -990.]

yOr=[-304.86625, -304.86625, -304.86625, -304.86625, -304.86625, -304.86625, -304.86625, 
	 -110.86125, -110.86125, -110.86125, -110.86125, -110.86125, -110.86125, -110.86125, 
	  110.86125,  110.86125,  110.86125,  110.86125,  110.86125,  110.86125,  110.86125,  
	  304.86625,  304.86625,  304.86625,  304.86625,  304.86625,  304.86625,  304.86625]


def pos_from_disp_file(disp_txt, d):

	horn_pos = np.zeros((28,2)) # [ [x1,y1], [x2,y2], ...]
	horn_pos[:,0] = xOr
	horn_pos[:,1] = yOr

	horn_info = np.loadtxt(disp_txt)[:,0]

	horn_disp = (horn_info-1)%5-2
	horn_numbers = np.array((horn_info-1)//5, dtype=int) # 0-27 to make indices. If 1-28, add 1
	disp_pos = []

	for i, h_info in enumerate(horn_info): #disp_pos[np.where(horn_disp==d)]):
		if horn_disp[i]==d:
			pos = horn_pos[horn_numbers[i]]
			disp_pos.append(pos)
			
	return disp_pos
		
		
def fits_from_pos(horn_pos, freq="980GHz", Npoints=101, jobNamePrefix="Retangular"):

	# mudar pra receber um fits_fmt e um kwargs que vai no fmt
	fits_files = []
	for pos in horn_pos:
		horn_fits = "{}_{}_{}_{}pts_{}.fits".format(jobNamePrefix, int(pos[0]), int(pos[1]), Npoints, freq).replace("-","MINUS")
		fits_files.append(horn_fits)
		
	return fits_files
	
	
def fits_from_disp_file(disp_txt, d, outtxt, freq="980GHz", Npoints=101, jobNamePrefix="Retangular"):
	
	horn_pos = pos_from_disp_file(disp_txt, d)
	fits_files = fits_from_pos(horn_pos, freq, Npoints, jobNamePrefix)
	np.savetxt(outtxt, fits_files, fmt="%s")
	return fits_files

	
if __name__=="__main__":
	
	disp_txt = "/scratch/bingo/joao.barretos/hide_and_seek/hide-beam/drectangular.txt"
	d =2 
	outtxt = "all_horns_fits_{}.txt".format(d)
	fits_files = fits_from_disp_file(disp_txt, d, outtxt, freq="980GHz", Npoints=101, jobNamePrefix="Retangular")
	for ff in fits_files:
		print(ff)
