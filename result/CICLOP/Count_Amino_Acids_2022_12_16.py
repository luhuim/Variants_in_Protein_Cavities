#!/usr/bin/python3
"""
Title: Choosing lines with "99999"
Date: 2022 December 12
Author: Huimin Lu

This program is to calculate the amino acid that on cavity surface. And this program has threshold choice.
If threshold is 2, that means the amino acids that will be counted in at lease have two atoms on cavity surface.


argv[1]=PDB_list
argv[2]=threshold
argv[3]=cavity_directory
argv[4]=output_cavity_amino_acid


Usage:
    python Count_Amino_Acids_2022_12_16.py PDB_ID_list.tsv 2 only_cavity/ Cavity_Amino_acid_2.tsv
"""

import sys
import os
from collections import Counter

PDB_List=open(sys.argv[1],'r')#input file
threshold=sys.argv[2]#each amino acid should have at least two atoms on cavity surface 
cavity_directory=sys.argv[3] #this is directory that contain cavity PDB files
cavity_Amino_Acid_count=open(sys.argv[4],"w")#output file

#Wiring First line into output file
Amino_Acid=["ALA","ARG","ASN","ASP","CYS","GLU","GLN","GLY","HIS","ILE","LEU","LYS","MET","PHE","PRO","SER","THR","TRP","TYR","VAL"]
first_line='\t'.join(Amino_Acid)

print("{}\t{}".format("PDB_ID",first_line),file=cavity_Amino_Acid_count)




#whether the pdb has cavity PDB file
for ID in PDB_List:
    ID=ID.strip()#remove new line sign
    input_file=ID+"_cavity.pdb"
    input_path=str(cavity_directory)+input_file
    if os.path.exists(input_path):
        cavity=open(input_path,"r")
        
        #Create list that contain 
        #list contain position digits of amonoacid 
        cavity_amount=[]#"amount" contain 20 sublist, each sublist contain digits of position
        cavity_number_of_Amino_Acid=[]#"number_of_Amino_Acid" contain the amount of each amino acid

        #adding 20 sublist into list "amount" and "acvity_amount"
        for i in range(0,len(Amino_Acid)):
            cavity_amount.append([])
        #Fill cavity_amount
        for line in cavity:#read PDB file line by line
            line=line.strip()# transform string into list called "line"
            #[ATOM, 690, OD2, ASP, A, 136, 51.513, 28.67, 94.558, 1.00, 99999, O ]

            amino=line[17:20].strip()#Aminoq Acid
            position=line[22:26].strip()#Position of Amino Acid

            if amino in Amino_Acid:#whether this atom is from amino acid
                y=Amino_Acid.index(amino)#y is the index of amino acid of this line
                #add into cavity amino acid
                cavity_amount[y].append(position)#adding the position of this amino acid into correspond sublist 
        #check the threshold
        for sub_list in cavity_amount:
            result = Counter(sub_list)#result is a dictionary, key is position digit,value is the amount of atoms
            print("dic",result)
            digit=list(result.keys())#position
            print("position",digit)
            amount=list(result.values())#the number of atom in each amino acids
            print("number of atoms",amount)
            i=0
            uniq=[]
            for n in amount:#n is the number of atoms from one amono acid that is  on the surface
                if n>=int(threshold):#the number of atoms are >= threshold
                    uniq.append(digit[i])
                    i+=1
                else:#the atoms from this amino acid is lower than sreshold
                    i+=1
                    pass
            uniq=list(set(uniq))
            cavity_number_of_Amino_Acid.append(len(uniq))
            
            
        # PDB_List=open(sys.argv[1],'r')#input file
        # threshold=sys.argv[2]#each amino acid should have at least two atoms on cavity surface 
        # cavity_directory=sys.argv[3] #this is directory that contain cavity PDB files
        # cavity_Amino_Acid_count=open(sys.argv[4],"w")#output file
        cavity_number_of_Amino_Acid=[str(x) for x in cavity_number_of_Amino_Acid]
        cavity_Amino_Acid_count.write("{}\t{}\n".format(ID,'\t'.join(cavity_number_of_Amino_Acid)))
        cavity.close()
PDB_List.close()
cavity_Amino_Acid_count.close()



