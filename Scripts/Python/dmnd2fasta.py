#! usr/pyenv/python3

import sys

blast_file=sys.argv[1]
out=sys.argv[2]

with open(blast_file,'r') as blast, open(out, 'a') as fasta:
    for line in blast:
        cols=line.split('\t')
        fasta.write('>' + cols[1]+'_'+cols[12] +'_REF'+ '\n' + cols[13] + '\n') #for refseq
#        fasta.write('>' + cols[1] +'_IMG'+ '\n' + cols[12] + '\n') #for imgvr

