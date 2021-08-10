#! usr/pyenv/python3

import sys

#change this to "argparse" later
cutoff_file="./cutoff_score.csv"
hmm_output="./hmmsearch_result_SRR10302631_subset.tblout"
parsed_table="./parsed_hmm_output.tbl"


with open (cutoff_file, 'r') as cutoff:
    genes={}
    for line in cutoff:
        line=line.strip('\n')
        cols=line.split(',')
        genes[cols[0]]=float(cols[1])

#print(genes,type(genes['AlkB_HMM']))

with open(hmm_output, 'r') as hmm, open(parsed_table, 'a') as output:
   for line in hmm:
       line=line.strip('\n')
       cols=line.split()
#       print(cols[8],type(cols[8]))
       if cols[2] in genes.keys():
           if float(cols[8]) > genes[cols[2]]:
               output.write(line+'\n')
               print(line)



