#! usr/bin/python3

#this program will take input from blast input with the following columns:"qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qcovs" and hopefully produce a pairwise alignment based on bitscore ratio
#results:
#contig0001 contig0002  0.33
#contig0001 contig0060  0.80

import pandas as pd
from pandas import DataFrame 
import numpy as np
import csv, sys, re

#read the blast file (all_prot_selfdmnd.out). this file is the self blast of all the protein sequences incl. reference seq
blastp=sys.argv[1]
#outfile is pairwise alignment file
outfile=sys.argv[2]

#read blast file into a dataframe 'df' and rename columns
df=pd.read_csv(blastp,sep='\t',usecols=[0,1,11],names=['query','subject','bitscore'],header=None)
#print(df.loc[[21601]])
#create columns for contigs
df.insert(0,"qcontig",df['query'].str.extract(r'(^\w+.contig\d+|^IMG_\d+_____[a-zA-Z0-9]+_\d+|^IMG_\d+_____[a-zA-Z0-9]+|^IMG_[A-Za-z]+_gi_\d+|\d+_REF)'))
df.insert(2,"scontig",df['subject'].str.extract(r'(^\w+.contig\d+|^IMG_\d+_____[a-zA-Z0-9]+_\d+|^IMG_\d+_____[a-zA-Z0-9]+|^IMG_[A-Za-z]+_gi_\d+|\d+_REF)'))
#print(df['scontig'])

df1=df[df.isna().any(axis=1)]
print(df1)

#sum bitscores by query and subject contigs and put into condensed datafram 'df_cond'
df_cond=df.groupby(['qcontig','scontig']).sum().reset_index()
df_cond.rename(columns={'bitscore':'BSsum'},inplace=True)
print(df_cond)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#mapping contigs to dictionary
contigs=[]
for line in df_cond['qcontig']:
    if line in contigs:
        next
    else:
        contigs.append(line)
        
#print(contigs)
dictionary={}
i=0
for j in contigs:
    dictionary[j]=i
    i=i+1
#print(dictionary)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#convert datafram from long to wide format and then into a 2d array
df_cond.dropna(inplace=True)
df_cond=df_cond.set_index(['qcontig','scontig']).unstack()
arr=df_cond.values
#print(arr)

#calculate dice distance and assign to new dictionary 'new_dict'
new_dict={}
for i in range(0,len(arr)):
    for j in range(0,len(arr[0])):
        dice=1-((2*max(arr[i][j],arr[j][i]))/(arr[i][i]+arr[j][j]))
        new_dict[i,j]=dice

#inverse dictionary of contigs
inv_map={v:k for k,v in dictionary.items()}

#create a new final dataframe for printing using list comprehension and using values from inv_map (inversed contig mapping) and dice from 'new_dict'
d=[]
for k1,k2 in new_dict.keys():
    d.append({'contig1':inv_map[k1],'contig2':inv_map[k2],'dice':new_dict[k1,k2]})
#    print(inv_map[k1]+'\t'+inv_map[k2]+'\t'+str(new_dict[k1,k2]))
#print(d)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#create final dataframe for printing out and clean up
df_final=pd.DataFrame(d)
df_final=df_final[['contig1','contig2','dice']]
df_final.replace([np.inf,-np.inf],np.nan,inplace=True)
df_final.dropna(inplace=True)
#df_final.insert(3,'1-dice',1-df_final['dice'])
#df_final.drop(columns='dice',inplace=True)

df_final.to_csv(outfile,sep='\t',header=True,index=False)
print(df_final)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#this section changes the ids of all the reference genomes to virus names

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#This section will construct a a distance matrix using the final dataframe and then phylogenetic tree using biopython's phylo module
#from Bio import Phylo
#from Bio.Phylo.TreeConstruction import DistanceTreeConstructor
#from scipy import skbio
#from skbio.core.distance import DistanceMatrix
#
#dm=DistanceMatrix(df_final['contig1'],df_final['contig2'])
##distmat=df_final.set_index(['contig1','contig2']).unstack().fillna(0)
#print(dm)
#constructor=DistanceTreeConstructor()
#tree=constructor.upgma(dm)
#print(tree)




