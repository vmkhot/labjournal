#! usr/bin/python3

import pandas as pd
from pandas import DataFrame
from pathlib import Path
import os, shutil               # for directory and file control commands like cp and mv
import urllib.request           # for downloading from ftp
import csv


genomes_df = pd.read_csv('../final_genomes_selection_reducedbyorder.tsv',header=0,sep='\t')

#genomes_df = genomes_df_0.sample(n=100, random_state=123)
#print(genomes_df)

# genomes_list = genomes_df["genome_id"].tolist()
"""
assign {genome_id: ['accession','ncbi_assembly_name']} dictionary from my dataframe.

"""
genome_list = genomes_df.set_index(genomes_df["genome_id"])[['accession','ncbi_assembly_name']].values.tolist()
genome_dict = dict(zip(genomes_df['genome_id'],genome_list))
print(genome_dict)


source_path = Path('/ceph/common/VEO/databases/genomes_bacteria_bvbrc/genomes/bacteria/all_files')
dest_path = Path('./aa_files_new')
ftp_path = 'ftp://ftp.bvbrc.org/genomes'
"""
Need to add something to deal with files that are not found:
0.5. first try without the decimal point
1. can wget from ftp instead
2. if not found in folder or wget, print to a file that genome wasn't found
"""

for key,value in genome_dict.items():
    cds_path = os.path.join(source_path, str(key), f"{key}.PATRIC.faa")
    if os.path.isfile(cds_path):
        #print(cds_path)
        new_path = os.path.join(dest_path, f"{key}.PATRIC.faa")
        shutil.copyfile(cds_path, new_path)
    else:
        with open ('genomes_found_where.tsv', 'a+') as f:
            try:
                # attempt to get file from ftp site
                urllib.request.urlretrieve(f"ftp_path/{key}/", f"{key}.PATRIC.faa")
                print(ftp_new_path)
                # write to file
                f.write('ftp' + '\t' + str(key) + '\t' + + value[0] + '\t' + value[1] + '\n')

            except:
            # print to a file that the record or accession wasn't found
                f.write('not_found' + '\t' + str(key) + '\t' + value[0] + '\t' + value[1] + '\n')
                

#genbank ftp link format
#https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/001/644/195/GCA_001644195.2_ASM164419v2/GCA_001644195.2_ASM164419v2_genomic.fna.gz
