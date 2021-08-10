#! usr/pyenv/python3

#this script will compare columns 0 and 1 of a self-blastn output (fmt 6) and remove hits of sequence to itself.

import glob,re,os,sys
from pathlib import Path

#headers=sys.argv[1] #file of contig_ids list (input from user)
blastn_in=sys.argv[1]
output="./blastn_unique.out"

with open(blastn_in,"r") as blastn, open(output, "a") as out:
    for line in blastn:
        cols=line.split('\t')
        if cols[0] != cols[1]:
            out.write(cols[0] + '\t' + cols[1] + '\t' + cols[2] + '\t' +cols[3]+ '\t' + cols[4]+ '\t'+ cols[5]+ '\t'+ cols[6]+ '\t'+ cols[7]+ '\t'+ cols[8]+ '\t'+ cols[9]+ '\t' +cols[10]+ '\t' +cols[11])
            #print(cols[0],cols[1])

print("parsing finished")

