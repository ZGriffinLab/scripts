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

#here's the actual method call
if __name__ == '__main__':
    logcombiner("results.csv", "combinedlog.csv")
