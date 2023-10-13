#!usr/bin/python3

#This program takes genbank.gz input from the ncbi ftp and writes a amino acid fasta file and a mapping file for taxonomy using BioPython SeqIO module
#


from Bio import SeqIO
import gzip
import re

with gzip.open ("viral.all.protein.gpff.gz",'rt') as genbank, open ("./viral.all.taxonomy.faa",'a') as fasta, open ("./genbankid_taxonomy_map.tsv", 'a') as mapper:
    counter=0
    for record in SeqIO.parse(genbank,"genbank"):
        counter = counter + 1
        print("parsing..." + record.id + "..." + str(counter))
#        print(record)  #just to see the format of the object
        for feature in record.features:
            if 'source' in feature.type:
                taxid=''.join(feature.qualifiers['db_xref'])
                taxid=re.sub(r'.*taxon:','',taxid)          #get taxid from the db_xref line
                mapper.write(record.id + '\t' + taxid + '\t' + str(';'.join(record.annotations['taxonomy'])) + '\t' + record.annotations['source'] + '\n')     #write mapping file with protein accession, taxid, full taxonomy, common name
                fasta.write(">"+ record.id + "|" + record.description + "\n" + str(record.seq) + "\n")   #write fasta with protein accession as the header