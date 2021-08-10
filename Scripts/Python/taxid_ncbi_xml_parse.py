#bin/python
#This script parses the xml tree downloaded from ncbi's batch entrez results to get taxid, scientific name and lineage

import xml.etree.ElementTree as ET
import csv, os, re, operator

outfile="./parsed_taxon_result.csv"
tree=ET.parse('./taxonomy_result.xml')
root=tree.getroot()
print(root)
with open(outfile,'a',newline='') as out:
    writer=csv.writer(out,delimiter='\t')
    writer.writerow(['TaxId','ScientificName','Lineage'])
    for Taxon in root.findall('Taxon'):
        taxid=Taxon.find('TaxId').text
        name=Taxon.find('ScientificName').text
        lineage=Taxon.find('Lineage').text
        print(taxid, name, lineage)
        writer.writerow([taxid,name,lineage])

#~~~~~~~~~~~~~~~~
import pandas as pd
import numpy as np

diamondout='./diamondout2_split.txt'
ncbi_info='./parsed_taxon_result.csv'
output='diamondout2_split_taxon_added.csv'

df_dmnd=pd.read_csv(diamondout,delimiter='\t')
df_info=pd.read_csv(ncbi_info,delimiter='\t')
print(df_dmnd.columns)
print(df_info.columns)

df_dmnd.rename(columns={'staxids':'TaxId'},inplace=True)

print(df_info.dtypes)
print(df_dmnd.dtypes)
df_info.TaxId.astype('object')
print(df_info['TaxId'])
print(df_dmnd['TaxId'])

df_3=pd.merge(df_dmnd,df_info,on='TaxId')
print(df_3)


