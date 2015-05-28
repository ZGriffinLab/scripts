import os

def renamer () : 
	for filename in os.listdir(".") :
		if filename.startswith("c02") : 
			os.rename(filename, "s02" + filename[3:])
			
renamer()
	