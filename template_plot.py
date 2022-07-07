# -*- coding: cp1252 -*-
'''
Author: Joao Alberto
Test Version
Last Update: 16/07/2020
'''

import matplotlib.pyplot as plt

templates_path = '/home/otobone/Documentos/ic/projeto_karin/hide-master/hide/data/'
save_path = '/home/otobone/Documentos/ic/projeto_karin/exercicios/plots_templates/'

filenames = ['gain_template_fake_bingo_model_2_0.dat']
                          
templates = []
for filename in filenames:
        templates.append(open(templates_path + filename))

cols=[]                            #Lista com as colunas de cada template
for i in range(len(templates)):
        cols.append([[],[]])       #[[[],[]],[[],[]],[[],[]]]
        print(templates[i].name)
        for line in templates[i]:
                #print(line.split())
                data_0, data_1 = line.split()
                cols[i][0].append(float(data_0))
                cols[i][1].append(float(data_1))

        plt.figure(i)
        titulo_0 = ((templates[i].name).split('/'))[-1].split('.')[0]  #pega o nome do arquivo sem a extens�o com .
        titulo = 'Gain Model 2'
        #print(title)
        plt.title(titulo)
        plt.plot(cols[i][0],cols[i][1])
        plt.xlabel('Frequency (MHz)')
        plt.ylabel('Gain')
        #plt.show()
        plt.savefig(save_path + titulo_0 + '.png')
        plt.close(i)
        
