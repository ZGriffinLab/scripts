import csv

def gentest(num) :
    gazefix = open("gazefix" + str(num) + ".csv", 'w')
    loganalyzer = open("loganalyzer" + str(num) + ".csv", 'w')
    forwardorder = open("forwardorder" + str(num) + ".csv", 'w')
    logcombiner = open("logcombinertest" + str(num) + ".csv", 'w')
    firstline = "RECORDING_SESSION_LABEL,DATA_FILE,TRIAL_INDEX,imgfile,CURRENT_FIX_INTEREST_AREA_LABEL,CURRENT_FIX_INTEREST_AREA_ID,CURRENT_FIX_INDEX,CURRENT_FIX_START,CURRENT_FIX_END,CURRENT_FIX_DURATION,CURRENT_FIX_RUN_INDEX,CURRENT_FIX_RUN_DWELL_TIME,CURRENT_FIX_X,CURRENT_FIX_Y,EYE_USED".split(',')
    gfwriter = csv.writer(gazefix)
    gfwriter.writerow(firstline)
    

if __name__ == '__main__':
    gentest(1)
    gentest(2)
    gentest(3)
