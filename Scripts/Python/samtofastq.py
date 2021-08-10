#! bin/python

#This program takes a list of contigs and filters a sam file to get reads of just the filtered contigs and creates paired-end fastq files of them.
#could be used to only get reads belonging to specific set of contigs for reassembly/rebinned etc


import glob,re,csv,os
from pathlib import Path
from itertools import islice

#input files to change
#contig_file="Virus/VirSorter2/Results_refseq_custom/Analysis/contigs_unfiltered.txt"
#samfile="bioreactor/Mapping/samples_in_assembly/assembly_sam/C_8_6_Ammonium_reformat.sam"
#fastq1="bioreactor/Fastq_files/C_8_6_Ammonium.qc.1.fastq"
#fastq2="bioreactor/Fastq_files/C_8_6_Ammonium.qc.2.fastq"
#outfile1="Virus/VirSorter2/Results_refseq_custom/Analysis/Fastq/C_8_6_Ammonium.reads1.fq"
#outfile2="Virus/VirSorter2/Results_refseq_custom/Analysis/Fastq/C_8_6_Ammonium.reads2.fq"
import argparse

parser=argparse.ArgumentParser(description='this program outputs paired reads for a list of contigs')

parser.add_argument('-l','--contigs',help='file with list of contigs')
parser.add_argument('-s','--samfile',help='path to sam file')
parser.add_argument('-f1','--fastq1',help='path to forward paired reads')
parser.add_argument('-f2','--fastq2',help='path to reverse paired reads')
parser.add_argument('-o1','--output1',help='path output fastq1 file')
parser.add_argument('-o2','--output2',help='path output fastq2 file')

args=parser.parse_args()

contig_file=args.contigs
samfile=args.samfile
fastq1=args.fastq1
fastq2=args.fastq2
outfile1=args.output1
outfile2=args.output2
#print(contig_file, samfile, fastq1, fastq2, outfile1, outfile2)

contigs=[]
reads={}


with open(contig_file, 'r') as contig_list:
    for line in contig_list:
        line=line.strip('\n')
        contigs.append(line)

print(contigs)

with open(samfile, 'r') as sam:
    print(samfile)
    for line in sam:
        if line.startswith('NB'):
            cols=line.split('\t')
            if cols[2] in contigs:
                #print(cols[2],cols[0][0:-13])
                reads[cols[0][0:-13]]=1
                #print(reads)

#print(reads.keys(),len(reads))

with open(fastq1, 'r') as reads1, open(outfile1, 'a') as out1:
    for line in reads1:
        if line.startswith('@'):
            line=line.strip('\n')
            if line[1:-13] in reads:
#                print(line +'\r'+''.join(islice(reads1,4)))
                out1.write(line +'\n'+''.join(islice(reads1,3)))

with open(fastq2, 'r') as reads2, open(outfile2, 'a') as out2:
    for line in reads2:
        if line.startswith('@'):
            line=line.strip('\n')
            if line[1:-13] in reads:
                out2.write(line +'\n'+''.join(islice(reads2,3)))
