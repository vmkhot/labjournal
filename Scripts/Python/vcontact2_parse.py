#! usr/pyenv/python3


#This program takes network file produced by vcontact2, filters for contigs and outputs into a table that reports a table with taxonomic assignment to each contig found in the network file. the output looks like below:
#~~~bin23.contig0003    bin12.contig0010_10.487;unbinned.contig63620_7.63
#~~~bin35.contig0006    Pseudomonas~phage~F10_4.924;Pseudomonas~phage~MD8_4.881

import pandas as pd
import csv, sys

#read the network file
ntw=sys.argv[1]
#read the file into a dataframe and assign headers
df=pd.read_csv(ntw,sep='\s+',usecols=[0,1,2], names=['query','match','weight'], header=None)
#print(df['query'])
#sort for contigs,weights>3.0 (which translates to 3value<=0.001, and rounds the weights to 3 decimal places
df_contigs=df[df['query'].str.contains("contig",na=False) & (df['weight'] >= 3)].round({'weight':3})
df_contigs.sort_values(by=['query','weight'],ascending=[True,False],inplace=True)

#reset index
df_contigs.reset_index(drop=True,inplace=True)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#creates a nested dictionary-list-dict to store all the values of contigs
d={}

for i in df_contigs['query'].unique():
    d[i] = [{df_contigs['match'][j]: df_contigs['weight'][j]} for j in df_contigs[df_contigs['query']==i].index]

#iterate through the dictionary to print values to the outfile
#print(d)
with open('./vcontact_contig_results.txt','a',newline='') as out:
    writer1=csv.writer(out,delimiter=';')
    writer2=csv.writer(out,lineterminator='\t')
    for k,v in d.items():
        contig=[]
        for ls in v:
    #        print(ls.items())
            for k2,v2 in ls.items():
                var=str(k2)+"_"+str(v2)
                contig.append(var)
        writer2.writerow([k])
        writer1.writerow(contig)
#                print(k,end='\t')
#                print(*contig,sep=";")




