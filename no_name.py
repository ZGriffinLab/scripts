#-------------------------------------------------------------------------
#no_name.py
#Ariel Sibille 2015
#a file that will go in and fill in all of the no_names for you when
#you're done coding responses for brother
#if can also be used for other files if you tweak the index values
#write your file names where testing and testresult are; i would
#suggest making these different names because you wouldn't want to
#rename your original file. then you can rename the final file afterwards
#-------------------------------------------------------------------------


import csv

def no_name(filename, outputname) :
	w = csv.writer(open(outputname,'wb'), delimiter=',')
	reader = csv.reader(open(filename, 'rU'), delimiter = ',')
	for splitline in reader :
		if len(splitline) < 8 :
			pass
		elif splitline[7] == '0' and splitline[8] == '' :
			splitline[8] = 'no_name'
		elif splitline[9] == '0' and splitline[10] == '' :
			splitline[10] = 'no_name'
		else :
			pass
		w.writerow(splitline)

if __name__ == '__main__':
	no_name("brother_descriptions_for_ariel_tricia.csv", "brother_descriptions_for_ariel_tricia_1.csv")
	
