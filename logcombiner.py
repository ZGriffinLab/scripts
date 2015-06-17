#-------------------------------------------------------------------------
# logcombiner.py
# Ariel Sibille 2015
# Combines experimental log with eyetracker log.
#
#-------------------------------------------------------------------------

import csv
import re
import os

def logcombiner(filename, outputname) :

	#create a csv writer that will write to a file with our output name
	w = csv.writer(open(outputname,'w', newline=''), delimiter=',')

	#create a reader to read from our csv file
	reader = csv.reader(open(filename, 'rU'), delimiter = ',')

	#we'll be looking for exp data files so we compile this
	p = re.compile('exp_data')

	#get the first line in the csv file
	currline = reader.__next__()
	#get the index of the image file field in the csv file
	imgindex = currline.index('imgfile')
	labelindex = currline.index('CURRENT_FIX_INTEREST_AREA_LABEL')
	#get the first line of actual data from the csv file
	currline = reader.__next__()

	#go through the participants folder
	for dirname in os.listdir("../experiment files/participants") :
		#join the directory name to the rest of the path
		directory = os.path.join('../experiment files/participants', dirname)
		#we don't want to try to navigate through something in the participants folder that isn't a dir
		if os.path.isdir(directory) :
			#for every participants folder, we look for the exp data file
			for file in os.listdir(directory) :
				#if the file is the exp data file
				if p.search(file) :
					#create a reader to read from our exp data file
					logreader = open(os.path.join(directory, file), 'rU')
					#splitting the current line by tabs
					currlogline = logreader.readline().split('\t')

					#finding indeces of all the good stuff that we want
					logimgindex = currlogline.index('stim_file_name')
					biasedindex = currlogline.index('biased')
					onsetindex = currlogline.index('response time')

					w.writerow(currlogline[:-2] + ['biased','speech onset', 'forward order'])

					currlogline = logreader.readline().split('\t')

					#go through the exp data file
					for line in logreader :
						lastlogline = currlogline
						currlogline = line.split('\t')
						#if the image files match, minus the extensions
						try:
							while currline[imgindex][:-3] == lastlogline[logimgindex][:-3] :
								lastline = currline
								currline = reader.__next__()
								forwardorder = 0
								if (lastline[labelindex] == 'patient' and currline[labelindex] == 'recipient') or (lastline[labelindex] == 'recipient' and currline[labelindex] == 'patient') :
									forwardorder = 1
								newline = lastline[:-1] + [lastlogline[biasedindex], lastlogline[onsetindex], forwardorder]
								w.writerow(newline)
						#have to catch reader's stopiteration exception
						except Exception as e:
							pass

#here's the actual method call
logcombiner("results.csv", "combinedlog.csv")
