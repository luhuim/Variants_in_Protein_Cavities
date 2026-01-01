#                 CICLOP
CICLOP (Characterization of Inner Cavity Lining of Proteins) aims to identify and characterize the pores/cavities/tunnels/channels found in proteins. The software is able to accurately map the residues that line the inside surface of these structural features of a given protein. CICLOP is completely automated with the only required input of the protein coordinates, in the form of a PDB file. The tool was tested on varying (both in structure and function) proteins and was able to achieve its objective in an efficient and accurate manner. Created in an attempt to provide some key insights into critical biological functions of these proteins, CICLOP was also bench tested with some of the leading softwares and methods trying to achieve a similar goal

##               Citation: 
If you use our tool, please read and cite the CICLOP publication:

CICLOP: A Robust, Faster, and Accurate Computational Framework for Protein Inner Cavity Detection  
**bioRxiv** : https://www.biorxiv.org/content/10.1101/2020.11.25.399246v1  

##      Authors:
CICLOP is written and maintained by Ray Lab at Indraprastha Institute of Information and Technology, New Delhi

##  Downloaded Files

      1. Extract the CICLOP folder
      2. Inside the CICLOP folder you would find the following:
                (a) build folder 
                (b) dist Folder
                (c) CICLOP.spec File
      3. Open the dist folder
      4. Inside the dist folder you would find the following:
                (a) Sample pdb file: 1j4n.pdb
                (b) Sample fasta file: rcsb_pdb_1j4n.FASTA
                (c) sample parameters file: ciclop_parameters.txt
                (d) CICLOP linux executable file (./CICLOP)      
          
## Python Prerequisites:

  - Python --version >= 3
      * **Python Packages:-** 
      * multiprocessing
      * threading
      * datetime
      * decimal
      * math
      * numpy
      * scipy
      * functools
      * operator
      * itertools
      * matplotlib
      * mpl_toolkits
      * zipfile

*Command: pip3 install <Package Name>*

##  Software Prerequisites:
- **DSSP** Secondary Structure Prediction Tool (as environment variable, system-wide installed)  
    -Link: https://swift.cmbi.umcn.nl/gv/dssp/ 
    -Command: sudo apt-get install dssp
- **zip** command line tool  
    -Command: sudo apt-get install zip
- **muscle** command line tool  
    -Command: sudo apt-get install -y muscle
- **rate4site** command line tool  
    -Command: sudo apt-get install -y rate4site
   
## Usage:
1. Write the parameters inside the ciclop_parameters.txt file. 
*The parameter values are case sensitive.*
*Walk through the parameters:*

    PDB_FILE_NAME: "Name of your PDB FILE.pdb"

    FASTA_FILE_NAME: "Name of your FASTA FILE.FASTA" or "None" in case of NO FASTA

    Alignment: Enter 1 for Automatic alignment and 0 for Manual Alignment*

    Cons_Score: Enter "YES" to calculate conservation score otherwise "NO"

    Rate_inf_method: Write "EB" for Empirical Bayesian or "ML" for Maximum Likelihood approach*

    E_Value: An integer from 1 to 10 as Evalue while searching for sequence homologues.

    Evo_Model: write "JTT" or "REV" or "DAY" or "WAG" or "LG" or "cpREV" or "JCamino" or "HKY" or "Tamura92"*

    Blast Method: write "p" for PSI-BLAST or "j" for jackhmmer

    Psiblast: Provide path for PSI-BLAST (Default: System-wide installed psiblast)

    Nr_db: Provide path for nr database for PSI-BLAST
    
    jackhmmer: Provide path for jackhmmer (Default: System-wide installed jackhmmer)
    
    Swisprot:  Provide path for Uniprot/Swissprot database (FASTA File)  
    
    psiblast_ncpu: Number of threads to provide to PSI-BLAST (Default: 4)
    
    jackhmmer_ncpu: Number of threads to provide to jackhmmer (Default: 4)
    
2. The pdb and the Fasta files should be in the same directory as the CICLOP executable file (CICLOP/dist/)
3. The ciclop_parameters.txt should also in the same directory and named as "ciclop_parameters.txt". (Case Sensitive)
4. Run through the command line: ./CICLOP    

**Note:**
  
**- FASTA identifiers in FASTA file should contain only the chain information**
    Example: >A,B,C,D or >A
  
**- NR database is only compatible with PSI-BLAST and Uniprot/Swissprot or any other datbase in FASTA format is compatible with jackhmmer**
  


##  Database:

- **NCBI** NR Protein Database

- **Uniprot-Swissprot** Database (FASTA File)  
Link: https://ftp.uniprot.org/pub/databases/uniprot/knowledgebase/uniprot_sprot.fasta.gz

- **PSI-BLAST** Tool Installed (with path to executable)  
Link: https://www.ebi.ac.uk/seqdb/confluence/display/THD/PSI-BLAST

- **jackhmmer** Tool Installed (with path to executable)  
Link: http://eddylab.org/software/hmmer/hmmer-3.3.2.tar.gz  
Command: sudo apt-get install -y hmmer
