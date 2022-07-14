A) Creating Python Environment:

	1) A Python environment allows for project isolation.
	
	2) To create a Python environment, go to the folder in which you wish to leave the 
	environment, and execute:
	
	$ python3 -m venv <env-name>
	
	in which <env-name> is the chosen name for the environment. The convention is "venv".
	
	3) To activate the environment:
	
	$ source <env-name>/bin/activate
	
	4) To deactivate the environment:
	
	$ deactivate
	
	
B) Installing Ivy:

	1) Clone Ivy from Github:
	
	$ git clone https://github.com/zxcorr/ivy.git 
	
	2) Install requirements:
	
	$ pip3 install -r requirements.txt
	
	3) Install Ivy:
	
	$ python3 setup.py install
	$ python3 setup.py develop
	
	Develop mode creates a link between the local files and the ones inside the environment, allowing one to change the files locally and having the modifications applied imediately without having to install again.
	
	
C) Installing Hide:

	1) Clone Hide from Github:
	
	$ git clone https://github.com/zxcorr/hide.git 
	
	2) Install requirements:
	
	$ pip3 install -r requirements.txt
	# (!) the line trying to install ivy should be commented
	
	3) Install Hide:
	
	$ python3 setup.py install
	$ python3 setup.py develop
	
D) Running HIDE:

	1) Optional: Run hide/data/make_fake_bingo_model_X.py to produce gain, noise, background and RFI 
	data for all horns.
	
	- Alternatively, comment the plugins "apply_gain", "add_background", "background_noise"
	to ignore these parameters.
	
	2) Change bingo.py:
	
	- output path
	- map
	
	3) Change run_hide.py:
	
	- model
	- destination path
	 

