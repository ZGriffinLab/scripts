#----------------------------
# renamer.py
# Ariel Sibille 2015
# renames all the files in a
# folder. intended for when
# you mess up a ptcpt name
#----------------------------

import os

def renamer () :
	for filename in os.listdir(".") :
		if filename.startswith("wrong prefix here ex: c02") :
			os.rename(filename, "actual prefix here ex: s02" + filename[3:])
			
if __name__ == '__main__':
	renamer()
