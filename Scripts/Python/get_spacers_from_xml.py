# bin/python
import xml.etree.ElementTree as ET
import csv, os, re, operator

outfile="Virus/VirSorter/Results_custom/Analysis/host_predict/crisprs/spacers_test.fna"
tree = ET.parse('Crassout/bioreactor2/crass.crispr') #element-tree parses crass.crispr files
root=tree.getroot() #setting the root of the tree

with open (outfile, 'a', newline='') as out:
    for child in root.iterfind('group'):
        for step_child in child.iterfind('./data/spacers/spacer'):
            g_id=child.get('gid')
            sp_id=step_child.get('spid')
            cov=step_child.get('cov')
            sp_seq=step_child.get('seq')
            out.write('>'+g_id+'_'+sp_id+'_'+'cov'+'_'+cov+'\n'+sp_seq+'\n')





