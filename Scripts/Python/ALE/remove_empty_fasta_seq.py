#! usr/bin/python3

from Bio import SeqIO
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_faa')
    parser.add_argument('--out_faa')
    return parser.parse_args()

args=parse_arguments()
in_faa = args.in_faa
out_faa = args.out_faa

with open (in_faa, 'r+') as in_put, open (out_faa, 'a+') as out_put:
    for current_seq in SeqIO.parse(in_put, "fasta"):
        if str(current_seq.seq) != '':
            #seq = str(current_seq.seq).lstrip(' ')
            #seqid = str(current_seq.id).lstrip(' ')
            out_put.write(">" + str(current_seq.description) + "\n" + str(current_seq.seq) + '\n')
