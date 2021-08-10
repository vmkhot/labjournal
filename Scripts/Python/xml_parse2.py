# bin/python
#This script prints a tab-delimited file with (CRISPR group numbers, reads, mapped contigs, and the mapping positions) based on the the information in the xml-tree file (crass.crispr) produced by crass and the sam files produced for each group. It then deduplicates the reads and sorts by contig+position. so that the reads are ranked by position for each contig.
#Example:
#CRISPR Group    Reads   Contig  Start   End
#9       NB501138:168:H2TWVAFXY:1:11101:6142:3568        bin00.contig0012 length=83555   8988    8867
#9       NB501138:168:H2TWVAFXY:1:11101:8849:2821        bin00.contig0012 length=83555   9056    8887
#9       NB501138:168:H2TWVAFXY:1:11101:4477:3817        bin00.contig0012 length=83555   9149    9007
#9       NB501138:168:H2TWVAFXY:1:11101:22230:2852       bin00.contig0012 length=83555   9710    9740


import xml.etree.ElementTree as ET
import csv, os, re, operator

#setting writing out file
outfile="Crassout/Sample/xml_reads.csv"
tree = ET.parse('Crassout/Sample/crass.crispr') #element-tree parses crass.crispr files
root=tree.getroot() #setting the root of the tree

#this loop iterates through the children in xml-tree and writes to a csv file

with open(outfile,'a',newline='') as out: #with loops close file at the end automatically
    writer=csv.writer(out, delimiter='\t')
    for child in root.iterfind('group'): #finds the child branch called "group"
 #       print(child.attrib)
        for step_child in child.iterfind('./data/sources/source'): #iterates thrugh particular group in the "sources" branch
#            print(step_child.get('accession'))
            g_num=child.get('gid') #gets group id from the attributes
            number=int(''.join(filter(str.isdigit,g_num)))
            read_id=step_child.get('accession') #gets read_ids from the sources
            sam_path=f"Crassout/Sample/MappedReads/Mapped{number}/Group{number}.sam"
            for line in open(sam_path,'r'):
                if read_id in line:
                    contig=str.split(line,sep='\t')[2]
                    start=str.split(line,sep='\t')[3]
                    end=str.split(line,sep='\t')[7]
 #                   print(g_num,'\t',read_id,'\t',contig,'\t',start,'\t',end)
                    writer.writerow([number,read_id,contig,start,end]) #writes a row to outfile

#the next function removes duplicates according to the read ID
with open('Crassout/Sample/xml_reads.csv','r') as infile, open('Crassout/Sample/xml_deduped.csv','a+',newline='') as deduped:
    reader=csv.reader(infile, delimiter='\t')
    writer=csv.writer(deduped,delimiter='\t')
    seen=set()
    for row in reader:
        if row[1] in seen: continue
        seen.add(row[1])
        writer.writerow(row)

#this function sorts the deduplicated file by contig and then by start position of the mapping and writes it to final file
with open('Crassout/Sample/xml_deduped.csv','r',newline='') as deduped, open('Crassout/Sample/xml_sorted.csv','a') as sort_file:
    reader2=csv.reader(deduped,delimiter='\t')
    writer2=csv.writer(sort_file,delimiter='\t')
    writer2.writerow(['CRISPR Group','Reads','Contig','Start','End'])  #writes header to the final file
    sort=sorted(reader2,key=lambda x: (float(x[0]),x[2],float(x[3]))) #sorts by column 2 (contig) and 3 (position)
    for line in sort:
#        print(line)
        writer2.writerow(line)

with open('Crassout/Sample/xml_sorted.csv','r',newline='') as sort, open('Crassout/Sample/xml_short.csv','a') as short:
    reader=csv.reader(sort,delimiter='\t')
    writer=csv.writer(short,delimiter='\t')
    positions=[]
    for row[0] in reader:
        for row[2] in reader:
            positions.append(row[3])
            positions.append(row[4])
            mini=min(positions)
            maxi=max(positions)
            print(row[2],mini,maxi)

