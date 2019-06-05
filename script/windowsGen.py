# py to generate commands to run all models

import os

################################## Change these variables on per user basis

Letter_ID = "a/acm503"
email = "acmalis@hotmail.com"

################################## User Guide
# 
# Change letter id and email for user

# 
# Check cd /storage/ command for destination, currently ~/work/nmt
#   - This folder needs to have a correct path for data in VL and PL
#   - For testing, this was done by having WebNLG folder inside nmt folder
#
# To run, qsub <Correct pbs file>, if having trouble, pathing is likely cause
# 
################################## Disclaimer
#
# I can not get on ICS-ACI to test, testing was done on local computer
# may have issues with submission script, need help fixing this by someone
# who can test. My worry is it will not run in parralell.
# 
##################################

VL = []
VL.append("WebNLG-G4-P2/vocab/SPACE_SPLIT/")
VL.append("WebNLG-G4-P2/vocab/SPACE_SPLIT/")
VL.append("WebNLG-G4-P2/vocab/SPACE_SPLIT_NO_PUNCT/")
VL.append("WebNLG-G4-P2/vocab/SPACE_SPLIT_NO_PUNCT/")
VL.append("WebNLG-G4-P2/vocab/SPACE_SPLIT_NO_PUNCT_POSSESSIVES/")
VL.append("WebNLG-G4-P2/vocab/SPACE_SPLIT_NO_PUNCT_POSSESSIVES/")
VL.append("WebNLG-G4-P2/vocab/SPACE_SPLIT_NO_PUNCT_FIX/")
VL.append("WebNLG-G4-P2/vocab/SPACE_SPLIT_NO_PUNCT_FIX/")
VL.append("WebNLG-G4-P2/vocab/SPACE_SPLIT_NO_PUNCT_POSSESSIVES_FIX/")
VL.append("WebNLG-G4-P2/vocab/SPACE_SPLIT_NO_PUNCT_POSSESSIVES_FIX/")

PL = []
PL.append("WebNLG-G4-P2/parsing/P1V0/A/")
PL.append("WebNLG-G4-P2/parsing/P1V0/B/")
PL.append("WebNLG-G4-P2/parsing/P1V1/A/")
PL.append("WebNLG-G4-P2/parsing/P1V1/B/")
PL.append("WebNLG-G4-P2/parsing/P1V2/A/")
PL.append("WebNLG-G4-P2/parsing/P1V2/B/")
PL.append("WebNLG-G4-P2/parsing/P1V3/A/")
PL.append("WebNLG-G4-P2/parsing/P1V3/B/")
PL.append("WebNLG-G4-P2/parsing/P1V4/A/")
PL.append("WebNLG-G4-P2/parsing/P1V4/B/")
# Discontinued parsing
#PL.append("WebNLG-G4-P2/parsing/P02/A/")
#PL.append("WebNLG-G4-P2/parsing/P02/B/")
#PL.append("WebNLG-G4-P2/parsing/P03/A/")
#PL.append("WebNLG-G4-P2/parsing/P03/B/")
#PL.append("WebNLG-G4-P2/parsing/P04/A/")
#PL.append("WebNLG-G4-P2/parsing/P04/B/")

NL = []
NL.append("STD")
NL.append("BEAM")
NL.append("ATT")
NL.append("BEAT")

SL = []
SL.append("12000")
SL.append("24000")

UL = []
UL.append("256")
UL.append("512")

LL = []
LL.append("2")
LL.append("4")

# list of completed blocks
doneList = [0, 4, 10, 24]

def genOutput(v, p, o, m, step, unit, layer):
    if m == "STD": 
        output = []
        output.append("% python -m nmt.nmt")
        output.append("--src=vi --tgt=en")
        output.append("--vocab_prefix="+v+"vocab")
        output.append("--train_prefix="+p+"train")
        output.append("--dev_prefix="+p+"dev")
        output.append("--test_prefix="+p+"test")
        output.append("--out_dir=tmp/"+o+"/")
        output.append("--num_train_steps="+step)
        output.append("--steps_per_stats=100")
        output.append("--num_layers="+layer)
        output.append("--num_units="+unit)
        output.append("--dropout=0.2")
        output.append("--metrics=bleu")
        #ot = os.path.join(p, "../UWL/")
        #output.append("--inference_input_file="+ot+"test.vi")
        #output.append("--inference_ref_file="+ot+"test.en")
        #output.append("--inference_output_file==tmp/"+o+"/inf.output.txt")
        return " ".join(output)
    if m == "BEAM":
        output = []
        output.append("% python -m nmt.nmt")
        output.append("--src=vi --tgt=en")
        output.append("--vocab_prefix="+v+"vocab")
        output.append("--train_prefix="+p+"train")
        output.append("--dev_prefix="+p+"dev")
        output.append("--test_prefix="+p+"test")
        output.append("--out_dir=tmp/"+o+"/")
        output.append("--num_train_steps="+step)
        output.append("--steps_per_stats=100")
        output.append("--num_layers="+layer)
        output.append("--num_units="+unit)
        output.append("--dropout=0.2")
        output.append("--metrics=bleu")
        output.append('--infer_mode="beam_search"')
        output.append("--beam_width=12")
        #ot = os.path.join(p, "../UWL/")
        #output.append("--inference_input_file="+ot+"test.vi")
        #output.append("--inference_ref_file="+ot+"test.en")
        #output.append("--inference_output_file==tmp/"+o+"/inf.output.txt")
        return " ".join(output)
    if m == "ATT":
        output = []
        output.append("% python -m nmt.nmt")
        output.append("--attention=scaled_luong")
        output.append("--src=vi --tgt=en")
        output.append("--vocab_prefix="+v+"vocab")
        output.append("--train_prefix="+p+"train")
        output.append("--dev_prefix="+p+"dev")
        output.append("--test_prefix="+p+"test")
        output.append("--out_dir=tmp/"+o+"/")
        output.append("--num_train_steps="+step)
        output.append("--steps_per_stats=100")
        output.append("--num_layers="+layer)
        output.append("--num_units="+unit)
        output.append("--dropout=0.2")
        output.append("--metrics=bleu")
        #ot = os.path.join(p, "../UWL/")
        #output.append("--inference_input_file="+ot+"test.vi")
        #output.append("--inference_ref_file="+ot+"test.en")
        #output.append("--inference_output_file==tmp/"+o+"/inf.output.txt")
        return " ".join(output)

    if m == "BEAT":

        output = []
        output.append("% python -m nmt.nmt")
        output.append("--attention=scaled_luong")
        output.append("--src=vi --tgt=en")
        output.append("--vocab_prefix="+v+"vocab")
        output.append("--train_prefix="+p+"train")
        output.append("--dev_prefix="+p+"dev")
        output.append("--test_prefix="+p+"test")
        output.append("--out_dir=tmp/"+o+"/")
        output.append("--num_train_steps="+step)
        output.append("--steps_per_stats=100")
        output.append("--num_layers="+layer)
        output.append("--num_units="+unit)
        output.append("--dropout=0.2")
        output.append("--metrics=bleu")
        output.append('--infer_mode="beam_search"')
        output.append("--beam_width=12")
        #ot = os.path.join(p, "../UWL/")
        #output.append("--inference_input_file="+ot+"test.vi")
        #output.append("--inference_ref_file="+ot+"test.en")
        #output.append("--inference_output_file==tmp/"+o+"/inf.output.txt")
        return " ".join(output)

def scriptStart():
    output = []
    output.append("#!/bin/bash -login\n")
    output.append("#PBS -A cyberlamp_class -l qos=cl_class\n")
    output.append("##PBS -l qos=cl_gpu\n")
    output.append("#PBS -j oe\n")
    output.append("#PBS -l walltime=08:00:00\n")
    output.append("#PBS -l nodes=4:ppn=1:gpus=1:shared\n")
    
    output.append("#PBS -l pmem=5gb\n")
    output.append("#PBS -m abe\n")
    output.append("#PBS -M "+email+"\n")
    output.append("cd /storage/home/"+Letter_ID+"/work/nmt\n")
    return "".join(output)+"\n"

def genScript(name, step, unit, layer):
    idname = "_S"+step+"_U"+unit+"_L"+layer
    fn = name+idname+".bat"
    f = open(fn, "wb+")
    #f.write(scriptStart().encode('utf8'))
    for j in range(len(PL)):
        if (j % 2) == 0:
            tag = "A"
        else:
            tag = "B"
        tag = tag+str(j//2)
        
        f.write((genOutput(VL[j], PL[j], name+idname+"-"+tag, name, step, unit, layer)+"\n").encode('utf8'))
    f.close()

count = 0
for p in range(len(NL)):
    for q in range(len(SL)):
        for r in range(len(UL)):
            for s in range(len(LL)):
                if count not in doneList:
                    print("Generating #"+str(count)+": "+NL[p]+", "+SL[q]+", "+UL[r]+", "+LL[s])
                    genScript(NL[p], SL[q], UL[r], LL[s])
                count = count + 1

