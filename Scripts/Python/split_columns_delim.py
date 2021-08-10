#! bin/python
#to split one column by delimiter and add multiple entries of the same column

import csv, os, re, operator

infile='./diamondout2_100.txt'
outfile='./diamond2_100_splitstaxids.txt'

with open (infile, 'r') as dmnd, open(outfile,'a',newline='') as out:
    writer=csv.writer(out,delimiter='\t')
    for line in dmnd:
        cols=line.split('\t')
        if ";" in cols[12]:
            taxids=cols[12].split(';')
            for each_taxid in taxids:
                print(cols[1],cols[2],cols[3],cols[4],cols[5],cols[6],cols[7],cols[8],cols[9],cols[10],cols[11],each_taxid,sep='\t')
                writer.writerow([cols[1],cols[2],cols[3],cols[4],cols[5],cols[6],cols[7],cols[8],cols[9],cols[10],cols[11],each_taxid])

































