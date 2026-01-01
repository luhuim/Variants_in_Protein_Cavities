#!/usr/bin/python3
"""
Title: Finding Entity in PDB
Date: 2022 September 27
Author: Huimin Lu
Version: A[auth B], this version write letter inside of squrare bracket

Description:
    
    In the input file, under every PDB ID, there are one or couple of chains. 
    In databese PDB, every PDB_ID has one or couple of entities. 
    This program is to find all entity that correspond to chains in input file. And then add Annotation.
    
    In PDB databse, the chain has many kinds of format, for example: "A[auth B]","A,B" and so on.
    For one line in input file, if it match with an entity both in chain and Uniprot ID, we will add the annotation of this entity in this line in output file
    
    We classify the format of chain into five cases
        A
        A,B,C
        A[auth B]
        A[auth B], C[auth D]
        A[auth B],C,D
    Specially, in case of format "A[auth B]", two letter correspond to one chain. 
    The data in SIFT use chain character inside the square bracket. So if the information in input file match with character inside the square bracket and its Uniprot ID, we will add this annotation in output file. 
    
    In the case of "A,B,C" and "A[auth B],C,D", if couple of chains and theirs Uniprot ID match with this entity, we will only leave the longest chain.
    
List of function:

Procedure:
    1, Read line one by one, add the lines with same PDB_ID in a list called "PDB_list".
    2, When the list "PDB_list" is full, searching PDB webpage to look at entities
    3, For every entity, we use BeautifulSoup to find the Annotation and Chain of this entity,
        and use API to find the Uniprot ID
    4, According to the format of "Chain", we have different process to check 
        whether the input file has corresopnd chain
        The principle framework is:
##############################################################
        if "[" in the chain:
            if len(chain_list)==square_bracket:
                if square_bracket==1:
                    B [auth P]
                else:
                    G [auth M],H [auth N],I [auth O]
            else:
                A,B,E [auth C],F [auth D]
        else:
            if len(chain_list)==1:
                A
            else:
                G, H
###############################################################
    5, If there is one element in "PDB_list" which can correspond with both Chain and Uniprot ID, we will write this line in output file adding Annotation
    6, After finishing final entity of this PDB_ID, empty variable "PDB_list" and start new PDB_ID.

Usage:
    command line:
    python 2022-09-27_Filtering.py sample_data_3.tsv sample_3_result.tsv

Special Note: In the case of "A [auth B]", This script will write "B" in output file.

"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import requests
# import copy
# import sys

whole=open("Debug_example.tsv",'r')
w=open("Debug_example_result.tsv",'w')


# whole=open(sys.argv[1],'r')
# w=open(sys.argv[2],'w')


w.write("PDB\tCHAIN\tANNOTATION\tRESOLUTION\tUniprot_ID\tLENGTH\tPDB_BEG\tPDB_END\n")

PDB_list=[]#this list contains all lines under one PDB_ID
PDB_ID=""# PDB_ID store pdb id

whole.readline()#skip first line

for line in whole:
    line=line.strip().split('\t')# transform string into list called "line"
    # print(line)#It looks like"['6t1r', 'N', 'P02489', '166', '9.8', '1', '166']"
    
    if line[0] == PDB_ID:#if this PDB_ID is equal to previous one, just adding a chain 
        PDB_list.append(line)# add this line into list "PDB_list" 
    elif PDB_ID=="":# The first line
        PDB_ID=line[0]
        # Resolution=line[4]
        PDB_list.append(line)# add this line into list "PBD" 
    else:#if the PDB_ID of this line is different from previous ID, That means last PDB_ID is full.
        #That means we can look at entity
        
        # print("PDB ID:",PDB_ID)
        # print("PDB list",PDB_list)
        
        #create list to contain all chian ID and Uniprot ID 
        letter_list=[]# This list is to contain all chain ID in this PDB
        Uniprot_list=[]# This list is to contain all Uniprot ID in this PDB
        
        for i in range (0,len(PDB_list)):# Fill the list, letter_list and Uniprot_list
            letter_list.append(PDB_list[i][1])# add every chain ID into list "letter_list""
            Uniprot_list.append(PDB_list[i][2])# add every Uniprot ID into list "Uniprot_list"

        #connecting the webpage and getting the the whole html page, called "soup"
        url="https://www.rcsb.org/structure/"+PDB_ID
        html = urlopen(url).read()
        soup = BeautifulSoup(html, features="html.parser")#regarding the whole webpage as "soup"
        
        ##locating entities
        
        #getting the amount of Entity ID, which determine the rounds in loop.Storing it in variable "amount"
        text = soup.get_text() # getting text in webpage
        result=re.findall("Entity ID:",text)
        # the number of "Entity ID:" is equal to the amount of entity molecule
        amount=len(result) #"amount" means the amount of entity ID
        # print("The number of entity:",amount)
        
        for i in range(1,amount+1):#go through every entity, looking at whether it match, and write in output file
            # print("Entity ID:",i)
            
            #locating the table of Entity_ID, one ID one table
            ID="table_macromolecule-protein-entityId-"+str(i)
            table=soup.find("table",id=ID)#extracting the content of table into a variable "table"
            if table ==[]: # maybe it is nucleid entity
                pass
            else:#this table is not empty, that means this entity has content
                #cruling data from website
                table=str(table)#transforming the content into string
                soup_2= BeautifulSoup(table, features="html.parser")#regarding the content of table as a new soup,"soup_2"
                tr=soup_2.find_all("tr")# "tr" means a line in the table, this is to find all line in this table
                if tr==[]:#if it doesn't has content
                    pass
                else:#it has content, we will find the data we want
                    #locating the annotation and chain using Beautiful Soup
                    #In the third <tr>, under this <tr>: the first <td> is annotation, the second <td> is chain
                    chain_line=str(tr[2])#the third <tr>
                    soup_3=BeautifulSoup(chain_line, features="html.parser")#regarding the content of chain_line as a new soup,"soup_3"
                    td=soup_3.find_all("td")#find all td in this line under tr
                    annotation=td[0].get_text()#first <td> is annotation
                    # print("annotation",annotation)
                    chain_box=td[1].get_text()# the second td is chain box, the content is like "C [auth D]"
                    # print(chain_box)
                    if "Less" in chain_box:#if there is "Less" inside chain box,just remove it
                        chain_box=chain_box.replace('Less', '')
                    chain_list=chain_box.split(',')#transfrom chain box(string) into chain list
                    chain_list=[x.strip() for x in chain_list]#remove all space near letter, letter is element of the list
                    #Finally, "annotation" and "chain_list".
                    
                    #locating the Uniprot Id, using API
                    response = requests.get("https://data.rcsb.org/rest/v1/core/polymer_entity/"+PDB_ID+"/"+str(i))
                    entity=response.json()['rcsb_polymer_entity_container_identifiers']#"entity" is a dictionary, and "uniprot_ids" is included in this dictionary
                    if "uniprot_ids" not in entity:#whther "uniprot_ids" exist in "entity"
                        pass#there is no Uniprot ID in this entity
                    else:#This entity has Uniprot ID. 
                        uniprot_ids=entity["uniprot_ids"]# "uniprot_ids" is a list, it includes all Uniprort ID, it could be one or two
                        
                        #Count the number of "[]" in chain box, storing it in variable "square_bracket"
                        i=0
                        for letter in chain_box:#"chain_box" is string, so this is checking letter one by one, look at whether they have "["
                            if letter=="[":
                                i+=1
                        square_bracket=i# the number of "[" is stored in square_bracket
                        # print(square_bracket)
                        if "[" in chain_box:#
                            if len(chain_list)==square_bracket:
                                if square_bracket==1:# That mean it is "A [auth B]"
# B [auth P]########################################################################################
                                    #extract the auth chain ID from "B [auth P]"
                                    print(PDB_ID)
                                    print(chain_box)
                                    square=list(re.findall(r"\[.*\]",chain_box))[0]#"square" is the string "[auth B]"
                                    letter=square[:-1][6::]# The characters of chain is stored in variable "letter"
                                    
                                    #extrtact the letter before "[auth B]"
                                    # front_letter={}
                                    square_index=chain_list[0].index("[")#"square_index" is index of "["
                                    # print(chain_list[0])
                                    front_letter=chain_list[0][:square_index].strip()#"front_letter" is the letter before "[auth B]"
                                    # print(front_letter)
                                    
                                    # print("letter",letter)
                                    #Double check, firstly check chain character, then check Uniprot ID
                                    if letter in letter_list:#This chain character is inside letter_list
                                        #getting index of this chain character, storing in variable "y"
                                        y=letter_list.index(letter)# the index of "letter" in list "letter_list"
                                        #Check Uniprot ID
                                        if PDB_list[y][2] in uniprot_ids:# looking at whether correspond Uniprot ID equal to the ID on website
                                            # if it is equal, we can write this sublist into file
                                            print("{}\t{}\t{}\t{}".format(PDB_list[y][0],annotation,str(letter),'\t'.join(PDB_list[y][2::])),file=w)
                                            pass
                                        else:# The Uniprot ID doesn't match btween website and file
                                            pass# skip this entity
                                    length_dic={}#empty this dictionary
                                    front_letter={}#empty dictionary
                                else:#There are more than two square bracket
#"G [auth M],H [auth N],I [auth O]"###################################################################################
                                    # print(PDB_ID)
                                    # print(chain_list)
                                    #Construct a list "inside" to collect all chain character inside square bracket
                                    inside=[]#"inside" stores all letters inside the square bracket
                                    # letter_checklist={}#"letter_checklist", key is letter inside square bracket, value is the letter outside the square bracket
                                    length_dic={}
                                    for element in chain_list:#check "chain_list" one by one
                                        square=list(re.findall(r"\[.*\]",element))[0]#"square" is string "[ auth A]"
                                        letter=square[:-1][6::]#"letter" is extract the chain characters
                                        inside.append(letter)#add chain character into list "inside"
                                        #extrtact the letter before "[auth B]"
                                        # square_index=element.index("[")#"square_index" is index of "["
                                        # front_letter=element[:square_index].strip()#"front_letter" is the letter before "[auth B]"
                                        # print(front_letter)
                                        # letter_checklist[letter]=front_letter#adding two letters into dictionary
                                        
                                    # print(inside)
                                    #Firstly, checking every letter in square bracket, whether the chain letter and Uniprot ID match information of this entity
                                    #Secondly, add letter that matches into dictionary and finally choose the longest one in output file
                                    #If all letter in square bracket don't match, we will scan all letter in "Letter_list", 
                                        #if anyone matches, adding into dictionary, and choose longest one into output file
                                    for x in inside:#
                                        if x in letter_list:#Firstly,check whether this letter is inside list "letter_list"
                                            if Uniprot_list[letter_list.index(x)] in uniprot_ids:#Double check, whether Uniprot ID is correct
                                                y=letter_list.index(x)#"y" is index of this letter in list "letter_list"
                                                length_dic[y]=PDB_list[y][3]#Adding letter in dictionary. key is index, value is length

                                    if len(length_dic)!=0:#if there is a letter matching with Uniprot id, find the longest one and write it in the output file
                                        # print("*",letter_checklist)
                                        print("*",length_dic)
                                        length=list(length_dic.values())#"length" is the list of value of dictionary,length
                                        length=[int(x) for x in length]
                                        index=list(length_dic.keys())#"index" is the list of key of dictionary,index
                                        y=index[length.index(max(length))]# "y" is the index of ID whose length is longest
                                        print(y)
                                        print("{}\t{}\t{}\t{}".format(PDB_list[y][0],annotation,PDB_list[y][1],'\t'.join(PDB_list[y][2::])),file=w)
                                        length_dic={}#empty the dictionary
                                    else:#all letters in square bracket don't match uniprot id
                                        pass
                                    length_dic={}#empty this dictionary
                                    # letter_checklist={}#empty this dictionary
                                    inside=[]
                            else:#
#A,B,E [auth C],F [auth D]###################################################################################################################
                                print(PDB_ID)
                                print(chain_list)
                                priority=[]#letters in "priority" are among all single letter, and letters inside square bracket.And they match both chain letter and Uniprot ID
                                # letter_checklist={}# "letter_checklist",for pattern "A[ auth B]":key is letter in square bracket, value is letter out of square bracket; in pattern single letter: key and value is the same.
                                for x in chain_list:# "x" can be divided into two pattern: one square bracket pattem, another is single letter it self
                                    if "[" in x:#This is to do with pattem look like G [auth M]
                                        square=list(re.findall(r"\[.*\]",x))[0]#"sqaure" is string "[auth A]"
                                        letter=square[:-1][6::]#"letter" is the letter itself in square bracket
                                        #extrtact the letter before "[auth B]"
                                        # square_index=x.index("[")#"square_index" is index of "["
                                        # front_letter=x[:square_index].strip()#"front_letter" is the letter before "[auth B]"
                                        # print(front_letter)
                                        # letter_checklist[letter]=front_letter#adding two letters into dictionary
                                        
                                        if letter in letter_list:#Firstly checking whether letter in letter_list
                                            if Uniprot_list[letter_list.index(letter)] in uniprot_ids:#Double checking whether it is equal to Uniprot in the webpage
                                                priority.append(letter)# if it matches, add into list "priority"
                                        else:#this letter is not in letter list
                                            pass
                                    else:#This is to do with pattem of single letter, 
                                        # letter_checklist[x.strip()]=x.strip()#adding letter into dictionary, key and value is the same
                                        if x in letter_list:#Firstly checking whether letter in letter_list
                                            if Uniprot_list[letter_list.index(x)] in uniprot_ids:#Double checking whether it is equal to Uniprot in the webpage
                                                priority.append(x)#if it matches, add in list "priority"
                                        else:# this letter not in letter list
                                            pass
                                #Check that whether "priority" is empty
                                if len(priority) !=0:#if list "priority" is not empty, adding them in dictionary and choose the longest one into dictionary
                                    for x in priority:#adding x into dictionary 
                                        y=letter_list.index(x)#"y" is the index of x
                                        length_dic[y]=PDB_list[y][3]
                                    #comparing the length 
                                    if len(length_dic)==1:# there is only one letter in this dictionary, write this into output file
                                        y=list(length_dic.keys())[0]#"y" is index, (there is only one element in the list)
                                        print("{}\t{}\t{}\t{}".format(PDB_list[y][0],annotation,PDB_list[y][1],'\t'.join(PDB_list[y][2::])),file=w)
                                    elif len(length_dic)==0:
                                        pass
                                    else:# There are more than one letter in dictionary.Find the logest one
                                        length=list(length_dic.values())#"length" is the list of value of dictionary,length
                                        index=list(length_dic.keys())#"index" is the list of key of dictionary,index
                                        y=index[length.index(max(length))]#"y" is the index of ID whose length is longest
                                        print("{}\t{}\t{}\t{}".format(PDB_list[y][0],annotation,PDB_list[y][1],'\t'.join(PDB_list[y][2::])),file=w)
                                        length_dic={}
                                    length_dic={}#empty this 
                                # letter_checklist={}# empty the dictionary
                                length_dic={}#empty this dictionary
                                priority=[]
                        else:
                            if len(chain_list)==1:
#"A"#########################################################################################################################
                                if chain_list[0] in letter_list:#Firstly checking whether letter in letter_list
                                    if Uniprot_list[letter_list.index(chain_list[0])] in uniprot_ids:#Double checking whether it is equal to Uniprot in the webpage
                                        y=letter_list.index(chain_list[0])#"y" is the index of this letter
                                        print("{}\t{}\t{}".format(PDB_list[y][0],annotation,'\t'.join(PDB_list[y][1::])),file=w)
                            else:
#"G, H"#########################################################################################################
                                priority=[]#letters in "priority" are among all single letter.And they match both chain letter and Uniprot ID
                                length_dic={}
                                for x in chain_list:# "x" can be divided into two pattern: one square bracket pattem, another is single letter it self
                                    if x in letter_list:#Firstly,check whether this letter is inside list "letter_list"
                                        if Uniprot_list[letter_list.index(x)] in uniprot_ids:#Double check, whether Uniprot ID is correct
                                            priority.append(x)# if it macthes,adding letter into list "priority"
                                if len(priority)!=0:#there is at least one letter in the list
                                    #comparing the length
                                    for x in priority:#adding the element in dictionary 
                                        # key is index, value is length
                                        y=letter_list.index(x)#the index of x is y
                                        length_dic[y]=PDB_list[y][3]
                                    
                                    if len(length_dic)==1:
                                        y=list(length_dic.keys())[0]#y is index, (there is only one element in the list)
                                        print("{}\t{}\t{}".format(PDB_list[y][0],annotation,'\t'.join(PDB_list[y][1::])),file=w)
                                    else:#finding more than one Uniprot IDs that match
                                        length=list(length_dic.values())#"length" is the list of value of dictionary,length
                                        index=list(length_dic.keys())#"index" is the list of key of dictionary,index
                                        y=index[length.index(max(length))]#"y" is the index of ID whose length is longest
                                        print("{}\t{}\t{}".format(PDB_list[y][0],annotation,'\t'.join(PDB_list[y][1::])),file=w)
                                        length_dic={}
                                length_dic={}#empty this dictionary
                                priority=[]
        PDB_list=[]
        PDB_ID=line[0]
        Resolution=line[4]
        PDB_list.append(line)# add this line into list "PBD" 
whole.close()
w.close()













