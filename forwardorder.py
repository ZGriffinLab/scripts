#-------------------------------------------------------------------------
# forwardorder.py
# Ariel Sibille 2015
# Determines forward order of gaze transitions.
#
#-------------------------------------------------------------------------

import csv
import re
import os

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

#here's the actual method call
if __name__ == '__main__':
    forwardorder("combinedlog.csv", "forwardorder.csv")
