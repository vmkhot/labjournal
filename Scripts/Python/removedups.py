import numpy as np

#File import

#open text file as read only
file1 = open('examplesfile.fasta', 'r') #filepath if you're already in directory, otherwise need full filpath

allText = file1.read() #read in text

#open write-only output file
outFile = open('MODexamplesfile.fasta','w') #filepath if you're already in directory, otherwise need full filpath

Entries=allText.split('>') #split text into discrete entries using > header char
del(Entries[0]) #the very first entry is empty

IDs=[]

for entry in Entries: #for each fasta entry

    IDend=entry.find('.') #End of each fasta ID is '.'
    print('ID end index is', IDend)
    
    ID=entry[:IDend]
    print('ID is: ',ID)
    
    IDs.append(ID) #collect IDs in to a list

    TaxStart=entry.find(' ')
    TaxEnd=entry.find('\n')
    
    print('\nTaxonomy is', entry[TaxStart:TaxEnd])

print('\n')
    
for ID in np.unique(IDs):  #for each unique ID #this  is numpy function - it will return only unique items from  list
    if IDs.count(ID)> 1:    #if it occurs more than once
        print(ID,' has ',IDs.count(ID),' duplicates')

        inds= [i for i, x in enumerate(IDs) if x == ID] #get indexes where they occur in IDs list (which should be same ordering as Entries list)
        
        del(Entries[inds[-1]]) #get the last index in the list of indexes, and delete the corresponding entry in Entries

outStr = ">" #initialize an empty string - it will join the strings with a >

outStr=outStr.join(Entries) #join all entries from modified Entries list into on string of text

outFile.write(outStr) #file output

#close all files
file1.close()
outFile.close()
