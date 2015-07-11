#-------------------------------------------------------------------------
# gaze_fix.py
# Ariel Sibille 2015
# Strips RS CSV of its filler files and calculates total gaze duration on
# an interest area.
#
#-------------------------------------------------------------------------

import csv
import re

def gaze_fix(filename, outputname) :
	#create a csv writer that will write to a file with our output name
	w = csv.writer(open(outputname,'w', newline=''), delimiter=',')
	#create a reader to read from our csv file
	reader = csv.reader(open(filename, 'rU'), delimiter = ',')

	#use regex to come up with a thing to check strings against
	p = re.compile('stimuli/visual/f')

	#get first line and variable indeces
	firstline = reader.__next__()
	stim_index = firstline.index('imgfile')
	label_index = firstline.index('CURRENT_FIX_INTEREST_AREA_LABEL')
	label_id_index = firstline.index('CURRENT_FIX_INTEREST_AREA_ID')
	gaze_start_index = firstline.index('CURRENT_FIX_START')
	gaze_end_index = firstline.index('CURRENT_FIX_END')

	#set up our gaze start at 0
	gaze_start = 0
	#initialize our last line as an empty list
	lastline = firstline
	#write column headings to results
	headings = ['RECORDING_SESSION_LABEL', 'DATA_FILE', 'TRIAL_INDEX', 'imgfile', 'CURRENT_FIX_INTEREST_AREA_LABEL', 'CURRENT_FIX_INTEREST_AREA_ID', 'CURRENT_FIX_INDEX', 'CURRENT_GAZE_START', 'CURRENT_GAZE_END', 'CURRENT_GAZE_DUR', 'CURRENT_FIX_RUN_INDEX']
	w.writerow(headings)
	#go through the csv file
	for line in reader :
		#if the line doesn't have a filler in the variable name
		if not p.match(line[stim_index]):
			#if the last line wasn't recording session label and if the stimulus has changed
			if lastline != firstline and line[stim_index] != lastline[stim_index] :
					if(lastline[label_index] == '.') :
							lastline[label_index] = 'other'
							lastline[label_id_index] = 4
					newline = lastline[:-8] + [gaze_start, lastline[gaze_end_index], int(lastline[gaze_end_index]) - int(gaze_start), 1]
					w.writerow(newline)
					gaze_start = 0
			else:
				#if the interest area has changed
				if line[label_index] != lastline[label_index] and lastline != firstline:
					total = int(lastline[gaze_end_index]) - int(gaze_start)
					#this is where we change the non-IA stuff to "other"
					if(lastline[label_index] == '.') :
						lastline[label_index] = 'other'
						lastline[label_id_index] = 4
					newline = lastline[:-8] + [gaze_start, lastline[gaze_end_index], total, 1]
					w.writerow(newline)
					gaze_start = line[gaze_start_index]
			lastline = line

#here's the actual method call
if __name__ == '__main__':
	gaze_fix("fixation_s01-s19-3.csv", "results1.csv")
