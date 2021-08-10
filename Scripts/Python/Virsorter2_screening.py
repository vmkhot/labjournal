#! usr/bin/python3

#  This script will screen Virsorter2 results into 3 categories - "keep", "discard" and "manual check" based on the following criteria from https://www.protocols.io/view/viral-sequence-identification-sop-with-virsorter2-btv8nn9w?version_warning=no&step=4
#   Keep: viral_gene>0, OR max_score>0.95, OR hallmark>2, OR (viral_gene=0 AND host_gene=0)
#   Discard: viral_gene =0 AND host_gene >1 OR (viral_gene =0 AND host_gene =1 AND length <10kb)
#   Manual check: viral_gene =0 AND host_gene =1 AND length >=10kb

import pandas as pd
from pandas import DataFrame
import numpy as np
import csv, sys, re

contamination="~/data/bioreactor/Virsorter2/checkv/contamination.tsv"
pass1_scores="~/data/bioreactor/Virsorter2/pass1/final-viral-score.tsv"
keep="~/data/bioreactor/Virsorter2/filtering/keep.tsv"
discard="~/data/bioreactor/Virsorter2/filtering/discard.tsv"
manual="~/data/bioreactor/Virsorter2/filtering/manual_check.tsv"

df_cont=pd.read_csv(contamination,sep="\t",usecols=[0,1,3,4])
df_score=pd.read_csv(pass1_scores,sep="\t",usecols=[0,3,4,5,6])

df_merged=pd.merge(df_cont,df_score,left_on='contig_id',right_on='seqname')

#print(df_merged)

df_keep=df_merged.loc[(df_merged.viral_genes>0) | (df_merged.max_score > 0.95) | (df_merged.hallmark > 2) | ((df_merged.viral_genes==0) & (df_merged.host_genes==0))]

#print(df_keep)

df_discard=df_merged.loc[((df_merged.viral_genes==0) & (df_merged.host_genes>1) & (df_merged.hallmark < 2) & (df_merged.max_score < 0.95)) | ((df_merged.viral_genes==0) & (df_merged.host_genes==1)& (df_merged.length< 10000) & (df_merged.hallmark < 2) & (df_merged.max_score < 0.95) )]

#print(df_discard)

df_manual=df_merged.loc[((df_merged.viral_genes==0) & (df_merged.host_genes==1) & (df_merged.length >= 10000))]
print(df_manual)

df_keep.to_csv(keep,sep='\t',header=True,index=False)
df_discard.to_csv(discard,sep='\t',header=True,index=False)
df_manual.to_csv(manual,sep='\t',header=True,index=False)
