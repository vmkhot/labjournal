#! usr/bin/python3

'''
Script will iterate through faa fasta files in a dir,
- Check the number of sequences of in the fasta file
- if num > 3, move them to a new directory
To iterate through a series of dirs named like "dir_1, dir_2...",
use the i(range for loop
'''

import glob, os
from pathlib import Path
import shutil

#for i in range(1,104):
for file in Path(f"./dir/").glob("*.faa"):
    num = len([1 for line in open(file) if line.startswith(">")])
    #print(num)
    if num > 3:
        new_path = str(file.resolve()).replace(f"dir", "seq_mt_3")
        shutil.move(file, new_path)
