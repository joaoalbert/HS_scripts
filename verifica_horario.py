# -*- coding: cp1252 -*-
'''
Author: Carlos Otobone, João Alberto
Created at: 14/08/2020
Last Updated at: 15/08/2020
'''

import radec2altaz
import numpy as np


def findtime (w_path, d_path, GEO, date, perfil, displacement = 0):
	
	hour_verified = 0
	minute_verified = 0

	coord_before = radec2altaz.RAdec2AltAz(0.000000, -15.398583, GEO[0], GEO[1], GEO[2], date)
	
	hours = 24
	#minutes = 60

	print("Verifying each hour...")
	for hour in range (1, hours):
	
		date = date.split()[0] + ' {:02d}:00'.format(hour)
		coord_current = radec2altaz.RAdec2AltAz(0.000000, -15.398583, GEO[0], GEO[1], GEO[2], date) 
		#print("Current == " + str(coord_current))
	   
		if (coord_current[1] >= 90 and coord_current[1] <= 270 and coord_current[0] >= 0):
			if (abs(coord_current[1] - 180) < abs(coord_before[1] - 180)):
				coord_before = coord_current
				hour_verified = hour

		elif (coord_current[1] > 270 and coord_current[0] >= 0):
			coord_current[1] = 360 - coord_current[1]

		elif(coord_current[1] < 90 and coord_current[0] >= 0):
			if (abs(coord_current[1]) < abs(coord_before[1])):
				coord_before = coord_current
				hour_verified = hour
	
	
	print("Verifying each minute...")
	for minute in range(1, 60):
	
		date = date.split()[0] + ' {0:02d}:{1:02d}'.format(hour_verified, minute)
		coord_current = radec2altaz.RAdec2AltAz(0.000000, -15.398583, GEO[0], GEO[1], GEO[2], date) 
		#print("Current == " + str(coord_current))


		if (coord_current[1] >= 90 and coord_current[1] <= 270 and coord_current[0] >= 0):
			if (abs(coord_current[1] - 180) < abs(coord_before[1] - 180)):
				coord_before = coord_current
				minute_verified = minute

		elif (coord_current[1] > 270 and coord_current[0] >= 0):
			coord_current[1] = 360 - coord_current[1]

		elif(coord_current[1] < 90 and coord_current[0] >= 0):
			if (abs(coord_current[1]) < abs(coord_before[1])):
				coord_before = coord_current
				minute_verified = minute

	
	if (minute_verified == 0):
		print("Verifying minutes in the previous hour...")
	
		hour_verified -= 1
		for minute in range(1, 60):
		
			date = date.split()[0] + ' {0:02d}:{1:02d}'.format(hour_verified, minute)
			coord_current = radec2altaz.RAdec2AltAz(0.000000, -15.398583, GEO[0], GEO[1], GEO[2], date) 
			#print("Current == " + str(coord_current))

			if (coord_current[1] >= 90 and coord_current[1] <= 270 and coord_current[0] >= 0):
				if (abs(coord_current[1] - 180) < abs(coord_before[1] - 180)):
					coord_before = coord_current
					minute_verified = minute

			elif (coord_current[1] > 270 and coord_current[0] >= 0):
				coord_current[1] = 360 - coord_current[1]

			elif(coord_current[1] < 90 and coord_current[0] >= 0):
				if (abs(coord_current[1]) < abs(coord_before[1])):
					coord_before = coord_current
					minute_verified = minute

	print("A melhor hora eh {0:2d}:{1:2d}\nA melhor coordenada eh {2}".format(hour_verified, minute_verified, coord_before))
	
	return(hour)



if __name__=="__main__":


	w_path = '/home/otobone/Documentos/ic/projeto_karin/exercicios/optical/'
	d_path = '/home/otobone/Documentos/ic/projeto_karin/hide-master/'
	files = ['drectangular', 'rectangular', 'hexagonal']
	GEO =[-7.0, -38.0, 0.0]										# [telescope_latitude, telescope_longitude, telescope_elevation]
	date = '2018-01-{:02d} 00:00'
	perfil = files[2]

	for i in range(1,30): findtime(w_path, d_path, GEO, date.format(i), perfil)
	
