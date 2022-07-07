# -*- coding: cp1252 -*-            #Comando para aceitar o João.

'''
Created on 13/07/2020
Last update 27/07/2020

Author: Carlos Otobone, João Alberto
'''

import numpy as np
import os


azs = np.arange(0,360,60)       #cria vetor == [0, 60, 120, 180, 240, 300]
als = np.arange(0,120,30)       #cria vetor == [0, 30, 60, 90]

output_path = "/home/otobone/Documentos/ic/projeto_karin/exercicios/azimuth_altitude/"      
working_path = "/home/otobone/Documentos/ic/projeto_karin/hide-master/"
print(azs, als)
for az in azs:
    for al in als:
        dire = "az" + str(az) + "_al" + str(al)     #variável com o diretório para criar a pasta
        os.system("mkdir -p " + output_path + dire + "/")    #cria a pasta

        azimuth = open(working_path + "azimuth.txt", "w")   #abre o arquivo no modo escrita
        azimuth.write("#Azimuth of each horn\n" + str(az))       #altera os valores no arquivo
        azimuth.close()

        altitude = open(working_path + "altitude.txt", "w")       #abre o arquivo no modo escrita
        altitude.write("#Altitude of each horn\n" + str(al))          #altera os valores no arquivo
        altitude.close()

        with open(working_path + "hide/config/bingo.py", "r") as bingo_read:    #abre o endereço e salva na variável 'bingo_read' 
            bingo_lines = bingo_read.readlines()        #salvando as linhas do bingo_read como uma lista no bingo_lines
            bingo_read.close()

        bingo = open(working_path + "hide/config/bingo.py", "w")        #abre o bingo.py no modo leitura

        for line in bingo_lines:
            if (line[0:11] == "output_path"):       #procura a string 'output_path' com até o elemento com indice 11
                bingo.write('output_path = "'+ output_path + dire + '"  # path to output folder\n')       #altera o conteúdo do output_path com base no que está definido
            else:
                bingo.write(line)   #escreve todas as outras linhas que não alteramos. A ausência desse comando irá APAGAR todas as outras linhas do arquivo bingo.py
        bingo.close()

        os.chdir(working_path)
        os.system("python2 run_hide.py")

