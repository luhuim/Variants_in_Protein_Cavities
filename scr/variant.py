#!/usr/bin/env python3
"""
Title: Finding variant that have PDB structure. 
Date: 2022 May 19
Author: Huimin Lu

Description:
    Not all variants have PDB structure. 
    The file "PDB_list" incluse Uniprot_IDs that both exist in "All_species_train.csv", and have PDB structure.  
    This program is to select the variants whose Uniprot _ID is in file "PDB_list". 
    The input file "All_species_train.csv", if this variant's Uniprort ID exist in file "PDB_list", it will be putput.

List of functions:
    None
    
List of "non standard modules":
    None
    
Procedure:
    1, import "PDB list", and add all Uniprot ID in dictionary
    2, a loop for lines in "All_species_train.csv", if Uniprot in variants exist in dictionary, it will be output in file
    
Usage:
    
    Conmmand line: python variant.py [variant list] [PBD list] [output file]
    for example:
    python scr/variant.py data/All_species_train.csv result/collect_PDB/first_parse.tsv result/variant_info/variant.tsv
    
"""
import sys

whole=open(sys.argv[1],'r')# large one
selection=open(sys.argv[2],'r')#this is PDB list

#open the file we want to output
t=open(sys.argv[3],'w')
t.write('Protein\tVariation\tUniprotID\tis_del\tmut_residue\tnutation\tlen\n')#writing the header of output file
#collect 
selection.readline()#pass the header
ID_Collection=[]#this list is to collect Uniprot ID 

for line in selection:
    content=line.split('\t')#split line (string) into a list, called content
    ID=content[2].strip()# the third element is the protein ID we want to collect, extract this element into variable called "ID"
#    print(ID)
    ID_Collection.append(ID)
#print("What kinds of Uniprot ID?",len(set(ID_Collection)))
# print("list",ID_Collection)

whole.readline()#the first line pass
for line in whole:
#    print(line)
    content_2=line.split(',')#split line (string) into a list, called content_2 
    content_2=content_2[0:7]
#    print(content_2)
#    print(content_2[2])
    if content_2[2].strip() in ID_Collection:#if the Uniport id in the list 
#         print("in")
         result="\t".join(content_2[0:7])
         t.write("{}\n".format(result))
t.close()
selection.close()
whole.close()        
        