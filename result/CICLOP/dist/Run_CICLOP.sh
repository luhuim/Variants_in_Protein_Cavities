#!/bin/bash                 
cat PDB_list.tsv |while read line; 
do wget https://files.rcsb.org/download/$line.pdb;                                          
   wget https://www.rcsb.org/fasta/entry/$line -O $line.fasta;                                                                              
   python Writing_Parameter.py $line ciclop_parameters.txt; #fill parameter file
   ./CICLOP; # the software "CLCLOP" must be run in dist/ folder
   done                                                                                                               
