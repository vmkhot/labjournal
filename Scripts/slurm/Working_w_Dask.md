 Dask is an python library used for parallelization of code, including pandas using [Dask dataframes](https://saturncloud.io/docs/examples/python/dask/collections/qs-dask-collections-dask-dataframe/)
To use with slurm in sbatch mode is simplest. interactive mode (salloc + srun) is trickier because you are only allocated a single node

To install the libraries:

```
conda install dask
conda install dask distributed -c conda-forge
conda install dask-mpi -c conda-forge
conda install dask-jobqueue -c conda-forge

#to use dask mpi, also need openmpi

```

Example sbatch script: Here we request 20 cpus across 5 nodes and 200 GB in total. - that's 100 processes? 
I assigned 
Each worker gets 10 GB
This is too many - more success with less workers (<20)

```
#!/bin/bash
#SBATCH --job-name=dask-py      # Job name
#SBATCH --nodes=5                    # Run all processes on a 10 node
#SBATCH --cpus-per-task=15            # Number of CPU cores per task
#SBATCH --mem=200G                    # Job memory request
#SBATCH --partition=standard,short,long,fat
#SBATCH --output=dask-py%j.log     # Standard output and error log

#SBATCH --mail-user=varada.khot@uni-jena.de     #email user
#SBATCH --mail-type=BEGIN                       #email when job begins
#SBATCH --mail-type=END                         #email when job ends

echo "Running Dask-MPI"

module load mpi/openmpi/4.1.1

source /vast/ri65fin/miniconda3/etc/profile.d/conda.sh

conda activate working-env  # Activate conda environment 


mpirun --oversubscribe -np 15 python3 filter_diamond_get_clusters.py
```

Example python script:

```
#! usr/bin/python3

'''
For these large dataframes:
0.5. I used "sort -u" on the command line to get just the sequence IDs of the sseqid, 
    sort them and deduplicate, instead of reading in full blast output
1. I used the dask library (which parallelizes pandas) to read in my tsv files dd.read_csv instead of pd.read_csv
2. set_index to the columns I wanted to merge on and used df.join() instead of df.merge()
''' 

import pandas as pd
from pandas import DataFrame
import dask.dataframe as dd
from dask.distributed import Client
#from dask_jobqueue import SLURMCluster
from dask_mpi import initialize


initialize()

client = Client()  # Connect this local process to remote workers


 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# INITIAL READ INS
# diamond_df = dd.read_csv("./MGYP_v_pharokka_blastp.tsv", sep="\t", header=None,blocksize = '64MB',
#                          names=['qseqid', 'sseqid','pid','length','mismatch','gapopen','qstart','qend','sstart','send','evalue','bitscore'])

clusters_df = dd.read_csv("/home/ri65fin/MCP_struct/mgnify_databases/mgy_cluster_seqs.tsv", sep="\t", header=None, blocksize = '64MB',
                          names=['representative','cluster_seq']).set_index('representative')
print("1...clusters_df read")
print(type(clusters_df))
#print(clusters_df.head(n=10), len(clusters_df))
clusters_df = client.persist(clusters_df)


uniq_mgyp_id = dd.read_csv("./mgyp_CR_uniq.list", sep="\t", header=None, names=['CR']).set_index('CR')
print("2...uniq_mgyp_id read")
print(type(uniq_mgyp_id))

# uniq_mgyp_id = diamond_df[['sseqid']].sort_values(by='sseqid', inplace=True).drop_duplicates()
print(uniq_mgyp_id.head(n=10), len(uniq_mgyp_id))
uniq_mgyp_id = uniq_mgyp_id.repartition(npartitions=1)
uniq_mgyp_id = client.persist(uniq_mgyp_id)

#merged_df = uniq_mgyp_id.merge(clusters_df, how = "left", left_on='sseqid', right_on='representative')
# merging large dataframes is too expensive. A better method is to set_index on the merging columns and use a join on a left index instead

merged_df = uniq_mgyp_id.join(clusters_df,how='left')
merged_df = client.persist(merged_df)

print("3... joining dataframes done")

#print(merged_df.head(n=10), len(merged_df))
merged_df = merged_df.repartition(npartitions=10).reset_index()
merged_df = client.persist(merged_df)

merged_df.to_parquet('uniq_cluster_seqs.parquet')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#read in normal dataframe

#merged_df = dd.read_parquet('uniq_cluster_seqs.parquet')

merged_df['cluster_seq'] = merged_df['cluster_seq'].str.split(";")
merged_df = client.persist(merged_df)


merged_df = merged_df.explode('cluster_seq').reset_index(drop=True)     #single column into multiple rows
merged_df = client.persist(merged_df)  
print("4... dataframe exploded")

print(merged_df.head(n=10), len(merged_df))

merged_df = merged_df.repartition(npartitions=1)
merged_df = client.persist(merged_df)


merged_df.to_csv('uniq_cluster_seqs.tsv', sep='\t', index=False)

```
