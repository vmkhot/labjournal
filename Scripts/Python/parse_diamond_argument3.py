#! usr/pyenv/python3

#This script takes a diamond result with staxids and splits the columns and only ouputs certain fields - query, subject, length, pident, evalue, bitscore, taxid
#Creates a new file for each contig


import glob,re,os,sys
from pathlib import Path

#headers=sys.argv[1] #file of contig_ids list (input from user)
diamond_file=sys.argv[1]

#commented out section creates different files based onthe contig id
#contigs=[]
#with open(headers,'r') as headers:
#    for line in headers:
#        line=line.strip('\n')
#        contigs.append(line)
#        os.mknod(f"{line}_dmnd_hits.faa")
#        os.mknod(f"{line}_staxids.txt")
#        os.chmod(f"{line}_dmnd_hits.faa",0o770)
#    print(contigs)


with open(diamond_file,"r") as diamond:
    for line in diamond:
        cols=line.split('\t')
        x=re.search("(^[a-z]+[0-9]+|^[a-z]+)\.contig[0-9]+",cols[0])
        contig_id=x.group(0)
#        print(contig_id)
        with open (f"{contig_id}_staxids.txt", 'a')as taxon: #open(f"{contig_id}_dmnd_hits.faa",'a') as fastaout:
            print(cols[0],cols[1], cols[2],cols[3],cols[10],cols[11],cols[12])
            taxon.write(cols[0] + '\t' + cols[1] + '\t' + cols[2] + '\t' +cols[3]+ '\t' + cols[10]+ '\t' +cols[11]+ '\t' +cols[12] + '\n')
#            fastaout.write('>' + cols[0] + "_" +cols[1] + '\n' + cols[13] + '\n')

print("parsing finished")

