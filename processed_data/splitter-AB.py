# dev/train/test splitter
# input     -> contents of unprocessed_data
# output    -> Split-A with 10/80/10 dev/train.test split
#           -> Split-B with 10/85/5 dev/train.test split

import os
import sys
import xml.etree.ElementTree as et

# Insert method for writing files for basic parsing
def insertToFile(mts, lex, fi, fi2, c):
    printTab = 0
    for row in mts:
        printTab = printTab + 1
        if printTab > 1:
            fi.write(" | ".encode('utf8'))
        elif (c != 1):
            fi.write("\n".encode('utf8'))
            fi2.write("\n".encode('utf8'))
        fi.write(row.text.encode('utf8'))
    fi2.write(lex.text.encode('utf8'))

# Insert method for writing files without lex entries for basic parsing
def insertToFileNL(mts, fi, c):
    printTab = 0

    for row in mts:
        printTab = printTab + 1
        if printTab > 1:
            fi.write(" | ".encode('utf8'))
        if (c != 1):
            fi.write("\n".encode('utf8'))
        fi.write(row.text.encode('utf8'))

# Method to build files from a directory
def buildFile(src, devE, devV, trainE, trainV, testE, testV, devN, testN):
    devC = 0
    for data in src:
        mts = 0
        count = 0
        trainC = 0
        testC = 0
        tree = et.parse(data)
        root = tree.getroot()
        for bm in root:
            for ents in bm:
                for ent in ents:
                    if ent.tag == "modifiedtripleset":
                        mts = ent
                        count = count + 1
                    if ent.tag == "lex":
                        lex = ent
                        if count % 20 in devN:
                            devC = devC + 1
                            insertToFile(mts, lex, devV, devE, devC)
                        elif count % 20 in testN:
                            testC = testC + 1
                            insertToFile(mts, lex, testV, testE, testC)
                        else:
                            trainC = trainC + 1
                            insertToFile(mts, lex, trainV, trainE, trainC)

# Method to build files from a single file
def buildFileSingle(src, testE, testV):
    mts = 0
    testC = 0
    tree = et.parse(src)
    root = tree.getroot()
    for bm in root:
            for ents in bm:
                for ent in ents:
                    if ent.tag == "modifiedtripleset":
                        mts = ent
                    if ent.tag == "lex":
                        lex = ent
                        testC = testC + 1
                        insertToFile(mts, lex, testV, testE, testC)

# Method to build files from a single file with no lex entries
def buildFileSingleNL(src, testV):
    mts = 0
    testC = 0
    tree = et.parse(src)
    root = tree.getroot()
    for bm in root:
            for ents in bm:
                for ent in ents:
                    if ent.tag == "modifiedtripleset":
                        mts = ent
                        testC = testC + 1
                        insertToFileNL(mts, testV, testC)

#Build sources from sub files in a directory
def buildSrcDir(tgt, loc):
    output = []
    for d in tgt:
        d = os.path.join(loc, d)
        temp = os.listdir(d)
        for t in temp:
            output.append(os.path.join(d, t))
    return output

# Data split by using modulo 20 division on count
# Split-A
splitAModDev = [3, 7]
splitAModTest = [11, 13]

# Split-B
splitBModDev= [2, 17]
splitBModTest = [5]
        
# Output for Split-A
AdevE = open("Split-A/dev.en","wb")
AdevV = open("Split-A/dev.vi","wb")
AtrainE = open("Split-A/train.en","wb")
AtrainV = open("Split-A/train.vi","wb")
AtestE = open("Split-A/test.en","wb")
AtestV = open("Split-A/test.vi","wb")

# Output for Split-B
BdevE = open("Split-B/dev.en","wb")
BdevV = open("Split-B/dev.vi","wb")
BtrainE = open("Split-B/train.en","wb")
BtrainV = open("Split-B/train.vi","wb")
BtestE = open("Split-B/test.en","wb")
BtestV = open("Split-B/test.vi","wb")

# Collect folders in target area
dataLoc = "../unprocessed_data/webnlg-corpus-release/"
dirDataLoc = os.listdir(dataLoc)
tgtDataLoc = buildSrcDir(dirDataLoc, dataLoc)

# Build Split-A
buildFile(tgtDataLoc, AdevE, AdevV, AtrainE, AtrainV, AtestE, AtestV, splitAModDev, splitAModTest)

# build Split-B
buildFile(tgtDataLoc, BdevE, BdevV, BtrainE, BtrainV, BtestE, BtestV, splitBModDev, splitBModTest)

# Close Split-A files
AdevE.close()
AdevV.close()
AtrainE.close()
AtrainV.close()
AtestE.close()
AtestV.close()

# Close Split-B files
BdevE.close()
BdevV.close()
BtrainE.close()
BtrainV.close()
BtestE.close()
BtestV.close()

#Testdata_withlex
dataWLLoc = "../unprocessed_data/testdata_unseen_with_lex.xml"

WLtestE = open("Unseen_withlex/test.en","wb")
WLtestV = open("Unseen_withlex/test.vi","wb")

buildFileSingle(dataWLLoc, WLtestE, WLtestV)

WLtestE.close()
WLtestV.close()

#Testdata_nolex
dataNLLoc = "../unprocessed_data/testdata_no_lex.xml"

NLtestV = open("Unseen_nolex/test.vi","wb")

buildFileSingleNL(dataWLLoc, NLtestV)

NLtestV.close()















