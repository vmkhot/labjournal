#! usr/bin/python3

import pandas as pd
from pandas import DataFrame
import numpy as np
import pyarrow

gtdb_df = pd.read_csv("./bac120_metadata_r214.tsv.gz", sep="\t", compression='gzip',engine='pyarrow')
#print(gtdb_df)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FILTER GTDB BY CRITERIA + SPECIES LEVEL REPS + SELECT ONE SPECIES AS A ORDER-LEVEL REPRESENTATIVE FROM EACH ORDER

gtdb_Baci_spec_rep_df = gtdb_df.loc[gtdb_df['gtdb_taxonomy'].str.contains('p__Bacillota;') &
                                      gtdb_df['gtdb_representative'].str.contains('t') &
                                      (gtdb_df['checkm_completeness'] >= 90) & (gtdb_df['checkm_contamination'] <= 5) & 
                                      (gtdb_df['checkm_strain_heterogeneity'] == 0)]

# split gtdb taxonomy
gtdb_Baci_spec_rep_df[['domain','phylum','class','order','family','genus','species']]=gtdb_Baci_spec_rep_df['gtdb_taxonomy'].str.split(';', expand = True)

# sort the columns to select genus reps
gtdb_Baci_spec_rep_df.sort_values(by=['genus','gtdb_type_species_of_genus','mimag_high_quality','checkm_completeness','checkm_contamination'],
                                  ascending=[True,False,False,False,True], inplace=True)
print(gtdb_Baci_spec_rep_df)

# select order level representative in all orders
gtdb_Baci_order_rep_df = gtdb_Baci_spec_rep_df.groupby('order').first().reset_index()
print(gtdb_Baci_order_rep_df)

# select genus-lvl representative ONLY in the Lactobacillales order
gtdb_Baci_Lacto_genera_df = gtdb_Baci_spec_rep_df.loc[gtdb_Baci_spec_rep_df['gtdb_taxonomy'].str.contains('o__Lactobacillales')].groupby('genus').first().reset_index()
print(gtdb_Baci_Lacto_genera_df)

# import all species in family Carnobacteriaceae
# carno_df = gtdb_Baci_spec_rep_df.loc[gtdb_Baci_spec_rep_df['gtdb_taxonomy'].str.contains('f__Carnobacteriaceae') & 
#                         (gtdb_Baci_spec_rep_df['checkm_completeness'] >= 95) & (gtdb_Baci_spec_rep_df['checkm_contamination'] <= 5) & 
#                         (gtdb_Baci_spec_rep_df['checkm_strain_heterogeneity'] == 0)]

carno_df = gtdb_df.loc[gtdb_df['gtdb_taxonomy'].str.contains('f__Carnobacteriaceae') & 
                        (gtdb_df['checkm_completeness'] >= 95) & (gtdb_df['checkm_contamination'] <= 5) & 
                        (gtdb_df['checkm_strain_heterogeneity'] == 0)]

# split gtdb taxonomy
carno_df[['domain','phylum','class','order','family','genus','species']]=carno_df['gtdb_taxonomy'].str.split(';', expand = True)
print(carno_df)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GET 10 ACTINOMYCETOTA GENUS LEVEL REPRESENTATIVES RANDOMLY
actino_df = gtdb_df.loc[gtdb_df['gtdb_taxonomy'].str.contains('p__Actinomycetota;') & 
                          gtdb_df['accession'].str.contains('GCF') &
                          (gtdb_df['checkm_completeness'] > 98) & (gtdb_df['checkm_contamination'] <= 2) & 
                          (gtdb_df['checkm_strain_heterogeneity'] == 0)]
# split gtdb taxonomy
actino_df[['domain','phylum','class','order','family','genus','species']]=actino_df['gtdb_taxonomy'].str.split(';', expand = True)
actino_df.sort_values(by=['genus','gtdb_type_species_of_genus','mimag_high_quality','checkm_completeness','checkm_contamination'],
                                  ascending=[True,False,False,False,True], inplace=True)
#print(gtdb_Baci_spec_rep_df)
gtdb_Act_genus_rep_df = actino_df.groupby('genus').first().reset_index()
#print(gtdb_Act_genus_rep_df)

# select 10 random genus level reps with a reproducible seed of 123
df_act_sample = gtdb_Act_genus_rep_df.sample(n=10, random_state=123)
print(df_act_sample)

all_selected_genomes_gtdb = pd.concat([gtdb_Baci_order_rep_df, gtdb_Baci_Lacto_genera_df, carno_df, df_act_sample], ignore_index=True, sort=True).drop_duplicates(subset='accession')

# fix up accessions
all_selected_genomes_gtdb[['RS_GB','accession']]=all_selected_genomes_gtdb['accession'].str.split('_', n=1, expand = True)

all_selected_genomes_gtdb['accession'] = all_selected_genomes_gtdb['accession'].str.replace('GCF','GCA')    #replace all GCF with GCA

all_selected_genomes_gtdb = all_selected_genomes_gtdb.reset_index().set_index('accession')
print(all_selected_genomes_gtdb)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
patric_ncbi_merged_df = pd.read_parquet('patric_ncbi_mapped_df.parquet').set_index('final_accession')
print(patric_ncbi_merged_df)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
merged_gtdb_patric_spec_df = all_selected_genomes_gtdb.merge(patric_ncbi_merged_df, how='left', left_index=True, right_index=True).reset_index()
print(merged_gtdb_patric_spec_df)
merged_gtdb_patric_spec_df.sort_values(by=['gtdb_genome_representative'],ascending=[False],inplace=True)
merged_gtdb_patric_spec_df.drop_duplicates(subset = 'genome_id',inplace=True)
print(merged_gtdb_patric_spec_df)

merged_gtdb_patric_spec_df.to_csv('final_genomes_selection_reducedbyorder.tsv',header=True,sep='\t',index=False)
