# -*- coding: utf-8 -*-
'''
Author: Carlos Otobone, João Alberto
Created at: 02/10/2020
Last Updated at: 23/10/2020
'''

#Pegar uma unica coluna do TOD, fazer um load no python e calcular a transformada de Fourier. Em função de 1/f, tal que f é a nossa frequência.
#Pegar uma unica linha do TOD, fazer um load no python e calcular a transformada de Fourier. Em função de 1/t, tal que t é o nosso tempo (frequência temporal). 

import numpy as np
import h5py
import matplotlib.pyplot as plt

def main():
    parametros = "alpha_2.0 knee_1.0 beta_1.0"
    alpha = 0.5
    beta = 1.0


    source = "/home/otobone/Documentos/ic/projeto_karin/exercicios/plots_tods/noise_test/False/" + parametros + "/2018/01/01/"

    hours = 24
    linha = np.array([])
    coluna = []
    freq = 0

    #Fixando linha e percorrendo coluna.
    for hour in range(hours):
        tod = h5py.File(source + "bingo_tod_horn_0_20180101_{:02d}0000.h5".format(hour), 'r')
        linha = np.concatenate((linha, tod["P/Phase1"][()][freq]))
        tod.close()
    print("Quantidade de elementos na linha: ", len(linha))

    #Fixando coluna e percorrendo linha.
    seconds = 36000    #Qualquer valor entre 0 e 86399.
    freqs = 30

    hour = seconds // 3600
    seconds = seconds % 3600

    for freq in range(freqs):
        tod = h5py.File(source + "bingo_tod_horn_0_20180101_{:02d}0000.h5".format(hour), "r")
        coluna.append(tod["P/Phase1"][()][freq][seconds])
        tod.close()
    print("Quantidade de elementos na coluna: ", len(coluna))

    x = np.linspace(960,1260,220)                    #x = np.array(list(range(960,1260,1)))
    xp = np.linspace(960,1260,30)                    #xp = np.array(list(range(960,1260,10)))
    print(len(xp), len(coluna))
    # coluna = np.interp(x, xp, coluna)

    plt.figure(0)
    plt.title("Frequencia Fixa - " + parametros)
    pxx, freqs = plt.psd(linha, Fs=1, NFFT=512)
    
    kf = 1000
    freq_fixo = kf*freqs ** ((beta - 1)/beta) - 1000

    # plt.plot(freqs,freq_fixo)
    # plt.legend()
    # plt.savefig(source + 'frequency_PSD.png')

    plt.figure(1)
    plt.title("Instante Fixo (interpolado) - " + parametros)
    pxx, freqs = plt.psd(coluna, Fs = 1/freqs, NFFT=512)
    
    kt = 2.5
    inst_fixo = kt*freqs ** (-alpha) - 60
    
    # plt.plot(freqs,inst_fixo)
    # plt.legend()
    # plt.savefig(source + 'time_PSD.png')
    
    plt.show()



    #Calculando a transformada de Fourier.
    # linha_fft = np.fft.fft(linha)/len(linha)
    # coluna_fft = np.fft.fft(coluna)/len(coluna)
   
    # linha_fft = abs(linha_fft[range(int(len(linha)/2))]) ** 2
    # coluna_fft = abs(coluna_fft[range(int(len(coluna)/2))]) ** 2

    # print("Transformada de Fourier na linha: ", linha_fft)
    # print("Transformada de Fourier na coluna: ", coluna_fft)
    
    # linha_freq = np.arange(int(len(linha)/2)) * 1/len(linha)
    # coluna_freq = np.arange(int(len(coluna)/2)) * 0.2/len(coluna)
    
    # plt.figure(0)
    # plt.plot(linha_freq, linha_fft)
    
    # plt.figure(1)
    # plt.plot(coluna_freq, coluna_fft)
    
    # plt.show()
    # plt.close()


main()