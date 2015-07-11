#-------------------------------------------------------------------------
# logcompleter.py
# Ariel Sibille 2015
# Runs all log functions for an edf file and outputs result to
# filename-1.csv. All functions in file so that this can be easily used for
# any eyetracker experiment. However, programmer may want to replace
# gaze_fix with more generic function gaze_fix_v2 (found in gaze_fix_v2.py)
# because gaze_fix is optimized for Rolling Stone.
#
#-------------------------------------------------------------------------

import sys
import csv
import re
import os

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
    firstline = currline
    currline = reader.__next__()

    first = 1

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

                    if first :
                        w.writerow(firstline[:-1] + ['biased','speech onset'])
                        first = 0

                    #go through the exp data file
                    for line in logreader :
                        currlogline = line.split('\t')
                        #if the image files match minus the extensions
                        while currline[imgindex][:-3] == currlogline[logimgindex][:-3] :
                            newline = currline[:-1] + [currlogline[biasedindex], currlogline[onsetindex]]
                            w.writerow(newline)
                            try:
                                currline = reader.__next__()
                            #have to catch reader's stopiteration exception
                            except Exception as e:
                                #changes the img name to end to break us out of the while loop
                                currline[imgindex] = "end"

def forwardorder(filename, outputname) :
    #create a csv writer that will write to a file with our output name
    w = csv.writer(open(outputname,'w', newline=''), delimiter=',')

    #create a reader to read from our csv file
    reader = csv.reader(open(filename, 'rU'), delimiter = ',')

    #get the first line in the csv file
    currline = reader.__next__()
    #get the index of the image file field in the csv file
    labelindex = currline.index('CURRENT_FIX_INTEREST_AREA_LABEL')

    first = 1

    for line in reader :
        forwardorder = 0
        if first :
            w.writerow(currline + ['forward order'])
            lastline = reader.__next__()
            first = 0
        else :
            if (lastline[labelindex] == 'patient' and line[labelindex] == 'recipient') or (lastline[labelindex] == 'recipient' and line[labelindex] == 'patient') :
                forwardorder = 1
            newline = lastline + [forwardorder]
            w.writerow(newline)
            lastline = line

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
            #adds transition value to before or after
			if line[gaze_end_index] < line[speech_onset_index] :
				trans_before += int(line[transition_index])
			else :
				trans_after += int(line[transition_index])
            #adds transition value to biased or unbiased
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

def logcompleter(filename) :
    gaze_fix(filename, filename[:-4] + '-1.csv')
    logcombiner(filename[:-4] + '-1.csv', filename[:-4] + '-2.csv')
    forwardorder(filename[:-4] + '-2.csv', filename[:-4] + '-1.csv')
    loganalyzer(filename[:-4] + '-1.csv', filename[:-4] + '-2.csv')

    os.rename(filename[:-4] + '-2.csv', filename[:-4] + '-1.csv')

if __name__ == '__main__':
	logcompleter(sys.argv[1])
