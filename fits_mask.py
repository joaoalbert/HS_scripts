# -*- coding: cp1252 -*-            #Comando para aceitar o João.

'''
Created on 16/12/2020
Last update 16/12/2020

Author: Carlos Otobone, João Alberto
'''
from __future__ import print_function
import numpy as np
import healpy as hp
import astropy.io.fits as pyfits
import matplotlib.pyplot as plt
import os
import h5py

def maskedmapplot(w_path, map_path):

    year = w_path.split('/')[-4]
    month = w_path.split('/')[-3]
    day = w_path.split('/')[-2]

    time_break_bool = True
    time_start = 6      # o programa so considera a parte inteira. Por enquanto.
    time_end = 11.99
    # time_break = 24.0       #Seleciona o periodo de observacao

    print(year)

    nside = 128
    #npix = 128 * 128 * 12 apenas para lembrar a definição de npix

    masked = np.zeros(hp.nside2npix(nside)) 
    horns = 0

    hours = 24

    # conteudo = os.listdir(w_path) #cria uma lista com o conteudo do diretorio
    
    # for file in conteudo:
    #     if (file.split('.')[-1] == 'txt'):
    #         horns += 1
    freq = 0
    original_map = pyfits.getdata(map_path)[freq]

    for horn in range (horns+1):
        print('\nLendo arquivo da corneta ' + str(horn) + '...')
        with open(w_path + 'coord_bingo_' + str(horn) + '_' + year + month + day+ '.txt', 'r') as coord_read:
            coord_lines = coord_read.readlines()
            coord_read.close()

        coord_lines.pop(0)
        
        print('Coletando angulos de RA e DEC do arquivo...' )


        for hour in range(int(time_start), (int(time_end)+1)):      #percorre as horas

            temp_maps = h5py.File(w_path + 'bingo_tod_horn_' + str(horn) + '_' + year + month + day+ '_' + '{:02d}0000.h5'.format(hour), 'r')["P/Phase1"][()][0]   #coleta as temperaturas do arquivo.h5 em um vetor. Com uma frequencia fixa.

            if(hour != 23):
                seconds = 3600
            else:
                seconds = 3599

            for i in range(seconds):   #percorre os segundos

                line = coord_lines[(hour*3600 + i)]

                ra = float(line.split(",")[-2])
                dec = float(line.split(",")[-1])
                instant = int(float(line.split(",")[0]))

                # print("\rTime " + str(instant), end = '')
            
                theta = ra
                phi = dec
                pix = hp.ang2pix(nside, theta, phi, lonlat = True)

                masked[pix] = original_map[pix]

                # if(horn == (horns - 1)):
                    # NAIVE[pix] /= masked[pix]


    print('Gerando imagem')

    minute_start = int((time_start%1)*60)
    minute_end = int((time_end%1)*60)

    # masked[counts==0] = hp.UNSEEN
    hp.mollview(masked, title= "Masked Map " + str(int(time_start)) + ":" + str(minute_start) + " - " + str(int(time_end)) + ":" + str(minute_end) + "(Standard)") #cmap= 'jet')
    # plt.show()
    plt.savefig(w_path + "/maskedmap_12am_standard.png")
    plt.close()

    # pyfits.writeto(w_path + 'hitmap_bingo_' + year + month + day + '_' + str(time_break) + 'hours.fits', masked, overwrite = True)

maskedmapplot("/home/otobone/Documentos/ic/projeto_karin/resultados/TOD/synch/horario_parcial/2018/01/01/", "/home/otobone/Documentos/ic/projeto_karin/hide-master/hide/data/sky/synch_cube_hs_test_rot.fits")