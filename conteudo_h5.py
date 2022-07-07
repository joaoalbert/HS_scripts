import h5py


#Observacao: nunca havia visto um loop com o comando with.

with h5py.File("/home/otobone/Documentos/ic/projeto_karin/exercicios/2018/01/01/bingo_tod_horn_0_20180101_120000.h5", "r") as fp:
  
    tod = fp["P/Phase1"][()]
    time = fp["TIME"][()]
    
    print(fp)	#aparentemente retorna o endereco do fp
		
	
