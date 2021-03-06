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
	newfile = open(outputname,'wt')
	w = csv.writer(newfile, delimiter=',')
	#create a reader to read from our csv file
	oldfile = open(filename, 'rU')
	reader = csv.reader(oldfile, delimiter = ',')

	#grab first line and all of our indeces
	firstline = next(reader)
	trial_index_index = firstline.index('TRIAL_INDEX')
	transition_index = firstline.index('forward order')
	speech_onset_index = firstline.index('speech onset')
	participant_index = firstline.index('RECORDING_SESSION_LABEL')
	gaze_end_index = firstline.index('CURRENT_GAZE_END')
	biased_index = firstline.index('biased')

	#write out the column headings
	w.writerow(firstline + ['transitions before onset', 'transitions after onset', 'average biased', 'average unbiased'])

	#these are the hideous variables we will need
	lastline = firstline
	trans_before = 0
	trans_after = 0
	lines = 0
	trans_biased = 0
	trans_unbiased = 0
	num_biased = 0
	num_unbiased = 0

	#go through the csv file
	for line in reader :
		if lastline != firstline :
			if line[gaze_end_index] < line[speech_onset_index] :
				trans_before += int(line[transition_index])
			else :
				trans_after += int(line[transition_index])
			if line[biased_index] == 'y' :
				trans_biased += int(line[transition_index])
				num_biased += 1
			else:
				trans_unbiased += int(line[transition_index])
				num_unbiased += 1
			#if there's a new parcticipant
			if line[participant_index] != lastline[participant_index] :
				newline = lastline + [trans_before, trans_after, trans_biased/num_biased, trans_unbiased/num_unbiased]
				w.writerow(newline)
				trans_before = 0
				trans_after = 0
				trans_unbiased = 0
				trans_biased = 0
				num_biased = 0
				num_unbiased = 0
			else:
				w.writerow(lastline)
		lastline = line

	newfile.close()
	oldfile.close()

#here's the actual method call
if __name__ == '__main__':
	loganalyzer("forwardorder.csv", "analyzedlog.csv")
