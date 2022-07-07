# -*- coding: cp1252 -*-            #Comando para aceitar o João.

'''
Created on ??/08/2020
Last update 08/09/2020

Author: Carlos Otobone, João Alberto
'''
from __future__ import print_function
import numpy as np
import healpy as hp
import astropy.io.fits as pyfits
import matplotlib.pyplot as plt
import os
import h5py

def hitmapplot(w_path, perfil):

    year = w_path.split('/')[-4]
    month = w_path.split('/')[-3]
    day = w_path.split('/')[-2]

    time_break_bool = True
    time_break = 24.0       #Seleciona o periodo de observacao

    print(year)

    nside = 64
    #npix = 128 * 128 * 12 apenas para lembrar a definição de npix

    HITMAP = np.zeros(hp.nside2npix(nside)) 
    horns = 0
    hit_tot = 0
    
    NAIVE = np.zeros(hp.nside2npix(nside))

    hours = 24


    conteudo = os.listdir(w_path) #cria uma lista com o conteudo do diretorio
    
    for file in conteudo:
        if (file.split('.')[-1] == 'txt'):
            horns += 1

    for horn in range (horns):
        print('\nLendo arquivo da corneta ' + str(horn) + '...')
        with open(w_path + 'coord_bingo_' + str(horn) + '_' + year + month + day+ '.txt', 'r') as coord_read:
            coord_lines = coord_read.readlines()
            coord_read.close()
                
        coord_lines.pop(0)

        hit_tot += len(coord_lines) * (time_break / 24)
        
        print('Coletando angulos de RA e DEC do arquivo...' )
        

        for hour in range(24):      #percorre as horas
                    

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

                print("\rTime " + str(instant), end = '')
            
                theta = ra
                phi = dec
                pix = hp.ang2pix(nside, theta, phi, lonlat = True)

                NAIVE[pix] += temp_maps[i]

                HITMAP[pix] += 1

                if(horn == (horns - 1)):
                    NAIVE[pix] /= HITMAP[pix]

                if (time_break_bool and instant == time_break):
                    break            


    
    print('\n')
    print('Contagem, total esperado: ' + str(int(hit_tot - horns)))
    print('Contagem, total obtido: ' + str(int(np.sum(HITMAP))))
    print('Gerando imagem')
    
    hitmap = False
    naivemap = True

    if (hitmap):
        hp.mollview(HITMAP, title= 'Hitmap BINGO ' + year + '/' + month + '/' + day + ' (' + str(time_break) + ' hours) - ' + perfil, cmap= 'jet')
        plt.show()
        # plt.savefig(w_path + 'hitmap_bingo_' + year + month + day + '_' + str(time_break) + 'hours_' + perfil + '.png')
        plt.close()

        pyfits.writeto(w_path + 'hitmap_bingo_' + year + month + day + '_' + str(time_break) + 'hours.fits', HITMAP, overwrite = True)

        hp.gnomview(HITMAP, title= 'Hitmap (zoom) BINGO ' + year + '/' + month + '/' + day + ' (' + str(time_break) + ' hours) - ' + perfil, rot= (0,-17), cmap= 'jet', reso= 5, xsize= 400, ysize= 200)    #cmap = 'jet', 'cool', 'winter', 'viridis'
        plt.show()
        # plt.savefig(w_path + 'hitmap_bingo_' + year + month + day + '_' + str(time_break) + 'hours_' + perfil + '_zoom.png')
        plt.close()
    
    if (naivemap):
        hp.mollview(NAIVE, title= 'Naivemap BINGO ' + year + '/' + month + '/' + day + ' (' + str(time_break) + ' hours) - ' + perfil, cmap= 'jet')
        # plt.show()
        plt.savefig(w_path + 'naivemap_bingo_' + year + month + day + '_' + str(time_break) + 'hours_' + perfil + '_' + str(nside) + '.png')
        plt.close()

        pyfits.writeto(w_path + 'naivemap_bingo_' + year + month + day + '_' + str(time_break) + nside + 'hours.fits', HITMAP, overwrite = True)

        hp.gnomview(NAIVE, title= 'Naivemap (zoom) BINGO ' + year + '/' + month + '/' + day + ' (' + str(time_break) + ' hours) - ' + perfil, rot= (0,-17), cmap= 'jet', reso= 5, xsize= 400, ysize= 200)    #cmap = 'jet', 'cool', 'winter', 'viridis'
        # plt.show()
        plt.savefig(w_path + 'naivemap_bingo_' + year + month + day + '_' + str(time_break) + 'hours_' + perfil + '_' + str(nside) + '_zoom.png')
        plt.close()


lista = ['drectangular']#, 'rectangular']

for element in lista:
    for i in [0]:
        # print('Perfil: {0} (errado) \t\tDisplacement: {1}d'.format(element,i))
        # hitmapplot('/home/otobone/Documentos/ic/projeto_karin/exercicios/optical/sem_ajuste_horario/' + element + '/' + str(i) + 'd/2018/01/01/', element)
        
        print('Perfil: {0} \t\tDisplacement: {1}d'.format(element,i))
        hitmapplot('/home/otobone/Documentos/ic/projeto_karin/exercicios/optical/' + element + '/' + str(i) + 'd/2018/01/01/', element)


# hitmapplot('/home/otobone/Documentos/ic/projeto_karin/exercicios/optical/sem_ajuste_horario/hexagonal/0d/2018/01/01/', 'hexagonal')
# print('Perfil: hexagonal (errado) \t\tDisplacement: 0d')

# hitmapplot('/home/otobone/Documentos/ic/projeto_karin/exercicios/optical/hexagonal/0d/2018/01/01/', 'hexagonal')
# print('Perfil: hexagonal \t\tDisplacement: 0d')

# lista = pyfits.getdata('/home/otobone/Documentos/ic/projeto_karin/exercicios/optical/sem_ajuste_horario/hexagonal/0d/2018/01/01/hitmap_bingo_20180101_24.0hours.fits')

# hp.gnomview(lista, title= 'Hitmap (zoom) BINGO ',rot= (0,-17), cmap= 'jet', reso= 5, xsize= 400, ysize= 200)    #cmap = 'jet', 'cool', 'winter', 'viridis'
# # plt.savefig(w_path + 'hitmap_bingo_' + year + month + day + '_' + str(time_break) + 'hours_hexagonal_zoom.png')
# plt.show()

#Plotar espera e obtido (OK)
#Fazer um hitmap para 6 horas
#Fazer um hitmap para observação "errada"
#Fazer plots do hitmap com gnomeview ()

