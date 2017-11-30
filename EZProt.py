#! #!/usr/bin/env python
#Developed by Cullen J. Cooper

#import all needed modules
import os
import sys
import Bio
import time
import shutil
import Bio.Align
import Bio.Phylo
import subprocess
from time import sleep
import Bio.Align.Applications
import Bio.Phylo.Applications
from Bio.Align.Applications import ClustalOmegaCommandline
from Bio.Align.Applications import TCoffeeCommandline
from Bio.Align.Applications import MuscleCommandline
from Bio.Phylo.Applications import RaxmlCommandline

print("Welcome to EZProt v.1, a tool for data mining in the genomic sciences.")
amount = raw_input("Do you have a single file or an entire directory to analyze? (Please type 'file' or 'directory'): ")
amount.lower()
if amount == "file":
    in_file = raw_input("Fasta Filename (you may enter the path all the way up to the file itself): ")
    out_file = raw_input("What would you like to name your alignment?: ")
    program1 = raw_input("Which program would you like to use to create your alignment? (type either 'tcoffee', 'muscle', or 'clustalo'): ")
    program1 = program1.lower()
    if program1 == "clustalo" :
        clustalo_cline = ClustalOmegaCommandline(infile=in_file, outfile=out_file, verbose=True, auto=True)
        platform = raw_input("What platform are you using? (ex: mac32, mac64, win32, win64, etc.): ")
        child = subprocess.call(str(clustalo_cline), shell=(sys.platform!=platform))
    elif program1 == "tcoffee" :
        tcoffee_cline = TCoffeeCommandline(infile=in_file, output="fasta", outfile=out_file)
        platform = raw_input("What platform are you using? (ex: mac32, mac64, win32, win64, etc.): ")
        child = subprocess.call(str(tcoffee_cline), shell=(sys.platform!=platform))
    elif program1 == 'muscle' :
        muscle_cline = MuscleCommandline(input = in_file, out = out_file)
        platform = raw_input("What platform are you using? (ex: mac32, mac64, win32, win64, etc.): ")
        child = subprocess.call(str(muscle_cline), shell=(sys.platform!=platform))
    else:
        print("error: invalid input, terminating program")
        time.sleep(3)
        sys.exit()
    #user given the option of using trimAl
    trimal = raw_input("Would you like to optimize your alignment using trimAl version 1.2? (type either 'yes' or 'no'): ")
    if trimal == 'yes':
        out_file2 = raw_input("What would you like to name your optimized alignment?: ")
        subprocess.call(['trimal', '-in', out_file, '-out', out_file2])
        print("Alignment optimization complete")
    elif trimal == 'no':
        out_file2 = out_file
    else:
        print("error: invalid input, terminating program")
        time.sleep(3)
        sys.exit
    #RAxML software initialized here
    out_file3 = raw_input("What would you like to call your tree?: ")
    raxml_cline = RaxmlCommandline(sequences=out_file2, model="PROTCATWAG", name=out_file3+".nwk")
    child = subprocess.call(str(raxml_cline), shell=(sys.platform!=platform))
    print("Process complete. You can open your newick files using any generic phylogenetic tree editor")

elif amount == "directory" :
    userdir = raw_input("Please write the path to the directory you would like to iterate over: ")
    os.chdir(userdir)
    program1 = raw_input("Which program would you like to use to create your alignment? (type either 'tcoffee', 'muscle', or 'clustalo'): ")
    trimal = raw_input("Would you like to optimize your alignment using trimAl version 1.2? (type either 'yes' or 'no'): ")
    platform = raw_input("What platform are you using? (ex: mac32, mac64, win32, win64, etc.): ")
    print("Your directory will now be analyzed")
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    i = 0
    for f in files:
        if f.endswith(".fasta"):
            in_file = f
            out_file = f+"_aligned"
            out_file2 = f+"_optimized"
            program1 = program1.lower()

            print("initializing multiple sequence alignment")

            if program1 == "clustalo" :
                clustalo_cline = ClustalOmegaCommandline(infile=in_file, outfile=out_file, verbose=True, auto=True)
                child = subprocess.call(str(clustalo_cline), shell=(sys.platform!=platform))
            elif program1 == "tcoffee" :
                tcoffee_cline = TCoffeeCommandline(infile=in_file, output="fasta", outfile=out_file)
                child = subprocess.call(str(tcoffee_cline), shell=(sys.platform!=platform))
            elif program1 == 'muscle' :
                muscle_cline = MuscleCommandline(input = in_file, out = out_file)
                child = subprocess.call(str(muscle_cline), shell=(sys.platform!=platform))
            else:
                print("error: invalid input, terminating program")
                time.sleep(3)
                sys.exit()

            print("Multiple sequence alignment complete")

            if trimal == 'yes':
                print("Optimization in progress")
                subprocess.call(['trimal', '-in', out_file, '-out', out_file2])
                print("Alignment optimization complete")
            elif trimal == 'no':
                out_file2 = out_file
            else:
                print("error: invalid input, terminating program")
                time.sleep(3)
                sys.exit

            print("Beginning phylogenetic tree construction")
            raxml_cline = RaxmlCommandline(sequences=out_file2, model="PROTCATWAG", name=f+".nwk")
            child = subprocess.call(str(raxml_cline), shell=(sys.platform!=platform))
            i = i + 1
    print('Total number of files analyzed: ', i)

else:
    print("error: invalid selection, terminating program")
    time.sleep(5)
    sys.exit()
