#! usr/pyenv/python3

import sys 

homolog_file=sys.argv[1]
blast_file=sys.argv[2]
out=sys.argv[3]

with open (homolog_file,'r') as homolog:
    sequences={}
    for line in homolog:
        sequences[line]=1

print(sequences.keys())        


with open(blast_file,'r') as blast, open(out, 'a') as fasta:
    for line in blast:
        cols=line.split('\t')
        if cols[0] in sequences.keys():
            fasta.write(cols[1] + '\n' + cols[12] + '\n')

