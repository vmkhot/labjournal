#! usr/pyenv/python3

import csv, os, re, operator, sys
from pathlib import Path
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##this section will create newlines for multiple taxids for a single entry
#diamond_old=sys.argv[1]
#diamond_new='./contigs_v_refseqdmnd_new.txt'
#
#with open (diamond_old, 'r') as dmnd, open(diamond_new,'a',newline='') as out:
#    writer=csv.writer(out,delimiter='\t')
#    for line in dmnd:
#        line=line.strip('\n')
#        cols=line.split('\t')
#        if ";" in cols[12]:
#            taxids=cols[12].split(';')
#            for each_taxid in taxids:
#                print(cols[0],cols[1],cols[2],cols[3],cols[4],cols[5],cols[6],cols[7],cols[8],cols[9],cols[10],cols[11],each_taxid,cols[13],sep='\t')
#                writer.writerow([cols[0],cols[1],cols[2],cols[3],cols[4],cols[5],cols[6],cols[7],cols[8],cols[9],cols[10],cols[11],each_taxid,cols[13]])
#        else:
#            writer.writerow([cols[0],cols[1],cols[2],cols[3],cols[4],cols[5],cols[6],cols[7],cols[8],cols[9],cols[10],cols[11],cols[12],cols[13]])
#
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##This section will create a smaller diamond output file with just 7 columns and taxids
#diamond_small='./contigs_v_refseqdmnd_small.txt'
#with open(diamond_new,'r') as read_in, open (diamond_small,'a',newline='') as small:
#    writer2=csv.writer(small,delimiter='\t')
#    writer2.writerow(["qseqid","sseqid","pident","length","evalue","bitscore","staxids"])
#    for line in read_in:
#        cols=line.split('\t')
#        writer2.writerow([cols[0],cols[1], cols[2],cols[3],cols[10],cols[11],cols[12]])
#
##Run up to here to get all taxids to run on batch entrez. get taxids from the 'small' file and process through batch entrez. download the records retrieved as an xml file.
##awk '{print $7}' contigs_v_refseqdmnd_small.txt > taxids_for_batch.txt
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#This section will parse the xml file downloaded from Batch Entrez for TaxId, Scientific Name and Lineage. Output is a table
import xml.etree.ElementTree as ET

xml_parsed="./parsed_taxon_result.csv" #outfile
tree=ET.parse('./taxonomy_result.xml') #downloaded from batch entrez result

root=tree.getroot()
print(root)
with open(xml_parsed,'a',newline='') as out:
    writer=csv.writer(out,delimiter='\t')
    writer.writerow(['TaxId','ScientificName','Lineage'])
    for Taxon in root.findall('Taxon'):
        taxid=Taxon.find('TaxId').text
        name=Taxon.find('ScientificName').text
        lineage=Taxon.find('Lineage').text
        print(taxid, name, lineage)
        writer.writerow([taxid,name,lineage])

#stop here for a mapping file between taxids and the scientific names
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##This section merges the parsed xml table and the smaller output file
#import pandas as pd
#import numpy as np
#
#taxon_info='./parsed_taxon_result.csv'
#output='diamondout2_added_taxon.csv'
#
#df_dmnd=pd.read_csv(diamond_small,delimiter='\t')
#df_info=pd.read_csv(taxon_info,delimiter='\t')
#print(df_dmnd.columns)
#print(df_info.columns)
#
#df_dmnd.rename(columns={'staxids':'TaxId'},inplace=True)
#print(df_dmnd.columns)
#
##print(df_info['TaxId'])
##print(df_dmnd['TaxId'])
#
#df_3=pd.merge(df_dmnd,df_info,on='TaxId')
#print(df_3)
#df_3.to_csv(output,sep='\t',index=False)




