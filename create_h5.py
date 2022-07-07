import h5py
import numpy as np

filename = "nome.h5"
Nframes = ? # numero de dados
frequencia_do_GEM = ?
tempos = [] # lista com o instante de tempo de cada frame


tod1 = h5py.File(filename,"w")

tod1.create_dataset("FREQUENCY",(1,),dtype="f")
tod1.create_group("T")
tod1.create_dataset("TIME",(3600,),dtype="f")

tod1["FREQUENCY"] = frequencia_do_GEM
tod1["TIME"] = tempos

tod1["T"].create_dataset("T1",(1,Nframes),dtype="f")
tod1["T"].create_dataset("T2",(1,Nframes),dtype="f")
tod1["T"].create_dataset("T3",(1,Nframes),dtype="f")
tod1["T"].create_dataset("T4",(1,Nframes),dtype="f")
