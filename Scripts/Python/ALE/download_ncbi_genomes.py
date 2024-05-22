#! usr/bin/python3

#genbank ftp link format
#https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/001/644/195/GCA_001644195.2_ASM164419v2/GCA_001644195.2_ASM164419v2_genomic.fna.gz

"""
1. Get genbank accessions and assembly names
2. Split into variables
3. Create ftp link
4. Download to a genomes dir
"""

from pathlib import Path
import os, shutil               # for directory and file control commands like cp and mv
import urllib.request

ftp_path = "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA"

# GCA 016 342 455

with open ("../genomes_found_where.tsv", 'r') as accessions:
    for line in accessions:
        cols=line.strip('\n').split('\t')
        genbank = cols[2]
        assembly = cols[3]
        first = genbank[4:7]
        second = genbank[7:10]
        third = genbank[10:13]
        #print(first, second, third)
        ftp_retrieve = str.join('/',(ftp_path, str(first), str(second), str(third),f"{genbank}_{assembly}",f"{genbank}_{assembly}_genomic.fna.gz"))
        print(ftp_retrieve)
        try:
            urllib.request.urlretrieve(ftp_retrieve,f"./{genbank}_{assembly}_genomic.fna.gz")
        except:
            pass
