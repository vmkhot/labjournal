#! usr/bin/python3

import pandas as pd
from pandas import DataFrame
import numpy as np
import pyarrow

gtdb_df = pd.read_csv("./bac120_metadata_r214.tsv.gz", sep="\t", compression='gzip',engine='pyarrow')
#print(gtdb_df)

gtdb_Baci_spec_rep_df = gtdb_df.loc[gtdb_df['gtdb_taxonomy'].str.contains('p__Bacillota') & 
                                    gtdb_df['gtdb_representative'].str.contains('t') & 
                                    (gtdb_df['checkm_completeness'] >= 90) & (gtdb_df['checkm_contamination'] <= 5)]


# split GTDB taxonomy
gtdb_Baci_spec_rep_df[['domain','phylum','class','order','family','genus','species']]=gtdb_Baci_spec_rep_df['gtdb_taxonomy'].str.split(';', expand = True)

#print(gtdb_Baci_spec_rep_df)


# sort the columns to select genus reps
gtdb_Baci_spec_rep_df.sort_values(by=['genus','gtdb_type_species_of_genus','mimag_high_quality','checkm_completeness','checkm_contamination'],
                                  ascending=[True,False,False,False,True], inplace=True)

print(gtdb_Baci_spec_rep_df)
# groupby genus and select the first row (best genus representative, hopefully)
gtdb_Baci_genus_rep_df = gtdb_Baci_spec_rep_df.groupby('genus').first().reset_index()
print(gtdb_Baci_genus_rep_df)

gtdb_Baci_genus_rep_df.to_csv('gtdb_genus_representatives.tsv', sep='\t',header=True,index=False)
