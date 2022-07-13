# -*- coding: cp1252 -*-            #Comando para aceitar o João.
'''
Created on 09/08/2020
Last update 13/08/2020

Author: Carlos Otobone, João Alberto
'''

# definir a posição geografica do BINGO.                                         
# definir as posicoes (-2d, -d, 0 ,d, 2d).
# separar as cornetas usando corn % 5 (resto).
# usar funcao do HIDE para trocar (RA, DEC) para (altitude, azimuth).
# alimentar os arquivos azimuth.txt e altitude.txt. 

from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.coordinates import EarthLocation
from astropy.coordinates import AltAz
from astropy.time import Time
import numpy as np


def main(w_path, d_path, GEO, date, perfil, displacement):
    '''
    w_path: caminho dos arquivos celestial_coor.txt.\n
    d_path: caminho dos arquivos azimuth.txt e altitude.txt.\n
    GEO: [latitude, longitude, elevation]\n
    date: formato '2018-01-01 18:00'\n 
    displacement: deslocamento da corneta (-2d, -1d, 0d, 1d. 2d)\n
    perfil: celestial_coor_X.txt\n
    '''
    
    telescope_latitude = GEO[0]      # sul-norte.
    telescope_longitude = GEO[1]     # oeste-leste.
    telescope_elevation = GEO[2]
    time = Time(date)     # formato '2018-01-01 18:00'
    
    celestial_coor = []
    alt_az = []

    lines = np.loadtxt(w_path + perfil)      # Lista com as linhas do arquivo do Pablo.

    if (perfil == 'hexagonal.txt'):
        print ("Coletando coordenadas RA(deg) DEC(deg)...")
        for line in lines:
            celestial_coor.append([line[1],line[2]])
        
    else:
        resto = ((displacement + 3) % 5)
        print ("Coletando coordenadas RA(deg) DEC(deg)...")

        for line in lines:
            if (line[0] % 5 == resto):
                celestial_coor.append([line[1],line[2]])
    
    print ("Salvando coordenadas Alt(deg), Az(deg)...")
    for line in celestial_coor:
        alt_az.append(RAdec2AltAz(line[0], 
        						  line[1], 
        						  telescope_latitude, 
        						  telescope_longitude, 
        						  telescope_elevation, 
        						  time))
        
    print ("Numero de cornetas: " + str(len(celestial_coor)))

    alt_txt = open(d_path + "altitude.txt", "w")
    az_txt = open(d_path + "azimuth.txt", "w")

    alt_txt.write("#Altitude of each horn")
    az_txt.write("#Azimuth of each horn")
    
    for coord in alt_az:
        alt_txt.write("\n" + str(coord[0]))
        az_txt.write("\n" + str(coord[1]))

    alt_txt.close()
    az_txt.close()


def RAdec2AltAz(RA, dec, latitude, longitude, elevation, time):
    
    loc = EarthLocation(lat=latitude, lon=longitude, height=elevation * u.m)
    aa = AltAz(location=loc, obstime=time)

    obj_dir = SkyCoord(RA * u.deg, dec * u.deg, frame='icrs')
    obj_altaz = obj_dir.transform_to(aa)

    alt = float(np.array(obj_altaz.alt))
    az = float(np.array(obj_altaz.az))

    return [alt, az]



def plotdisp(txt_path, perfil, displacement, d_path=None):
	'''
	Recebe um txt com o numero da corneta, o RA e a DEC,
	e plota a disposição para um displacement especifico.
	(Não tem a ver com TOD.)
	
	txt_path: diretorio com o txt.
	perfil: "hexagonal", "rectangular", "drectangular".
	displacement: -2, -1, 0, 1, 2.
	d_path: destination path.
	'''
	
	if d_path==None: d_path = txt_path
	
	print ("Coletando RA (deg) e DEC (deg)...")
	lines = np.loadtxt(txt_path + perfil + '.txt')
	lines = lines[lines[:,0].argsort()] # Organizando por numero da corneta
	
	RA = []
	DEC = []
	NUMBER = []	
	
	if (perfil == 'hexagonal'):
		displacement = 0 
		for line in lines:
			RA.append(line[1])
			DEC.append(line[2])
			NUMBER.append(line[0])
	   
	else:
		resto = ((displacement + 3) % 5)
		for line in lines:
			if (line[0] % 5 == resto):
				RA.append(line[1])
				DEC.append(line[2])
				NUMBER.append(line[0] // 5 + 1)
							
	print("Plotando gráfico...")			
	fig, ax = plt.subplots() 
	ax.scatter(RA, DEC, s=1000)

	for i in range (len(NUMBER)):
		ax.annotate(int(NUMBER[i]), (RA[i], DEC[i]))
	
	
	if (perfil == 'hexagonal'):
	
		plt.title(perfil.title())
		plt.xlabel('RA (deg)')
		plt.ylabel('DEC (deg)')
		plt.savefig(d_path + perfil + '.png')

	elif (perfil == 'rectangular'):
	
		plt.title(perfil.title() + ' ' + str(displacement) + 'd')
		plt.xlabel('RA (deg)')
		plt.ylabel('DEC (deg)')
		plt.savefig(d_path + perfil + str(displacement) + 'd.png')

	else:
	
		plt.title("Double Rectangular " + str(displacement) + 'd')
		plt.xlabel('RA (deg)')
		plt.ylabel('DEC (deg)')
		plt.savefig(d_path + perfil + str(displacement) + 'd.png')



if __name__=="__main__":

	GEO = [-7.0, -38.0, 0.0]
	w_path = "/home/joao/Documentos/cosmologia/hide_and_seek/resultados/optical/"  # caminho dos arquivos celestial_coor.txt (arquivos do Pablo).
	d_path = "/home/joao/Documentos/cosmologia/hide_and_seek/hide-master/"     # caminho dos arquivos azimuth.txt e altitude.txt.
	perfil = 'drectangular.txt'
	displacement = -2
	date = '2018-01-01 19:47'
	
	

	# l = ['hexagonal', 'drectangular', 'rectangular']
	# for elements in l:

	#	 if (elements == 'hexagonal'):
	#		 plotdisp("/home/otobone/Documentos/ic/projeto_karin/exercicios/optical/", 'hexagonal', 0)
	#	 else:
	#		 for d in range(-2,3):
				# plotdisp("/home/otobone/Documentos/ic/projeto_karin/exercicios/optical/", elements, d)
				
	#plotdisp("/home/joaoalb/Documents/Cosmologia/hide_and_seek/resultados/TOD/optical/", "rectangular", -2, "/home/joaoalb/Documents/Cosmologia/hide_and_seek/resultados/")


	main(w_path, d_path, GEO, date, perfil, displacement)
