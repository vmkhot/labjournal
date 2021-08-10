#! usr/pyenv/python3

import csv, os, re, operator, sys
import pandas as pd
from pathlib import Path

diamond_file=sys.argv[1]
tax_info=sys.argv[2]
output='./diamondout2_add_taxon.tsv'


df_dmnd=pd.read_csv(diamond_file,sep='\t',names=["qseqid","sseqid","pident","length","mismatch","gapopen","qstart","qend","sstart","send","evalue","bitscore","taxid","sequence"])
df_info=pd.read_table(tax_info,sep=',',engine='python',names=["taxid","sci_name","lineage"])
#print(df_dmnd['taxid'])
#print(df_info['taxid'])


df_dmnd[['contig','orf']] = df_dmnd.qseqid.str.split(pat='_',expand=True)
df_out=pd.merge(df_dmnd,df_info,on='taxid')
cols=["qseqid","contig","orf","sseqid","pident","length","mismatch","gapopen","qstart","qend","sstart","send","evalue","bitscore","taxid","sci_name","lineage"]
df_out=df_out[cols]
df_out.to_csv(output,sep='\t',index=False)
print(df_out.columns)

