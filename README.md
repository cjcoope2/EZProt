# EZProt

EZProt is a command-line-interface application used to help speed up the process of data-mining in genomic and proteomic laboratories. 

EZProt must be saved into your downloads and then moved into a directory of your choosing. Please put this final directory in your path. 

EZProt requires a slew of applcations that must be downloaded with the correct versions. Here is the best order to download each in:
*Please ensure that each is properly downloaded and moved to usr/local/bin or usr/bin prior to using EZProt*
  ~python 2.7.14
  ~numpy & scipy
  ~biopython version 1.70
  ~Clustal Omega version 1.2.4
  ~MUSCLE version 3.8.31
  ~TCoffee version 11
  ~trimAl version 1.2
  ~RAxML version 8.00
  
Soon an installer for all of the above programs will be put in the Master branch.

To use EZProt, simply go into the directory with the software and type 'python EZProt'

From there, when asked for either a single or multiple files, write the entire path from /Users (use the command pwd prior to determine the path)
For fastest analysis, use MUSCLE. For best results, use either MUSCLE or TCoffee as well as trimAl. 
