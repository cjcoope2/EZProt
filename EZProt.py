#!/usr/bin/env python

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

#define functions to app more white-space to the text interface
def newLine():
    print("")
def twoLines():
    newLine()
    newLine()

#Command-line initialization of the program
os.system('clear')

twoLines()

print("Welcome to EZProt version 1.2, a tool for rapid data interpretation in the genomic sciences.")

twoLines()

print("We recommend that you cd to the directory containing the subdirectory full of fasta files prior to running EZProt; enter 'ctrl+Z' to revert back to the CLI.")

twoLines()

print("The path to your current directory is: ")
path = subprocess.check_output('pwd')
print(path)

twoLines()

print("The following subdirectories are included inside of your current working directory: ")
from glob import glob
print(glob("./*/"))

twoLines()

#user selects the subdirectory they would like for the program to analyze, os.chdir cds into that subdirectory
userdir = raw_input("Please write the path to the directory you would like to have analyzed: ")
os.chdir(userdir)
twoLines()
#user selects MSA software
program1 = raw_input("Which program would you like to use to create your alignment? (type either 'tcoffee', 'muscle', or 'clustalo'): ")
program1 = program1.lower()
twoLines()
#user either includes or excludes trimal
trimal = raw_input("Would you like to optimize your alignment using trimAl version 1.2? (type either 'yes' or 'no'): ")
trimal = trimal.lower()
twoLines()
#platform variable is used in all subprocess calls throughout the program
platform = raw_input("What platform are you using? (ex: mac32, mac64, win32, win64, etc.): ")
twoLines()


print("Your subdirectory will now be analyzed")
#initializes a files variable that takes count of all files in the denoted directory
files = [f for f in os.listdir('.') if os.path.isfile(f)]
i = 0
for f in files:
    if f.endswith(".fasta"):
        in_file = f
        out_file = f+"_aligned"
        out_file2 = f+"_optimized"

        print("initializing multiple sequence alignment")

        #code block executes the preselected MSA
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

        #code block executes or skips trimal
        if trimal == 'yes':
            print("Optimization in progress")
            subprocess.call(['trimal', '-in', out_file, '-out', out_file2])
            print("Alignment optimization complete")
        elif trimal == 'no':
            out_file2 = out_file
        else:
            print("error: invalid input, terminating program")
            time.sleep(3)
            sys.exit()

        print("Beginning phylogenetic tree construction")

        #code block executes RAxML tree construction
        raxml_cline = RaxmlCommandline(sequences=out_file2, model="PROTCATWAG", name=f+".nwk")
        child = subprocess.call(str(raxml_cline), shell=(sys.platform!=platform))

        #i variable is used to count the number of files that are iterated over
        i = i + 1
twoLines()
print("Total number of files analyzed: "+str(i))
twoLines()

#sys.exit() is not used, this way commands and selections can be copied and pasted for documentation
