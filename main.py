import csv
import shutil
import os

# Function to get a list of all files to read through
def getRmsFileList(inputPath, inputType):
    fileList = [] # generate empty array
    for filename in os.listdir(inputPath): # for each file in the directory
        if inputType in filename: # if filename contains the input type
            fileList.append(filename) # append the file to the list of files
    return fileList # return the filled array

# Function to read through the passed file and extract the Frequency data
def getFreqData(dataPath):
    freqData = [] # generate empty array
    with open(dataPath, newline='') as csvfile: #open the file
        fileReader = csv.reader(csvfile, delimiter=',', quotechar='|') # read file as a csv
        trigger = False # generate a trigger to enter a loop
        for row in fileReader: # for each row of data in the file
            if trigger: # if trigger is true
                if len(row) > 0:
                    freqData.append(float(row[0])) # append frequency data to array to be returned
            elif len(row) > 0: # if row length > 0
                if 'Hz' in row[0] and 'dB' in row[1]: # search for row "Hz, dB, Hz, dB"
                    trigger = True # set trigger to true

    return freqData

# Function to read through the passed file and extract the SPL Data
def getSPLData(dataPath):
    splData = [] # generate empty array
    with open(dataPath, newline='') as csvfile: #open the file
        fileReader = csv.reader(csvfile, delimiter=',', quotechar='|') # read file as a csv
        trigger = False # generate a trigger to enter a loop
        for row in fileReader:
            if trigger: # if trigger set to true
                # log each value
                if len(row) > 0:
                    splData.append(float(row[1]))
            elif len(row) > 0: # if row length > 0
                if 'Hz' in row[0] and 'dB' in row[1]: # search for row "Hz, dB, Hz, dB"
                    # print(row [0])
                    trigger = True # set trigger to true

    return splData

def processRMS(fileList):
    allSPL = [] # generate empty array
    for file in fileList:
        splData=getSPLData("S118 Data\\%s" % file) # call getSPLData function
        allSPL.append(splData) #store data from file in allSPL
    return allSPL #return the array of all data to be averaged

def averageData(dataList):
    splDataSum = [] # generate empty array
    numOfFiles = len(dataList) # get length of input array
    for j, data in enumerate(dataList):
        for k, v in enumerate(data):
            if j > 0:
                splDataSum[k] += v # add data to splDataSum array
            else:
                splDataSum.append(v)
    avgData = [] #generate empty array
    for data in splDataSum:
        avgData.append(data/numOfFiles) # create averaged data
    
    return avgData


path = "S118 Data\\Stasys_Xair_660SXA_RMS.csv"
fileList = getRmsFileList("S118 Data\\", "RMS")
freqData = getFreqData(path)
allData = processRMS(fileList)
avgData = averageData(allData)


print(len(avgData))
# print(len(allData))
# print(len(freqData))
# print(len(splData))
# print(len(rms))