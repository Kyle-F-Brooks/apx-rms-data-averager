import csv
import shutil
import os

def getRmsFileList(inputPath, inputType):
    fileList = []
    for filename in os.listdir(inputPath):
        if inputType in filename:
            fileList.append(filename)
    return fileList

def getFreqData(dataPath):
    freqData = []
    with open(dataPath, newline='') as csvfile:
        fileReader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in fileReader:
            print(', '.join(row))

def getSPLData(dataPath):
    splData = []
    with open(dataPath, newline='') as csvfile:
        fileReader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        trigger = False
        for row in fileReader:
            print(row)

getSPLData("Input Data\\Stasys_Xair_660SXA_REL.csv")