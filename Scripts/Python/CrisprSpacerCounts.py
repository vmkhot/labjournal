#! usr/bin/python3

import pandas as pd
from pandas import DataFrame
import numpy as np

#input
in2017="./CC2018_CC2017_spacers_blastn.out"
in2018="CC2018_CC2018_spacers_blastn.out"
in2019="CC2018_CC2019_spacers_blastn.out"
inWGS="CC2018_WGS_spacers_blastn.out"
inlakes="CC2018_lakes_spacers_blastn.out"

#reading in blast files
df2017=pd.read_csv(in2017,sep='\t',header=None,names=['qseqid', 'sseqid', 'pident', 'length', 'mismatch', 'gapopen', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore'])
df2018=pd.read_csv(in2018,sep='\t',header=None,names=['qseqid', 'sseqid', 'pident', 'length', 'mismatch', 'gapopen', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore'])
df2019=pd.read_csv(in2019,sep='\t',header=None,names=['qseqid', 'sseqid', 'pident', 'length', 'mismatch', 'gapopen', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore'])
dfWGS=pd.read_csv(inWGS,sep='\t',header=None,names=['qseqid', 'sseqid', 'pident', 'length', 'mismatch', 'gapopen', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore'])
dflakes=pd.read_csv(inlakes,sep='\t',header=None,names=['qseqid', 'sseqid', 'pident', 'length', 'mismatch', 'gapopen', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore'])

#main filtering for exact match, no unbinned crisprs and small evalue
df2017_1=df2017.loc[(df2017['pident'] == 100) & (df2017['evalue'] <=0.0001) & (~df2017['sseqid'].str.contains('unbinned')) & (df2017['length'] >= 25)]
df2018_1=df2018.loc[(df2018['pident'] == 100) & (df2018['evalue'] <=0.0001) & (~df2018['sseqid'].str.contains('unbinned'))& (~df2018['qseqid'].str.contains('unbinned')) & (df2018['length'] >= 25)]
df2019_1=df2019.loc[(df2019['pident'] == 100) & (df2019['evalue'] <=0.0001) & (~df2019['sseqid'].str.contains('unbinned')) & (df2019['length'] >= 25)]
dfWGS_1=dfWGS.loc[(dfWGS['pident'] == 100) & (dfWGS['evalue'] <=0.0001) & (~dfWGS['sseqid'].str.contains('unbinned')) & (dfWGS['length'] >= 25)]
dflakes_1=dflakes.loc[(dflakes['pident'] == 100) & (dflakes['evalue'] <=0.0001) & (~dflakes['sseqid'].str.contains('unbinned')) & (dflakes['length'] >= 25)]

df2018_1.to_csv('./tmpdf2018_1.tbl',sep='\t')

#split crisprs from spacer numbers
df2017_1[['CC2017_contig','CC2017_spacer']]=df2017_1['qseqid'].str.split(pat='_spacer_',expand=True)
df2017_1[['CC2018_contig','CC2018_spacer']]=df2017_1['sseqid'].str.split(pat='_spacer_',expand=True)

df2018_1[['CC2018_contig_q','CC2018_spacer_q']]=df2018_1['qseqid'].str.split(pat='_spacer_',expand=True)
df2018_1[['CC2018_contig','CC2018_spacer']]=df2018_1['sseqid'].str.split(pat='_spacer_',expand=True)

df2019_1[['CC2019_contig','CC2019_spacer']]=df2019_1['qseqid'].str.split(pat='_spacer_',expand=True)
df2019_1[['CC2018_contig','CC2018_spacer']]=df2019_1['sseqid'].str.split(pat='_spacer_',expand=True)

dfWGS_1[['CCWGS_contig','CCWGS_spacer']]=dfWGS_1['qseqid'].str.split(pat='_spacer_',expand=True)
dfWGS_1[['CC2018_contig','CC2018_spacer']]=dfWGS_1['sseqid'].str.split(pat='_spacer_',expand=True)

dflakes_1[['CClakes_contig','CClakes_spacer']]=dflakes_1['qseqid'].str.split(pat='_spacer_',expand=True)
dflakes_1[['CC2018_contig','CC2018_spacer']]=dflakes_1['sseqid'].str.split(pat='_spacer_',expand=True)

#split lakes into individual lakes
#logic for np.where for NEW and OLD columns. Adds a NEW column to existing dataframe
#df['new column']=np.where(condition,condition_if_true, condition_if_false)
#df['NEW']=np.where(df.OLD.str.contains('randomstring'),df['OLD'],np.nan)
dflakes_1['CCGEM_contig']=np.where(dflakes_1['CClakes_contig'].str.contains('GEM'),dflakes_1['CClakes_contig'],np.nan)
dflakes_1['CCPLM_contig']=np.where(dflakes_1['CClakes_contig'].str.contains('PLM'),dflakes_1['CClakes_contig'],np.nan)

#value_counts now replaces groupby().count()
df2017_2=df2017_1.value_counts(['CC2018_contig','CC2017_contig']).to_frame('count2017')
df2018_2=df2018_1.value_counts(['CC2018_contig','CC2018_contig_q']).to_frame('count2018')
df2019_2=df2019_1.value_counts(['CC2018_contig','CC2019_contig']).to_frame('count2019')
dfWGS_2=dfWGS_1.value_counts(['CC2018_contig','CCWGS_contig']).to_frame('countWGS')
dfGEM_2=dflakes_1.value_counts(['CC2018_contig','CCGEM_contig']).to_frame('countGEM')
dfPLM_2=dflakes_1.value_counts(['CC2018_contig','CCPLM_contig']).to_frame('countPLM')

#merge value_counts dataframes
dfmerge1=df2017_2.merge(df2018_2,on='CC2018_contig',how='outer').merge(df2019_2,on='CC2018_contig',how='outer').merge(dfWGS_2,on='CC2018_contig',how='outer').drop_duplicates().reset_index()
dfmerge2=dfGEM_2.merge(dfPLM_2,on='CC2018_contig',how='outer').drop_duplicates()

dfFINAL=dfmerge2.merge(dfmerge1,on='CC2018_contig',how='outer').reset_index()
print(dfFINAL)

dfFINAL.to_csv('./crisprarraycounts.tbl',sep='\t',index=False)


