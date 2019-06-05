# Parser file
# Format, python parser.py FileName
import os
import sys
import ntpath

#Split-A
SATarget = "../processed_data/Split-A/"
#Split-B
SBTarget = "../processed_data/Split-B/"
#Unseen nolex
UNLTarget = "../processed_data/Unseen_nolex/"
#Unseen withlex
UWLTarget = "../processed_data/Unseen_withlex/"

#Parse all data with given params for known data sets
def parseAll(tgt, comp, order):
    #src file list
    srcList1 =  buildSrcDir(SATarget)
    srcList2 =  buildSrcDir(SBTarget)
    srcList3 =  buildSrcDir(UNLTarget)
    srcList4 =  buildSrcDir(UWLTarget)
    
    srcListAll = [srcList1, srcList2, srcList3, srcList4]
    outputList = ["A/", "B/", "UNL", "UWL"]

    for n in range(len(srcListAll)):
            
        for m in srcListAll[n]:
            target = ntpath.basename(m)
            fi = open(m, "r", encoding="utf-8")
            temp = os.path.join(tgt, outputList[n])
            if not os.path.exists(temp):
                os.makedirs(temp)
            temp = os.path.join(temp, target)
            fo = open(temp, "wb")
            if ".vi" in m:
                parseData(fi, fo, comp, order)
            elif ".en" in m:
                writeData(fi, fo)
            fi.close()
            fo.close()

#Write each individual file
def writeData(fi, fo):
    for line in fi:
        fo.write(line.encode('utf8'))

#Parse each individual file
def parseData(fi, fo, comp, order):
    for line in fi:
        temp = line
        if comp == 1:
            line = compProc(line)

        if order == 1:
            line = orderProc(line)

        fo.write(line.encode('utf8'))

#Order based parsing
def orderProc(l):
    ls = l.split(" | ")
    count = 0
    lsm = []

    while count + 2 < len(ls):
        temp = [ls[count], ls[count+1], ls[count+2]]
        lsm.append(temp)
        count = count + 3

    moved = []
    lso = []
    for i in range(len(lsm)):
        moved.append(0)

    for i in range(len(lsm)):
        for j in range(len(lsm)):
            if i < j and moved[i] == 0 and lsm[i][2] == lsm[j][0]:
                temp1 = lsm[i][0]
                temp2 = lsm[i][1]
                temp3 = lsm[i][2]
                lsm[i][0] = lsm[j][0]
                lsm[i][1] = lsm[j][1]
                lsm[i][2] = lsm[j][2]
                lsm[i][0] = temp1
                lsm[i][1] = temp2
                lsm[i][2] = temp3
                moved[i] == 1

    for i in range(len(lsm)):
        lso.append(lsm[i][0])
        lso.append(lsm[i][1])
        lso.append(lsm[i][2])

    l = (" | ".join(lso))
    
    return l

#Compression based parsing
def compProc(l):
    ls = l.split(" | ")
    count = 0
    lsm = []
    
    total = 0
    
    while count + 2 < len(ls):
        temp = [ls[count], ls[count+1], ls[count+2]]
        lsm.append(temp)
        count = count + 3

    used = []
    lso = []
    for i in range(len(lsm)):
        used.append(0)
        for j in range(len(lsm)):
            if i < j:
                if lsm[i][0] == lsm[j][0] and lsm[i][1] == lsm[j][1] and lsm[i][2] == lsm[j][2]:
                    used[i] = used[i]
                elif lsm[i][0] == lsm[j][0] and lsm[i][1] == lsm[j][1]:
                    lsm[j][2] = lsm[i][2]+" and "+lsm[j][2]
                    used[i] = 1
                    total = total + 1
                elif lsm[i][0] == lsm[j][0] and lsm[i][2] == lsm[j][2]:
                    lsm[j][1] = lsm[i][1]+" and "+lsm[j][1]
                    used[i] = 1
                    total = total + 1
                elif lsm[i][1] == lsm[j][1] and lsm[i][2] == lsm[j][2]:
                    lsm[j][0] = lsm[i][0]+" and "+lsm[j][0]
                    used[i] = 1
                    total = total + 1
        if used[i] == 0:
            lso.append(lsm[i][0])
            lso.append(lsm[i][1])
            lso.append(lsm[i][2])
            used[i] = 1

    l =  " | ".join(lso)

    return l

#Build sources from sub files in a directory
def buildSrcDir(loc):
    tgt = os.listdir(loc)
    output = []
    for d in tgt:
        d = os.path.join(loc, d)
        output.append(d)
    return output

#Standard parse
P01 = "P01/"
#Compressed parse
P02 = "P02/"
#Ordered parse
P03 = "P03/"
#Compressed and ordered parse
P04 = "P04/"

#Parsing steps
parseAll(P01, 0, 0)
parseAll(P02, 1, 0)
parseAll(P03, 0, 1)
parseAll(P04, 1, 1)
