import csv
import os

from tkinter import filedialog as fd

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

def processRMS(fileList, path):
    allSPL = [] # generate empty array
    for file in fileList:
        splData=getSPLData("%s\\%s" % (path, file)) # call getSPLData function
        allSPL.append(splData) #store data from file in allSPL
    return allSPL #return the array of all data to be averaged

def averageData(dataList, dataLen):
    splDataSum = [] # generate empty array
    numOfProcessed = 0
    for j, data in enumerate(dataList):
        if len(data) == dataLen:
            for k, v in enumerate(data):
                if j > 0:
                    splDataSum[k] += v # add data to splDataSum array
                else:
                    splDataSum.append(v)
            numOfProcessed += 1
    avgData = [] #generate empty array
    for data in splDataSum:
        avgData.append(data/numOfProcessed) # create averaged data
    return avgData

def sortData(freqData, avgData, dataPath):
    sortedData = []
    #insert headers from the normal file here
    sortedData.append(['RMS Level','','',''])
    sortedData.append(['Ch1 (XLR - Bal)','','Ch2 (XLR - Bal)',''])
    sortedData.append(['X','Y','X','Y'])
    sortedData.append(['Hz','dBSPL','Hz','dBSPL'])
    for k,v in enumerate(freqData):
        row = [v,avgData[k],'','']
        sortedData.append(row)
    return sortedData

def createCSV(newFilePath, sortedData):
    with open(newFilePath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(sortedData)
    print(f"CSV File Successfully Created")


path = fd.askdirectory(title="Select source folder", initialdir = '/')
# path = "Airten_V3\\"
freqFile = fd.askopenfilename(title='Open Latest Measured File', initialdir='/', filetypes=[('CSV Files', '*.csv')])
# freqFile = "%sAirten_V3_A6T1613_RMS.csv" % path
fileList = getRmsFileList(path, "RMS")
freqData = getFreqData(freqFile)
allData = processRMS(fileList, path)
avgData = averageData(allData, len(freqData))
sortedData = sortData(freqData,avgData, freqFile)
createCSV("AverageData.csv", sortedData)

# print(avgData)
# print(len(avgData))
# print(len(allData))
# print(len(freqData))
# print(len(splData))
# print(len(rms))