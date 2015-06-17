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
	w = csv.writer(open(outputname,'wt'), delimiter=',')
	#create a reader to read from our csv file
	reader = csv.reader(open(filename, 'rU'), delimiter = ',')

	#grab first line and all of our indeces
	firstline = next(reader)
	trial_index_index = firstline.index('trial')
	transition_index = firstline.index('forward order')
	speech_onset_index = firstline.index('speech onset')
	participant_index = firstline.index('participant')
	rt_index = firstline.index('response time')

	#write out the column headings
	w.writerow(firstline + ['transitions before onset', 'transitions after onset', 'average biased', 'average unbiased'])

	lastline = firstline
	trans_before = 0
	trans_after = 0
	lines = 0
	avg_biased = 0
	avg_unbiased = 0

	#go through the csv file
	for line in reader :
		if lastline != firstline :
			if line[rt_index] < line[speech_onset_index] :
				trans_before = trans_before + int(line[transition_index])
			else :
				trans_after = trans_after + int(line[transition_index])
			#if there's a new parcticipant
			if line[participant_index] != lastline[participant_index] :
				newline = [lastline + [trans_before, trans_after, avg_biased, avg_unbiased]]
				w.writerow(newline)
			else:
				w.writerow(lastline)
		lastline = line

#here's the actual method call
if __name__ == '__main__':
	loganalyzer("combinedlog.csv", "analyzedlog.csv")
