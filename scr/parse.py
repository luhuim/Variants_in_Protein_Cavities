#!/usr/bin/python3

"""
Title: Parse pdb ID and its resolution value
Data: 2022 May 13
Author: Huimin Lu

Description:
    In the file "All species train.csv", it only contain the Uniprot ID of all species, but don't have pbd ID. 
    And in the file "uniprot_segments_observed.csv", it include all pbd ID.
    This program is to parse pbd information of "All species". And at the same time, getting their resolution value and length of seqeunce.
    
List of function:
    
List of "non-standard module":
    bs4 (to install package, type "sudo apt-get install python3-bs4" in commnad line)
    requests
    
Procedure:
    1. Store the Uniprot ID of all species in a list
    2. Reading each line in file "Uniprot Segment", if the Uniprot ID in this line exist in the list (above) as well, we will continue
    3. Calculate the length of each sequence: "RES_END"-"RES_BEG"+1
    4. Getting the pbd ID and getting its resolution value, using API: 
        if the pbd ID has been replaced by others, searching the present ID and continue.
        if the pbd ID doesn't have resolution value, write into output file
        if the pbd ID has resolution value, write into file
Usage: 
    Installing the package at first: type "sudo apt-get install python3-bs4" in commnad line
    And then match the input file name with right variable, in the script: all species-->selection, uniport_segment-->whole
    python parse.py [PDB list] [variant list] [output file]
    for example:
    	Runing it in home directory of this project
        python scr/parse.py data/uniprot_segments_observed.tsv scr/All_species_train.csv collect_PDB/first_parse.tsv

"""

import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import requests

link="https://www.ebi.ac.uk/pdbe/api/pdb/entry/experiment/" #this is the front part of URL

#open the file we want to read
whole=open(sys.argv[1],'r')
selection=open(sys.argv[2],'r')
#open the file we want to output
t=open(sys.argv[3],'w')

t.write('PDB\tCHAIN\tSP_PRIMARY\tRES_BEG\tRES_END\tPDB_BEG\tPDB_END\tSP_BEG\tSP_END\tLENGTH\tRESOLUTION\n')#writing the header of output file
#collect 
selection.readline()
ID_Collection=[]#this list is to collect protein ID 
for line in selection:
    content=line.split(',')#split line (string) into a list, called content
    ID=content[2].strip()# the third element is the protein ID we want to collect, extract this element into variable called "ID"
    ID_Collection.append(ID)
#print(ID_Collection)
ID_Collection=set(ID_Collection)# there might be overlapped IDs. Sorting the list can save the some storage.
#print(len(ID_Collection))# the number of Uniprot IDs is 11891, in the "all species" file. 
whole.readline()
whole.readline()
for line in whole:
#    print(line)
    content_2=line.split('\t')#split line (string) into a list, called content_2
#    print(content_2)
    if content_2[2].strip() in ID_Collection:#if the id in the list 
#        print("in")
        result="\t".join(content_2) # this is the first part of result we want to write into output file.
        #calculating the length of each sequence
        a=int(re.sub(r'[A-Z]',"",content_2[6].strip()))#remove the letter in "PDB_BEG"
        b=int(re.sub(r'[A-Z]',"",content_2[5].strip()))#remove the letter in "PDB_END"
#        a=int(content_2[4].strip())# This is the position of "RES_END"
#        b=int(content_2[3].strip())# This is the position of "RES_BEG"
        length=a-b+1# variable "length" is the length of amino acid sequence
#        print("length",length)
        #getting resolution value
        id=content_2[0].strip()# the first element in the list is the ID of PBD
#        print("url",link+id) 
        response = requests.get(url=link+id)# request all data about this PDB ID, throuhgh API
        if response.status_code != 404:#if request of API is sucessful
            data=response.json()#getting actual data, all information, store those information into variable "data"
            #Firstly, checking whether there is "resolution" value
            upper_list=data[id][0] # the "upper_list" is the upper lever of "resolution"
            if "resolution" in upper_list:#checking whether there is "resolution" value
    #            print("it has resolution")
                resolution=data[id][0]['resolution'] #getting resolution value
    #            print("response",response)
    #            print("resolution",resolution)
            #write them into file, at the same time calculate the length of sequence           
    #            print("result",result)
#                print("{}\t{}\t{}\n".format(result.strip(),length,resolution))
                t.write("{}\t{}\t{}\n".format(result.strip(),length,resolution)) # The output is result+length+resolution
            else:
    #            print("{}\t{}\n".format(result,length))
                t.write("{}\t{}\t{}\n".format(result.strip(),length,"None"))
            upper_list=""
        else:# if there is ID that has been replace by other newer ID
            link2 = "https://www.rcsb.org/structure/removed/"+id#is link is to switch the out-of-date ID into newer one
            html = urlopen(link2).read()
            soup = BeautifulSoup(html, features="html.parser")
            
            for script in soup(["script", "style"]):
                script.extract()  
            text = soup.get_text()
            
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)# the text is content of web page "link2"
            
            ID_sentence=re.findall(r'superseded.{9}',text)#find the sentense "ID_sentence" that incluse newer ID
        #            print(text)
            id_2=ID_sentence[0][-4:]#extract newer ID from the sentense, storing it in variable "id_2" 
            id_2=id_2.lower()#the API only identify lower case
            response = requests.get(url=link+id_2)#searching the newer id one more time
            data=response.json()#getting actual data, all information, store those information into variable "data"
            #Firstly, checking whether there is "resolution" value
            upper_list=data[id_2][0] # the "upper_list" is the upper lever of "resolution"
            if "resolution" in upper_list:
    #            print("it has resolution")
                resolution=data[id_2][0]['resolution'] #getting resolution value
    #            print("response",response)
    #            print("resolution",resolution)
            #write them into file, at the same time calculate the length of sequence           
    #            print("result",result)
    #            print("{}\t{}\t{}\n".format(result,length,resolution))
                t.write("{}\t{}\t{}\n".format(result.strip(),length,resolution)) # The output is result+length+resolution
            else:
    #            print("{}\t{}\n".format(result,length))
                t.write("{}\t{}\t{}\n".format(result.strip(),length,"None"))
            upper_list=""
            
            
    content_2=[]

    

whole.close()
selection.close()
t.close()

