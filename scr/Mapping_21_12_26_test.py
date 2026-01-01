#!/usr/bin/python3
"""
试验品
Title: Choosing lines with "99999"
Date: 2022 December 12
Author: Huimin Lu

Description:
    This program is to map variant on PDB cavity file.
    This program will leave the PDB ID whose cavity-surface amino acids have variants, and record the variant in output file

Procedure:
    1, open "variant.tsv" and put the information into a dataframe.
    2, open "merge_data_11_23.tsv" and read each line
        2.1, when reading the line, extract the UniprotID, and extract sub-DataFrame which has this Uniprot ID 
        2.2, check whether this Uniprot ID has variant:
            2.3, If it has variant, then check whether this PDB ID has cavity file, if it has cavity PDB file, open it
            2.4, read cavity PDB file, line by line. When read line, search the 

Usage:

    argv[1]=variant_file
    argv[2]="merge_data_11_23.tsv"
    argv[3]=cavity_directory "only_cavity/"
    argv[4]=output_cavity_variant_information
    
    

"""

import re
import requests
import sys
import os
import pandas as pd #To read the data set



#Read the variant file, create a datafram
variant_list= pd.read_csv(sys.argv[1],sep='\t',index_col=None)
# variant_list= pd.read_csv("variant.tsv",sep='\t',index_col=None,)
df=pd.DataFrame(variant_list)#"df" is a dataframe of variant

info=open(sys.argv[2],'r')# "info" is "merge_data" file

cavity_directory=sys.argv[3]
cavity_variant=open(sys.argv[4],'w')#"cavity_variant" is an output file

#First line of output file
cavity_variant.write("PDB\tCHAIN\tUniprotID\tAnnotation\tVariantion Text\n")

link="http://www.bioinf.org.uk/servers/pdbsws/query.cgi?plain=2&qtype=ac&id="

#Create a dictionary of amino acid. 
#key is 3 character, value is one character
amino_dic={}
amino_dic["ALA"]="A"
amino_dic["ARG"]="R"
amino_dic["ASN"]="N"
amino_dic["ASP"]="D"
amino_dic["CYS"]="C"
amino_dic["GLN"]="Q"
amino_dic["GLU"]="E"
amino_dic["GLY"]="G"
amino_dic["HIS"]="H"
amino_dic["ILE"]="I"
amino_dic["LEU"]="L"
amino_dic["LYS"]="K"
amino_dic["MET"]="M"
amino_dic["PHE"]="F"
amino_dic["PRO"]="P"
amino_dic["SER"]="S"
amino_dic["THR"]="T"
amino_dic["TRP"]="W"
amino_dic["TYR"]="Y"
amino_dic["VAL"]="V"

Amino_Acid=amino_dic.keys()#"Amino_Acid" is a list of 20 amino acids.

#read "merge_data" line by line
info.readline()
for line in info:#read every line in "merge_data"
    line=line.strip().split('\t')# transform string into list called "line"
    # ['7ena', 'Cyclin-H', 'C', 'P51946', '287', '4.07', '3', '289']
    PDB=line[0].strip()
    uniprot=line[3].strip()
    
    #Firstly,Check whether Current Uniprot ID has variant
    #"variant_position" include all variant position of current uniprot ID 
    variant_position=list(df[df["UniprotID"].str.contains(uniprot)]["mut_residue"])#[80, 80, 78]
    variant_position=[int(x) for x in variant_position]
    #"variant_position" include all variation text of current uniprot ID 
    variation_text=list(df[df["UniprotID"].str.contains(uniprot)]["Variation"])#[I80S, I80H, Y78I ]
    # print("variation_text",variation_text)
    #"variant_dic" is to contain position of variant and its original amino
    # variant_dic={}#key is position, value is single letter of original amino acid
    # for i in range(0,len(variant_position)):#add all position in list "variant_position" into dictionary
    #     variant_dic[str(variant_position[i])]=variation_text[i][0]#index 0 is original letter
    uniq_position=list(set(variant_position))#"uniq_position"
    
    #check whether current Uniprot ID has variant
    if len(variant_position)==0:#if this Uniprot ID does't have variant.
        print("This Uniprot ID does't have variant")
        print("#####################################################################################")
        pass#Current Uniprot ID doesn't have variant
    else:#Current Uniprot ID has variants
        print("#####################################################################################")
        print("PDB ID", PDB)
        print("Uniprot ID:",uniprot)
        print("DataFrame\n", df[df["UniprotID"].str.contains(uniprot)])
        print("list",variant_position,variation_text)
        
        input_file=PDB+"_cavity.pdb"
        input_path=str(cavity_directory)+input_file
        if os.path.exists(input_path):#if this PDB ID has cavity file
            #### Create some list 
            full_list=[]
            summary_list=[]
            for x in uniq_position:# "x" is every unique variant position
                # Connecting API, We need settel Uniprot ID and variant position in Uniprot
                response = requests.get("{}{}&res={}".format(link,uniprot,str(x)))#ask for request
                first_dic= response.json()#this is result
                # Find the current PDB's correspond position among result
                
                # add all candidate PDB ID into list "temp_PDB"
                for i in range(0,len(first_dic["pdbsws"])):
                    if first_dic["pdbsws"][i]['PDB']==PDB:
                        if first_dic["pdbsws"][i]['CHAIN']==line[2]:
                            letter=first_dic["pdbsws"][i]["PDBAA"]
                            p=first_dic["pdbsws"][i]['RESID']#"p" is positon in current PDB
                            p=str(re.sub(r'[A-Z]',"",p.strip()))#remove the letter in "p"
                            full_list.append([str(x),p,letter])#add a sub list into "full_list",[61,1,K], [uniprot position, pdb position, amino acid character]
                            summary_list.append(p)#"summary_list" include all PDB position of variant
            #After finish checking all Unique variant position, we check whether the found PDB position
            if len(summary_list) ==0:#There is no corresponding position in current PDB
                pass#skip
            else:#It has some position in current PDB
                ######Open this PDB file and Read this Cavity PDB file
                cavity=open(input_path,"r")#open this cavity file
                
                position_on_cavity=[]
                text=[]
                for l in cavity:#read PDB file line by line
                    l=l.strip()# transform string into list called "line"
                    #[ATOM, 690, OD2, ASP, A, 136, 51.513, 28.67, 94.558, 1.00, 99999, O ]
                    amino=l[17:20].strip()#Aminoq Acid
                    position=l[22:26].strip()#Position of Amino Acid
                    position=str(re.sub(r'[A-Z]',"",position.strip()))#remove character among position
                    chain=l[21].strip()#chain character in the line
                    
                    if chain == line[2]:#whethe current line belongs to chains that corespond to Uniprot ID
                        # print("Current Chain:",chain,"Uniprot Chain:",line[2])
                        if str(position) in summary_list:#if current position is among "variant position"
                            # print("current amino acid is variant",position, variant_in_PDB)
                            if amino in Amino_Acid:#this amino acid in among 20 amino acids
                                # print("This is a regular amino acid")
                                y=summary_list.index(str(position))#"y" is the index of this position in both "full_list" and "summary_list"
                                if amino_dic[amino]==full_list[y][2]:# current amino acid (single letter) is same as that in API
                                    # print("********************")
                                    print(l)
                                    print("variant position in Uniprot",full_list[y][0])
                                    print("variant position in PDB", full_list[y][1])
                                    print("The amino acid is:",amino, amino_dic[amino])
                                    #### After finding a variant on cavity surface,add "variation text" into "text"
                                    for i in range(0,len(variant_position)):#check "variant_position" one by one
                                        if int(variant_position[i])== int(full_list[y][0]):#if we found a position that match
                                            # print("we make it @@@@@@@@@@")
                                            position_on_cavity.append(int(variant_position[i]))
                                            text.append(variation_text[i])#add this position's variation text into "text"
                                        # else:#This element does't match
                                        #     print("!!!!!!!!!!,failure in adding text")
                                else:#this amino acid is not in among 20 amino acids
                                    pass
                                    # print("&&&&&&&&&&&&&&&&&&&&&& single letter doesn't match", "in PDB file:",amino_dic[amino],"in variant:",variant_dic[str(position)])
                            else:#this amino acid is not in among 20 amino acids
                                pass
                                # print("This amono acid is innormal########################")
                        else:#current position is not among "variant position
                            # print("This amino acid doesn't belong to variants",position, variant_in_PDB)
                            pass
                    else:
                        pass
                        # print("Chain character doesn't match", "This chian:", chain,"The Uniprot ID should be:",line[2])
                        
                text=list(set(text))#removing repeated element
                
                
                for element in list(set(position_on_cavity)):#Write information of all amino acid on cavity, include variant position in Uniprot and text
                    sub_text=list(df[df["UniprotID"].str.contains(uniprot)][df["mut_residue"]==int(element)]['Variation'])
                    print(element,"\t",sub_text)
                print("Unique Variant Position:",summary_list.sort())
                print("variation text:",text)
                
                
                if len(text)!=0:
                    cavity_variant.write("{}\t{}\t{}\t{}\t{}\n".format(PDB,line[2],uniprot,line[1],','.join(text)))
                    print("in output file:")
                    print("{}\t{}\t{}\t{}\t{}\n".format(PDB,line[2],uniprot,line[1],','.join(text)))
                
                
                position_on_cavity=[]
                text=[]
                summary_list=[]
                full_list=[]
                cavity.close()
                print("###############################################################################")
        else:#this PDB ID doesn't have cavity file
            print("This PDB doesn't have cavity PDB file")
            print("###############################################################################")
            pass
cavity_variant.close()

# #%%
# import pandas as pd #To read the data set
# variant_list= pd.read_csv("variant.tsv",sep='\t',index_col=None)
# # variant_list= pd.read_csv("variant.tsv",sep='\t',index_col=None,)
# df=pd.DataFrame(variant_list)#"df" is a dataframe of variant
# # print(df.info())


# sub_text=list(df[df["UniprotID"].str.contains("Q9Y4U1")][df["mut_residue"]==161]['Variation'])
# print(sub_text)
    

