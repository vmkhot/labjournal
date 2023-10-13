#! usr/bin/python3

import os
import pandas as pd

path='/bio/data/Aiman/CPR_MAGS/CPR_output_files/csv_results/'

file_list=[path + f for f in os.listdir(path) if f.endswith('.csv')]

csv_list=[]

for file in sorted(file_list):
    csv_list.append(pd.read_csv(file).assign(File_name=os.path.basename(file)))

csv_merged=pd.concat(csv_list,ignore_index=True)

csv_merged.to_csv(path + 'catallresults.csv', index=False)

