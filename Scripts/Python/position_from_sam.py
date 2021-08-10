#! bin/python

#INCOMPLETE PROGRAM
#this program attempts to do the same thing as position_from_sam2.py but only prints 1 array per contig. some contigs might have more than 1 crispr group associated with them.
#does not print to file, only to STDOUT

import glob,re
from pathlib import Path
from collections import defaultdict
#location=glob.glob("/gpfs/home/vmkhot/Crassout/Sample/",recursive=True)
outfile="/gpfs/home/vmkhot/Crassout/Sample/group_reads_2.csv"
d={}
aligns=[]
for eachfile in Path('Crassout/Sample').glob('**/*.sam'):
    with open(eachfile, 'r') as sam, open(outfile, 'a') as out:
        g_num=re.findall(r'\d+',str(eachfile))[1]
#        print(g_num)
        for line in sam:
            if line.startswith('NB'):
                cols=line.split('\t')
                contigs=cols[2]
                start=float(cols[3])
                end=float(cols[7])
                aligns.append([g_num,contigs,start,end])
values=[]    
final={}

for g,c,s,e in aligns:
    values.append([c,s,e])
    d.setdefault(g,[]).append(values)
#    print(d.items())

for x,y,z in values:
    final.setdefault(x,[]).append([y,z])
    
#print(final.keys())
#    
#
#for gid,value in d.items():
#    for k,s,e in value:
#        d.setdefault(k,[]).append(s)
#        d.setdefault(k,[]).append(e)
        #print(d.items())
#
for item in final.keys():
    mini=min(final[item])
    maxi=max(final[item])
    print(item,'\t',mini[0],'\t',maxi[0])
