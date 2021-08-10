#! usr/bin/env python3
#This program prints a tab-delimited file with group numbers and the reads in the group based on the the reads in the group fasta files produced by crass
#Example:
#    103     NB501138:168:H2TWVAFXY:1:11101:9054:2555
#    103     NB501138:168:H2TWVAFXY:1:11101:2885:3396

import os, re, csv
#sets location of fasta files
location="/gpfs/home/vmkhot/Crassout/Sample"
fasta=[] #creates empty list

#creates list of all the fasta file paths to open
for file in os.listdir(location):
    if file.startswith("Group"):
        fpath=f"/gpfs/home/vmkhot/Crassout/Sample/{file}"
        fasta.append(fpath)
print(fasta)

#outfile is file with all the crispr groups and their reads printed
outfile="/gpfs/home/vmkhot/Crassout/Sample/group_reads.csv"

#this opens outfile to write just the header and closes it again
with open(outfile,'w',newline='') as out:
    header=csv.writer(out,delimiter='\t')
    header.writerow(["CRISPR Group","Reads"])

#Each file in the fasta-file list is opened and outfile is opened to append to
for eachfile in fasta:
    with open(eachfile, 'r') as fh, open(outfile, 'a',newline='') as out:
        writer=csv.writer(out, delimiter='\t') #sets the writer from csv.writer and delimiter to tabs
        g_num=int(''.join(filter(str.isdigit,eachfile))) #gets the group number from each file name
        for line in fh: #each line in the file is read, and read ids are identified and stored in a list called "line"
               if line.startswith('>'):
                   line=line.strip('\n')
                   line=line[1:-13] #only takes first part of the sequence ID
                   writer.writerow([g_num, line]) #csvwriter writes a new row to the outfile



