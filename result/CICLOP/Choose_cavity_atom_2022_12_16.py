#!/usr/bin/python3
"""
Title: Choosing lines with "99999"
Date: 2022 December 12
Author: Huimin Lu

Description:
    The input file is "*-inner_surface_marked.pdb".In these files, the lines with "99999" are the atoms one the cavity surface.
    This program is to find the atom with "99999" and leave these lines in output file.

Procedure:
    1, Read "merge_data" file, adding PDB ID in list "PDB_list",
        adding Chain character in list "Chain_list"
    2, Checking whether this PDB ID has cavity file
    3, If it has, read this cavity PDB file.
    4, Read every line, leave the line that contain "99999"
    5, close this file
    6, Start looking at next PDB ID
    
Usage:
    python Choose_cavity_atom.py [merge_data] [input_directory] [output_directory]
    
    For Example:
    cd CICLOP/
    python Choose_cavity_atom_2022_12_16.py merge_data_11_23.tsv all_inner_surface/ only_cavity/ Amino_Acid_Count.tsv

"""

import sys
import os

PDB_Chain=open(sys.argv[1],'r')#"PDB_Chain" contain all PDB ID and Chain character and other information


PDB_list=[]#"PDB_list" is to contain all PDB ID
Chain_list=[]#"Chain_list" is to contain a lot of sublist which will include chain chearacter

##Adding PDB ID and Chain character into empty list
PDB_Chain.readline()#skip the first line
for line in PDB_Chain:#read every line
    line=line.strip().split('\t')# transform string into list called "line"
    # ['7ena', 'Cyclin-H', 'C', 'P51946', '287', '4.07', '3', '289']
    if line[0] not in PDB_list:#a new PDB_ID
        PDB_list.append(line[0])#Adding this PDB_ID into list "PDB_list"
        Chain_list.append([])#append a new sublist in "Chain_list"
        y=PDB_list.index(line[0])#y is the index of this PDB_ID
        Chain_list[y].append(line[2])#adding chain character into sublist whose index is y
    else:#this PDB ID exists in list "PDB_list"
        y=PDB_list.index(line[0])#y is the index of this PDB_ID
        Chain_list[y].append(line[2])#adding chain character into sublist whose index is y

cavity_directory=sys.argv[2] #it is directory of cavity PDB files, more than 30000 files
output_directory=sys.argv[3] #is is directory of output file, more than 30000 files
Amino_Acid_count=open(sys.argv[4],"w")#output file


#Wiring First line into output file
Amino_Acid=["ALA","ARG","ASN","ASP","CYS","GLU","GLN","GLY","HIS","ILE","LEU","LYS","MET","PHE","PRO","SER","THR","TRP","TYR","VAL"]
first_line='\t'.join(Amino_Acid)
print("{}\t{}".format("PDB_ID",first_line),file=Amino_Acid_count)

#list contain whole amino acid
amount=[]#"amount" contain 20 sublist, each sublist contain digits of position
number_of_Amino_Acid=[]#"number_of_Amino_Acid" contain 20 numbers, the amount of each amino acid

#adding 20 sublist into list "amount" and "acvity_amount"
for i in range(0,len(Amino_Acid)):
    amount.append([])#add 20 sublist [] 

for ID in PDB_list:
    # print(ID)
    input_file=ID+"-inner_surface_marked.pdb"
    input_path=str(cavity_directory)+input_file
    if os.path.exists(input_path):
        CICLOP=open(input_path,"r")
        ##open out put file
        output_file=ID+"_cavity.pdb"
        output_path=str(output_directory)+output_file
        inner_cavity=open(output_path,'w')#"inner_cavity"contains lines that only have inner cavity
        
        ##extract the PDB ID and Chain character
        PDB_ID=ID#"PDB_ID" is current PDB ID we are impelement 
        y=PDB_list.index(PDB_ID)#"y" is index of current PDB ID
        Chain_character=Chain_list[y]#"Chain_character" is the entity we chosen previously.
        
        #list contain whole amino acid
        amount=[]#"amount" contain 20 sublist, each sublist contain digits of position
        number_of_Amino_Acid=[]#"number_of_Amino_Acid" contain 20 numbers, the amount of each amino acid

        #adding 20 sublist into list "amount" and "acvity_amount"
        for i in range(0,len(Amino_Acid)):
            amount.append([])#add 20 sublist [] 

        ##Read cavity PDB file, line by line
        for line in CICLOP:#read every atom in PDB file
            line=line.strip()# transform string into list called "line"
            if line=="END":#this is last line of this PDB file
                pass
            else:# these lines have informatiob of atoms
                chain=line[21].strip()#chain character in the line
                cavity=line[60:66].strip()#if this atom is on surface it is "99999", otherwise it is "0"
                amino=line[17:20].strip()
                position=line[22:26].strip()
                
                if chain in Chain_character:#in the chain list    
                    if amino in Amino_Acid:
                        y=Amino_Acid.index(amino)#"y" is the position of amimo acid 
                        amount[y].append(position)#add this position in the sublist
                        if cavity=="99999":#it is cavity
                            inner_cavity.write("{}\n".format(line))
        for sublist in amount:#read every sublist one by one.
            number_of_Amino_Acid.append(len(set(sublist)))
        number_of_Amino_Acid=[str(x) for x in number_of_Amino_Acid]
        Amino_Acid_count.write("{}\t{}\n".format(PDB_ID,'\t'.join(number_of_Amino_Acid)))
        
        CICLOP.close()
        inner_cavity.close()
PDB_Chain.close()
Amino_Acid_count.close()

