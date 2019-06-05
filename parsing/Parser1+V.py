# Parser file
# Format, python parser.py FileName
import os
import sys
import ntpath

sys.path.append("../vocab/")

import vocab

#Split-A
SATarget = "../processed_data/Split-A/"
#Split-B
SBTarget = "../processed_data/Split-B/"
#Unseen nolex
UNLTarget = "../processed_data/Unseen_nolex/"
#Unseen withlex
UWLTarget = "../processed_data/Unseen_withlex/"

#Parse all data with given params for known data sets
def parseAll(tgt, voc):
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
                parseData(fi, fo, voc)
            elif ".en" in m:
                writeData(fi, fo, voc)
            fi.close()
            fo.close()

#Write each individual file
def writeData(fi, fo, voc):
    for line in fi:
        g = vocab.Generator('x', 'x')
        if voc == 0:
            line = ' '.join(g.get_ens_from_sentence_with_method(line, g.Method.SPACE_SPLIT))
        if voc == 1:
            line = ' '.join(g.get_ens_from_sentence_with_method(line, g.Method.SPACE_SPLIT_NO_PUNCT))
        if voc == 2:
            line = ' '.join(g.get_ens_from_sentence_with_method(line, g.Method.SPACE_SPLIT_NO_PUNCT_POSSESSIVES))
        if voc == 3:
            line = ' '.join(g.get_ens_from_sentence_with_method(line, g.Method.SPACE_SPLIT_NO_PUNCT_FIX))
        if voc == 4:
            line = ' '.join(g.get_ens_from_sentence_with_method(line, g.Method.SPACE_SPLIT_NO_PUNCT_POSSESSIVES_FIX))
        fo.write(line.encode('utf8'))

#Parse each individual file
def parseData(fi, fo, voc):
    for line in fi:
        g = vocab.Generator('x', 'x')
        if voc == 0:
            line = ' '.join(g.get_vis_from_sentence_with_method(line, g.Method.SPACE_SPLIT))
        if voc == 1:
            line = ' '.join(g.get_vis_from_sentence_with_method(line, g.Method.SPACE_SPLIT_NO_PUNCT))
        if voc == 2:
            line = ' '.join(g.get_vis_from_sentence_with_method(line, g.Method.SPACE_SPLIT_NO_PUNCT_POSSESSIVES))
        if voc == 3:
            line = ' '.join(g.get_vis_from_sentence_with_method(line, g.Method.SPACE_SPLIT_NO_PUNCT_FIX))
        if voc == 4:
            line = ' '.join(g.get_vis_from_sentence_with_method(line, g.Method.SPACE_SPLIT_NO_PUNCT_POSSESSIVES_FIX))
        fo.write(line.encode('utf8'))

#Build sources from sub files in a directory
def buildSrcDir(loc):
    tgt = os.listdir(loc)
    output = []
    for d in tgt:
        d = os.path.join(loc, d)
        output.append(d)
    return output

# Output folders
VL = []
VL.append("P1V0/")
VL.append("P1V1/")
VL.append("P1V2/")
VL.append("P1V3/")
VL.append("P1V4/")

# Parsing steps
for i in range(len(VL)):
    parseAll(VL[i], i)

