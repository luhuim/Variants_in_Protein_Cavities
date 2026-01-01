#!/usr/bin/python3
"""
Title: Merge same Uniprot
Date: 2022 June 2rd
Author: Huimin Lu

Description:
    In the file "first_parse.tsv",under every PDB ID, it has couple of chians. 
    And under every chains, it could have one or more than one Uniprot ID.
    And among these sequences, every sequence (sub-chain) is one line in "first_parse.tsv" file.
    And every line also include start and end point in three database: "RES", "PDB", "SP".  
    We only want to leave the position information from "PDB".   
    Only keep the column "PDP"
    This script is to merge same Uniprot into one line, and sum up the length of sequences. 
    And write them in a new file.
    
    Attention:
    The unique point of this script is that the first line of output file is contained in a list, it will be wroten in output file with loop,
        not being wroten directly using t.write().

List of functions:
    None
List of "non standard modules":
    None
Procedure:
    The pattern of every line is "basic information"+ "position of every sub-chian"
    1, add the header of output file in the list "pre_line", in advance.
    2, when reading current lines in input file, transform string into list. "current_line".(remove the character in PDB position as well,e.g. 13A, change into 13 )
    3, There is loop of reading every line. If "current_line" is different from "pre_line", 
        it will write pre_line in file, and double check whether the "sum of length" is correct. 
    4, If the chain is different, write pre_line in file, double check the sum of lenght
    5, After the loop, write the last "pre_line" in the file. and check whether sum of length is correct
    
Usage:
    python merge_sub-chians.py [input file (PDB_originbal_list)] [output file (PDB_one_line_one_UniprotID)]
    In the command line, for example:
        python scr/merge_sub-chains.py result/collect_PDB/first_parse.tsv result/PDB_one_chain_one_line/merge_data_1.tsv  
    Note the console, if there string print on console, that means the calculation of length is in correct.
    
"""
#%%
# import re
# import sys

# #import the file
# r=open(sys.argv[1],'r')#input file
# t=open(sys.argv[2],'w')#output file

#%%
import re

#import the file
r=open("first_parse.tsv",'r')#input file
t=open("merge_data_1.tsv",'w')#output file

r.readline()#pass the first line of input file
pre_line=["PDB","CHAIN","Uniprot_ID","LENGTH","RESOLUTION","PDB_BEG","PDB_END"]# "preline" list contain elements of header in output file.

for line in r:
    current_line=line.strip().split('\t')#split current line into list
    # current_line[1]=current_line[1].upper()
    if len(current_line)!=11:#resolution value doesn't exist, it doesn't have "None".
        current_line.append("None")
    # current_line is the line that is reading in this loop
    # print("current_line",current_line)
    # Adjusting order
    position=current_line[5:7]# it is "PDB_BEG" and "PDB_END",extract them in "position"
    #first three columns 0,1,2, are basic information. and columns 9,10 are basic information as well
    #remove the all position, and rest columns are all basic information 
    del current_line [3:9]#these are RES_BEG,RES_END,PDB_BEG,PDB_END,SP_BEG,SP_END
    current_line = current_line + position #Here we add PDB position of this sun-chain
    # print("---",current_line)
    position=[]# clean this temparary list
    #Removing letter in PDB position
    # print("current_line",current_line)
    current_line[5]=re.sub(r'[A-Z]',"",current_line[5])#remove the letter in "PDB_BEG",and using new value to replace old value
    current_line[6]=re.sub(r'[A-Z]',"",current_line[6])#remove the letter in "PDB_END",and using new value to replace old value
#    print(current_line)
    if current_line == ['']:# When it read empty lines in input file, it might happen if the program read an empyt line in the last.
        break
    elif current_line[0]== pre_line[0]:#Same PDB. index[0] is PDB ID, if equal, that means same PDB ID
        # print("same PDB")
        if current_line[1]== pre_line[1]:#Same chain. index [1] is chain character, if equal, that means same PDB ID, same chain
            # print("same Chain")
            if current_line[2]== pre_line[2]:#Same Uniprot ID
                # print("same Uniprot")
                #sum up the length
                pre_len=int(pre_line[3]) #the length in "pre_line"
                new_len=int(current_line[3]) #the length in "current_line"
                sum_len=pre_len + new_len
                pre_line[3] =str(sum_len)#changing the value in "pre_line"
                sum_len=0
                #Add PDB position in "pre_line"
                position=current_line[5:7]#extract PDB from current_line, store it in "position"
                pre_line=pre_line+position #add "position" at the end of "pre_line"
                position=[]
            else:# this is another Uniprot ID
                # print("different Uniprot")
                # doble check length, write "pre_line" in the file, re
                #double checking the calclulation of length
                coordinate=pre_line[5:]#all position, storing them in list "coordinate"
                total_len=pre_line[3]#"tatal_len" is sum of length in the list
                i=0
                total=0
                while i<len(coordinate):
                    BEG=int(coordinate[i])
                    END=int(coordinate[i+1])
                    total=(END-BEG+1)+total#sum up length
                    i+=2                
                if str(total) != total_len:# if the length calculated with two method are different, we will print it out
                    print("not equal",pre_line[0],pre_line[1])
                    print(pre_line)
                    print("in the list",total_len)
                    print("second calculating",total)
                # write "pre_line" in the file
                result='\t'.join(pre_line)# transforming list into string, called "result"  
                print("{}".format(result),file=t)# write "pre_line" into file 
                #replace "pre_line" with "current_line", start a new round
                pre_line=current_line
                
        else:#different chain
            # print("different chain")
            # doble check length, write "pre_line" in the file, re
            #double checking the calclulation of length
            coordinate=pre_line[5:]#all position, storing them in list "coordinate"
            total_len=pre_line[3]#"tatal_len" is sum of length in the list
            i=0
            total=0
            while i<len(coordinate):
                BEG=int(coordinate[i])
                END=int(coordinate[i+1])
                total=(END-BEG+1)+total#sum up length
                i+=2                
            if str(total) != total_len:# if the length calculated with two method are different, we will print it out
                print("not equal",pre_line[0],pre_line[1])
                print(pre_line)
                print("in the list",total_len)
                print("second calculating",total)
            # write "pre_line" in the file
            result='\t'.join(pre_line)# transforming list into string, called "result"  
            print("{}".format(result),file=t)# write "pre_line" into file 
            #replace "pre_line" with "current_line", start a new round
            pre_line=current_line
            
    else:#different PDB
        # print("different PDB")
        #the process is similar to the procedure different chians above, but there are some different
        #checking calclulation
        if pre_line[5]=="PDB_BEG":#This is only used in first line
            result='\t'.join(pre_line)# transforming list into string, called "result"
            print("{}".format(result),file=t)# write "pre_line" into file 
            pre_line=current_line
        else:# this only is only used after first line, only used in double check
            #double checking the calclulation of length
            coordinate=pre_line[5:]#all position, storing them in list "coordinate"
            total_len=pre_line[3]#"tatal_len" is sum of length in the list
            i=0
            total=0
            while i<len(coordinate):
                BEG=int(coordinate[i])
                END=int(coordinate[i+1])
                total=(END-BEG+1)+total
                i+=2                
            if str(total) != total_len:#comparing "total_len" and "total", one is in "pre_line", the other is to check
                print("not equal",pre_line[0],pre_line[1])
                print(pre_line)
                print("in the list",total_len)
                print("second calculating",total)
            #write pre_line in the file
            result='\t'.join(pre_line)# transforming list into string, called "result"  
            print("{}".format(result),file=t)# write "pre_line" into file 
            #replace
            pre_line=current_line
#write last "pre_line" in file
result='\t'.join(pre_line)# transforming list into string, called "result"  
print("{}".format(result),file=t)# write "pre_line" into file 

r.close()
t.close()

        
            