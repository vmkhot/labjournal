#!/usr/python3

#run this from inside the "tree_build" folder

import csv,re,sys,codecs
pwa_file=sys.argv[1]
outfile=sys.argv[2]

#this section fills key-value pairs with information from naming files. for refseq, virus names (column 2) and taxonomy (column 3) are available 

taxids={}
with open ("/gpfs/home/vmkhot/Databases/July2020_taxid_fullnamelineage_viruses_ascii.csv",'r',encoding="utf-8") as mapfile:
    for line in mapfile:
        line=line.strip('\n')
        cols=line.split(',')
        virus_name=cols[2]+cols[1]
#        print(virus_name)
        taxids[cols[0]]=virus_name
print(taxids.values())

imgtaxids={} #empty array

with open ("../../contigs_v_img/IMGVR_all_Seq_Ecosystem_Info.tsv",'r') as mapfile:
    for line in mapfile:
        line=line.strip('\n')
        cols=line.split('\t')
        projectid=cols[0].split("_____")
        ecosystem=cols[1]+cols[2]+cols[3]+cols[4]+cols[5]
        ecosystem=ecosystem.replace("  ","_")
        #print(cols[0])
        if projectid[0] in imgtaxids.keys():
            next;
        else:
            imgtaxids[projectid[0]]=ecosystem
print(len(imgtaxids.keys()))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`
#This section renames the pwa file using the key-value pairs for _REF and _IMG tags
with open (pwa_file,'r') as pwa,open(outfile,'a',newline='') as out:
    writer=csv.writer(out,delimiter='\t')
    for line in pwa:
        line=line.strip('\n')
        cols=line.split('\t') #split the lines into 3 cols: contig1, contig2, inv_bsr
        if "_REF" in cols[0]:
            refid=re.findall(r'^\d+',cols[0])
            if refid[0] in taxids:
                name1=cols[0]+"_"+taxids.get(refid[0])
            if "_REF" in cols[1]:
                refid2=re.findall(r'^\d+',cols[1])
                if refid2[0] in taxids:
                    name2=cols[1]+"_"+taxids.get(refid2[0])
            elif "IMG_" in cols[1]:
                imgid2=re.findall(r'^\d+|\d+|[^IMG_]+_\w+',cols[1])
                if imgid2[0] in imgtaxids:
                    name2=imgid2[0]+"_"+imgtaxids.get(imgid2[0])
            else:
                name2=cols[1]
            writer.writerow([name1,name2,cols[2]])
        elif "IMG_" in cols[0]:
            imgid=re.findall(r'^\d+|\d+|[^IMG_]+_\w+',cols[0])
            if imgid[0] in imgtaxids:
                name1=imgid[0]+"_"+imgtaxids.get(imgid[0])
            if "_REF" in cols[1]:
                refid2=re.findall(r'^\d+',cols[1])
                if refid2[0] in taxids:
                    name2=cols[1]+"_"+taxids.get(refid2[0])
            elif "IMG_" in cols[1]:
                imgid2=re.findall(r'^\d+|\d+|[^IMG_]+_\w+',cols[1])
                if imgid2[0] in imgtaxids:
                    name2=imgid2[0]+"_"+imgtaxids.get(imgid2[0])
            else:
                name2=cols[1]
            writer.writerow([name1,name2,cols[2]])
        else:
            name1=cols[0]
            if "_REF" in cols[1]:
                refid2=re.findall(r'^\d+',cols[1])
                if refid2[0] in taxids:
                    name2=cols[1]+"_"+taxids.get(refid2[0])
            elif "IMG_" in cols[1]:
                imgid2=re.findall(r'^\d+|\d+|[^IMG_]+_\w+',cols[1])
                if imgid2[0] in imgtaxids:
                    name2=imgid2[0]+"_"+imgtaxids.get(imgid2[0])
            else:
                name2=cols[1]
            writer.writerow([name1,name2,cols[2]])
