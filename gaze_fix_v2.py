#-------------------------------------------------------------------------
# gaze_fix_v2.py
# Ariel Sibille 2015
# Calculates total gaze duration on an interest area. Will not filter out
# fillers for you!
#
#-------------------------------------------------------------------------

import csv
import re

def gaze_fix_v2(filename, outputname) :
	#create a csv writer that will write to a file with our output name
	w = csv.writer(open(outputname,'wb'), delimiter=',')
	#create a reader to read from our csv file
	reader = csv.reader(open(filename, 'rU'), delimiter = ',')
	firstline = reader.next()
	trial_index_index = firstline.index('TRIAL_INDEX')
	fix_area_label_index = firstline.index('CURRENT_FIX_INTEREST_AREA_LABEL')
	gaze_start_index = firstline.index('CURRENT_FIX_START')
	gaze_end_index = firstline.index('CURRENT_FIX_END')
	#set up our gaze start at 0
	gaze_start = 0
	#initialize our last line as the first line
	lastline = firstline
	#write out the column headings
	w.writerow(['TRIAL_INDEX', 'CURRENT_FIX_INTEREST_AREA_LABEL', 'CURRENT_GAZE_START', 'CURRENT_GAZE_END'])
	#go through the csv file
	for line in reader :
		#if there's a new trial
		if lastline != firstline and line[trial_index_index] != lastline[trial_index_index] :
			#change non-IA stuff to "other"
			if(lastline[fix_area_label_index] == '.') :
					lastline[fix_area_label_index] = 'other'
			newline = [lastline[trial_index_index], gaze_start, lastline[gaze_end_index], int(lastline[gaze_end_index]) - int(gaze_start)]
			w.writerow(newline)
			gaze_start = 0
		else:
			#if the interest area has changed
			if line[fix_area_label_index] != lastline[fix_area_label_index] and lastline != firstline:
				#this is where we change the non-IA stuff to "other"
				if(lastline[fix_area_label_index] == '.') :
						lastline[fix_area_label_index] = 'other'
				newline = [lastline[trial_index_index], gaze_start, lastline[gaze_end_index], int(lastline[gaze_end_index]) - int(gaze_start)]
				w.writerow(newline)
				gaze_start = line[gaze_start_index]
		lastline = line

#here's the actual method call
gaze_fix_v2("fixation_s01-s19-3.csv", "results.csv")
