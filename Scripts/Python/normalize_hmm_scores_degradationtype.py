#! usr/pyenv/python3
#script normalizes the domain score by its max possible hit score and appends the normalized score (between 0-1) and also the oxygen use and HC_type (aerobic aromatic etc)

import sys, csv, argparse                  
#cutoff_file=sys.argv[1] #comma seperated file of HMM name and max possible scores and degradation types
#hmm_file=sys.argv[2] #HMM search table output
#out_file=sys.argv[3] #output file


parser=argparse.ArgumentParser(description='This script normalizes domain scores for hmmsearch results to the HC_degradation hmm database')


parser.add_argument('-c','--csv',help='csv file of max possible scores and degradation types')
parser.add_argument('-t','--tbl',help='tblout file from hmmsearch')
parser.add_argument('-o','--output',help='output file for normalized results') 

args=parser.parse_args()
cutoff_file=args.csv
hmm_file=args.tbl
out_file=args.output

max_score={}

with open(cutoff_file, 'r') as score:
    for line in score:
        col=line.strip().split(',')
        max_score[col[0]]=[col[1],col[2],col[3]] #adds hmm name as key and list of max score and degradation type as values (Group10_con1_VK_TmoB: [200.7,aerobic,aromatic])
print(max_score)

with open (hmm_file, 'r') as hmm, open (out_file, 'a') as out:
    for line in hmm:
        if not line.startswith('#'):
            cols = line.strip('\n').split() #splits on whitespace
            if cols[2] in max_score.keys():
                nor_score=float(cols[8])/float(max_score[cols[2]][0]) #normalize the domain score by the max possible domain score for that HMM
                metabol=max_score[cols[2]][1]
                HC_type=max_score[cols[2]][2]
                out.write(line.strip('\n') + '\t'+ str(round(nor_score,3)) +'\t'+metabol +'\t'+HC_type+ '\n') #writes line and normalized score and degradation type at the end
                continue




