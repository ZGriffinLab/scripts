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
	w = csv.writer(open(outputname,'wb'), delimiter=',')
	#create a reader to read from our csv file
	reader = csv.reader(open(filename, 'rU'), delimiter = ',')
	#use regex to come up with a thing to check strings against
	p = re.compile('stimuli/visual/f')
	firstline = reader.next()
	#set up our gaze start at 0
	gaze_start = 0
	#initialize our last line as an empty list
	lastline = firstline
	#write column headings to results
	w.writerow(['RECORDING_SESSION_LABEL', 'DATA_FILE', 'TRIAL_INDEX', 'imgfile', 'CURRENT_FIX_INTEREST_AREA_LABEL', 'CURRENT_FIX_INTEREST_AREA_ID', 'CURRENT_FIX_INDEX', 'CURRENT_GAZE_START', 'CURRENT_GAZE_END', 'CURRENT_GAZE_DUR', 'CURRENT_FIX_RUN_INDEX'])
	#go through the csv file
	for line in reader :
		#if the line doesn't have a filler in the variable name
		if not p.match(line[3]):
			#if the last line wasn't recording session label and if the stimulus has changed
			if lastline != firstline and line[3] != lastline[3] :
					if(lastline[4] == '.') :
							lastline[4] = 'other'
							lastline[5] = 4
					newline = [lastline[0], lastline[1], lastline[2], lastline[3], lastline[4], lastline[5], lastline[6], gaze_start, lastline[8], int(lastline[8]) - int(gaze_start), 1]
					w.writerow(newline)
					gaze_start = 0
			else:
				#if the interest area has changed
				if line[4] != lastline[4] and lastline != firstline: 
					total = int(lastline[8]) - int(gaze_start)
					#this is where we change the non-IA stuff to "other"
					if(lastline[4] == '.') :
						lastline[4] = 'other'
						lastline[5] = 4
					newline = [lastline[0], lastline[1], lastline[2], lastline[3], lastline[4], lastline[5], lastline[6], gaze_start, lastline[8], total, 1]
					w.writerow(newline)
					gaze_start = line[7]
			lastline = line

#here's the actual method call
gaze_fix("fixation_s01-s19-3.csv", "results.csv")

#crucial and consistent variables: trial index, fixation area label,fixation start and fixation end
