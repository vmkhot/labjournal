#! usr/bin/python3

import pandas as pd
from pandas import DataFrame
import numpy as np
import pyarrow

gtdb_df = pd.read_csv("./bac120_metadata_r214.tsv.gz", sep="\t", compression='gzip',engine='pyarrow')
#print(gtdb_df)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FILTER GTDB BY CRITERIA + SPECIES LEVEL REPS + SELECT ONE SPECIES AS A GENUS-LEVEL REPRESENTATIVE FROM EACH GENUS

gtdb_Baci_spec_rep_df = gtdb_df.loc[gtdb_df['gtdb_taxonomy'].str.contains('p__Bacillota;') &
                                      gtdb_df['gtdb_representative'].str.contains('t') &
                                      (gtdb_df['checkm_completeness'] >= 90) & (gtdb_df['checkm_contamination'] <= 5) & 
                                      (gtdb_df['checkm_strain_heterogeneity'] == 0)]

# split gtdb taxonomy
gtdb_Baci_spec_rep_df[['domain','phylum','class','order','family','genus','species']]=gtdb_Baci_spec_rep_df['gtdb_taxonomy'].str.split(';', expand = True)

# sort the columns to select genus reps
gtdb_Baci_spec_rep_df.sort_values(by=['genus','gtdb_type_species_of_genus','mimag_high_quality','checkm_completeness','checkm_contamination'],
                                  ascending=[True,False,False,False,True], inplace=True)
#print(gtdb_Baci_spec_rep_df)

# groupby genus and select the first row (best genus representative, hopefully)
gtdb_Baci_genus_rep_df = gtdb_Baci_spec_rep_df.groupby('genus').first().reset_index()
print(gtdb_Baci_genus_rep_df)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# import all species in Carnobacteriaceae

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
print(gtdb_Act_genus_rep_df)

# select 10 random genus level reps with a reproducible seed of 123
df_act_sample = gtdb_Act_genus_rep_df.sample(n=10, random_state=123)
print(df_act_sample)

all_selected_genomes_gtdb = pd.concat([gtdb_Baci_genus_rep_df, carno_df, df_act_sample], ignore_index=True, sort=True)

print(all_selected_genomes_gtdb)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PATRIC METADATA FILE
# needs to be merged with the NCBI assembly to genbank accession mapping file
patric_df = pd.read_csv('./patric_db_files/genome_metadata_patric.tsv', sep='\t', engine='pyarrow')

#NCBI GENBANK MAPPING FILE:
mapping_df = pd.read_csv('./ncbi_files/assembly_genkban_mapping.tsv', sep='\s+',engine='python')
mapping_df['wgs_master'] = mapping_df['wgs_master'].str.split(r'\.').str.get(0)
#print(mapping_df)
#print(patric_df)

patric_filt_df = patric_df[['genome_id','taxon_id','assembly_accession','genbank_accessions','refseq_accessions','patric_cds']]
#print(patric_filt_df)

patric_filt_df['genbank_accessions'] = patric_filt_df['genbank_accessions'].str.split(',') #turn genbank accessions column into a list
patric_filt_df_2 = patric_filt_df.explode('genbank_accessions') #split into individual rows containing genbank accessions
#print(patric_filt_df_2)

#merge ncbi and patric metadata files
patric_ncbi_merged_df = patric_filt_df_2.merge(mapping_df, how='left', left_on='genbank_accessions', right_on='wgs_master',suffixes=['_patric','_ncbi'])
#print(patric_ncbi_merged_df)


# The next command is a conditional search and add to column using numpy.select. E.g. take value from x-column if cond=true, else take value from y-column
# Super fucking useful

patric_ncbi_merged_df['final_accession'] = np.select([patric_ncbi_merged_df['assembly_accession_patric'].str.contains('GC',na=False),
                                                      patric_ncbi_merged_df['assembly_accession_ncbi'].str.contains('GC',na=False)],
                                                      [patric_ncbi_merged_df['assembly_accession_patric'],patric_ncbi_merged_df['assembly_accession_ncbi']],
                                                      default=patric_ncbi_merged_df['assembly_accession_patric'])

patric_ncbi_merged_df.drop(labels=['assembly_accession_patric','genbank_accessions','refseq_accessions','assembly_accession_ncbi','wgs_master'], axis=1, inplace = True)

#print(patric_ncbi_merged_df)

patric_ncbi_merged_df['final_accession'] = patric_ncbi_merged_df['final_accession'].str.replace('GCF','GCA')

patric_ncbi_merged_df.drop_duplicates(subset='final_accession', inplace= True) #remove bullshit column

patric_ncbi_merged_df.to_parquet('patric_ncbi_mapped_df.parquet')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MERGE WITH PATRIC DB METADATA FILE

patric_ncbi_merged_df = pd.read_parquet('gtdb_patric_merged_speciesRep.parquet')


# fix up accessions
all_selected_genomes_gtdb[['RS_GB','accession']]=all_selected_genomes_gtdb['accession'].str.split('_', n=1, expand = True)

all_selected_genomes_gtdb['accession'] = all_selected_genomes_gtdb['accession'].str.replace('GCF','GCA')    #replace all GCF with GCA

# merging GTDB taxonomy and patric_db at species representatives
merged_gtdb_patric_spec_df = all_selected_genomes_gtdb.merge(patric_ncbi_merged_df, how='left', left_on='accession', right_on='final_accession')

merged_gtdb_patric_spec_df.drop_duplicates(subset = 'genome_id',inplace=True)

#merged_final = pd.concat([merged_GB,merged_RS])
#merged_final.drop_duplicates(subset = 'genome_id',inplace=True)

#merged_final.to_csv('gtdb_patric_merged.tsv',header=True,sep='\t')

print(merged_gtdb_patric_spec_df)

merged_gtdb_patric_spec_df.to_csv('final_genomes_selection.tsv',header=True,sep='\t',index=False)
