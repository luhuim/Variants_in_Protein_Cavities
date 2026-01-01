#!/usr/bin/python3
"""
Title: Writing Parameter file
Date: 2022 October 27th
Author: Huimin Lu

Description:
    This program is to write the paramiter file in every PDB id.
    require a list of pdb id
    
    
List of function:
    
Procedure:
    1. Open the list of PDB id 

Usage: 
    type code below in the command line:
    python Writing_Parameter.py sample_1.tsv ciclop_parameters.txt
    
"""

import sys

PDB_list=open(sys.argv[1],'r')
w=open(sys.argv[2],'w')

for line in PDB_list:
    print("PDB_File_Name: ",line.strip(),".pdb",file=w)
    print("FASTA_FILE_NAME: ",line.strip(),".fasta",file=w)
    print("Alignment: 1 \nCons_score: YES\nRate_inf_method: EB\nEvo_model: JCamino\nE_value: 10",file=w)
    print("Blast_method: j",file=w)
    print("nr_db: /home/inf-31-2021/Research_Project/Fourth/CICLOP/dist/nr",file=w)
    print("swissprot: /home/inf-31-2021/Research_Project/Fourth/CICLOP/dist/uniprot_sprot.fasta",file=w)
    print("psiblast: /home/inf-31-2021/Research_Project/Fourth/CICLOP/dist/ncbi-blast-2.13.0+/bin/psiblast",file=w)
    print("jackhmmer: /home/inf-31-2021/Research_Project/Fourth/CICLOP/dist/hmmer-3.3.2/makeTAGS.sh\n",file=w)
