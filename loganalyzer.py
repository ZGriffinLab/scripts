#-------------------------------------------------------------------------
# loganalyzer.py
# Ariel Sibille 2015
# Finds number of transitions before speech onset and some averages
#
#-------------------------------------------------------------------------

import csv
import re

def loganalyzer(filename, outputname) :
	#create a csv writer that will write to a file with our output name
	w = csv.writer(open(outputname,'wb'), delimiter=',')
	#create a reader to read from our csv file
	reader = csv.reader(open(filename, 'rU'), delimiter = ',')

	#grab first line and all of our indeces
	firstline_index= reader.next()
	transition_index = firstline.index('forward order')
	speech_onset_index = firstline.index('speech onset')
	participant_index = firstline.index('participant')

	#initialize our last line as the first line
	lastline = firstline
	#write out the column headings
	w.writerow(firstline + ['transitions before onset', 'average biased', 'average unbiased'])
	#go through the csv file
	for line in reader :

		lastline = line

#here's the actual method call
if __name__ == '__main__':
	loganalyzer("combinedlog.csv", "analyzedlog.csv")
