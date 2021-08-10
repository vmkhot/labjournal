#! usr/pyenv/python3

import sys,csv

tsv_file = sys.argv[1]
outfile = sys.argv[2]

with open(tsv_file, 'r') as annot, open(outfile, 'a', newline='') as out:
    writer=csv.writer(out, delimiter='\t')
    writer.writerow(['contigid','gene name','type','start','end','length','strand','annotation','taxonomy'])
    for row in annot:
        row=row.strip('\n')
        col=row.split('\t')
        #`print(col[1])
        if not (col[12] and col [13]):
        #    print(col[0],col[1],col[3],col[4],col[5],col[6],col[14],col[15],sep='\t')
            writer.writerow([col[0],col[1],col[2],col[3],col[4],col[5],col[6],col[14],col[15]])
        elif col[12]:
            writer.writerow([col[0],col[1],col[2],col[3],col[4],col[5],col[6],col[12],col[15]]) 
        #    print(col[0],col[1],col[3],col[4],col[5],col[6],col[12],col[15],sep='\t')
        elif col[13]:
            writer.writerow([col[0],col[1],col[2],col[3],col[4],col[5],col[6],col[13],col[15]]) 
        #    print(col[0],col[1],col[3],col[4],col[5],col[6],col[13],col[15],sep='\t')
         
