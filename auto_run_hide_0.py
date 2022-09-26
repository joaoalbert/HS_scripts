# -*- coding: cp1252 -*-
'''
Authors: Carlos Otobone, João Alberto

Created at: 10/08/2020
Last Updated: August 2022
'''


import os
import radec2altaz
import tod_plots as tod_plot
import numpy as np


#.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'#
#.'.Função principal'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'#
#.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'#

def main(destination_path, GEO, date_fmt, initial_day=1, final_day=5):
	'''
	Altera as altitudes e azimutes das cornetas do BINGO para cada
	displacement (um displacement por dia) e roda o HIDE para cada
	respectivo dia.
	
	destination_path: string. Path do hide no diretório local. Deve
	conter tambem o txt das coordenadas em RA, dec.
	GEO: [lat, lon, el]. Posicao geografica de observacao.
	date_fmt: "YYYY-MM-DD HH:MM". Data para conversao de coords.
	initial_day: int<=28. Dia inicial a fazer a analise.
	final_day: initial_day<=int<=28. Dia final a fazer a analise.
	'''

	#.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'#
	#.'.Início'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'#
	#.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'#
	
	#.'.Lendo bingo.py'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'#
	with open(destination_path + 'hide/config/bingo.py','r') as bingo_read:
		bingo_lines = bingo_read.readlines()
		bingo_read.close()
	for line in bingo_lines:
		if line[0:11] == "output_path":
			output_path = line.split()[line.split().index("=")+1] + "/"
			break
		
		
	# Sem correcao para mais de um mes!!
	for day in range (initial_day, final_day+1):
	
		#.'.Convertendo coordenadas.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'#
		# Se o feixe for assimetrico, deve ser feita uma correcao do horario 
		# pelo programa verifica_horario???

		# Faz um displacement por dia
		displacement = -2+(day-1)%5
		date = date_fmt.format(day)
		print("\n\nDay: {} // Displacement: {}d\n".format(date.split()[0], displacement))
		radec2altaz.main(destination_path, 
						 destination_path, 
						 GEO, 
						 date, 
						 "drectangular.txt", 
						 displacement)
		
		#.'.Alterando o programa bingo.py.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'#
		bingo = open(destination_path + 'hide/config/bingo.py','w')
		for line in bingo_lines:
			if line[0:14] == "strategy_start":
				bingo.write("strategy_start = '" + date[0:-6]+"-00:00:00" + 
							"' # survey start time. Format YYYY-mm-dd-HH:MM:SS\n")
			elif line[0:12] == "strategy_end":
				bingo.write("strategy_end = '" + date[0:-6]+"-23:59:59" + 
							"'   # survey start time. Format YYYY-mm-dd-HH:MM:SS\n")
			else:
				bingo.write(line)
		bingo.close()

		#.'.Executando o run_hide.py'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'#
		os.chdir(destination_path)
		os.system('python3 run_hide.py')
		
		#.'.Plotando o TOD.'.'.'..'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'#
		#tod_plot.tod24h(output_path, date[0:10], 0) #plotando só a corneta 1



#.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'#
#.'.Entrada de informações'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'#
#.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'.'#


if __name__=="__main__":

	#working_path = "/home/joaoalb/Documents/Cosmologia/hide_and_seek/resultados/optical/"
	destination_path = "/scratch/bingo/joao.barretos/hide_and_seek/hide-beam/"
	#output_path      = "/home/joaoalb/Documents/Cosmologia/hide_and_seek/resultados/TOD/freq_bingo/K/noiseless/deg_2/"

	GEO = [-7.0, -38.0, 0.0]									  # [telescope_latitude, telescope_longitude, telescope_elevation]
	date_fmt = '2018-01-{:02d} 19:47'							  # 'YYYY-MM-DD HH:MM'
	initial_day, final_day = 1, 1

	main(destination_path, GEO, date_fmt, initial_day, final_day)
