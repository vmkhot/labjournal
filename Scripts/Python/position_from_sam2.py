#! bin/python
#This program takes all sam files of all mapped crass groups and for each contig figures out the min and max positions of each of the crispr arrays. Produces a long format, where all the mapped reads are given and short format (1 crispr array per contig)
#short format result below:
#CRISPR Group    Contig  Start   End
#1   bin00.contig0038 length=40216   20663.0 22061.0
#1   unbinned.contig18836 length=1467    677.0   678.0
#1   unbinned.contig21640 length=1099    200.0   305.0
#6   bin00.contig0046 length=37465   596.0   19424.0
#6   unbinned.contig24225 length=3538    808.0   2998.0
#6   unbinned.contig51779 length=1037    596.0   17532.0
#6   unbinned.contig77025 length=1575    202.0   372.0
#7   bin00.contig0020 length=68665   49588.0 53817.0

import glob,re,csv,os
from pathlib import Path
from collections import defaultdict
#location=glob.glob("/gpfs/home/vmkhot/Crassout/Sample/",recursive=True)
out_short="/gpfs/home/vmkhot/Crassout/Sample/short_pos.csv"
out_long="/gpfs/home/vmkhot/Crassout/Sample/long_pos.csv"
nested_dict=defaultdict(lambda: defaultdict(list))
aligns=[]

for eachfile in Path('Crassout/Sample').glob('**/*.sam'):
    with open(eachfile, 'r') as sam, open(out_long, 'a') as out:
        writer=csv.writer(out,delimiter='\t')
        g_num=re.findall(r'\d+',str(eachfile))[1]
        for line in sam:
            if line.startswith('NB'):
                cols=line.split('\t')
                reads=cols[0]
                contigs=cols[2]
                start=float(cols[3])
                end=float(cols[7])
                writer.writerow([g_num,reads,contigs,start,end])
                aligns.append([g_num,contigs,start,end])

#the next function removes duplicates according to the read ID
with open('Crassout/Sample/long_pos.csv','r') as infile, open('Crassout/Sample/long_pos_deduped.csv','a+',newline='') as deduped:
    reader=csv.reader(infile, delimiter='\t')
    writer=csv.writer(deduped,delimiter='\t')
    seen=set()
    for row in reader:
        if row[1] in seen: continue
        seen.add(row[1])
        writer.writerow(row)

#this function sorts the deduplicated file by contig and then by start position of the mapping and writes it to final file
with open('Crassout/Sample/long_pos_deduped.csv','r',newline='') as deduped, open('Crassout/Sample/long_pos_sorted.csv','a') as sort_file:
    reader2=csv.reader(deduped,delimiter='\t')
    writer2=csv.writer(sort_file,delimiter='\t')
    writer2.writerow(['CRISPR Group','Reads','Contig','Start','End'])  #writes header to the final file
    sort=sorted(reader2,key=lambda x: (float(x[0]),x[2],float(x[3]))) #sorts by column 2 (contig) and 3 (position)
    for line in sort:
#        print(line)
        writer2.writerow(line)




for g,c,s,e in aligns:
    nested_dict[g][c].append([s,e])
#print(nested_dict.items())

with open(out_short, 'a') as out:
    writer=csv.writer(out, delimiter='\t')
    for group in nested_dict:
        for c in nested_dict[group]:
            pos=[]
            for coord in nested_dict[group][c]:
                pos.append(coord[0])
                pos.append(coord[1])
                mini=min(pos)
                maxi=max(pos)
            writer.writerow([group,c,mini,maxi])
            print(group,'\t',c,'\t',mini,'\t',maxi)

with open('Crassout/Sample/short_pos.csv','r',newline='') as unsorted, open('Crassout/Sample/short_pos_sorted.csv','a') as sort_file:
    reader2=csv.reader(unsorted,delimiter='\t')
    writer2=csv.writer(sort_file,delimiter='\t')
    writer2.writerow(['CRISPR Group','Contig','Start','End'])  #writes header to the final file
    sort=sorted(reader2,key=lambda x: (float(x[0]),x[1])) #sorts by column 2 (contig) and 3 (position)
    for line in sort:
#        print(line)
        writer2.writerow(line)
            
os.remove('Crassout/Sample/short_pos.csv')
os.remove('Crassout/Sample/long_pos_deduped.csv')
os.remove('Crassout/Sample/long_pos.csv')

