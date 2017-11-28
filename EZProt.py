#! usr/bin/env python

#import all needed modules
import os
import sys
import Bio
import time
import shutil
import Bio.Align
import Bio.Phylo
import Bio.Blast
import subprocess
from time import sleep
from Bio import SeqIO
import Bio.Align.Applications
import Bio.Phylo.Applications
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from Bio.Align.Applications import ClustalOmegaCommandline
from Bio.Align.Applications import TCoffeeCommandline
from Bio.Align.Applications import MuscleCommandline
from Bio.Phylo.Applications import RaxmlCommandline

#allow the user to choose which program they'd like to use
master = raw_input("Which program would you like to use? (Type either homologfinder or align2phylo): ")
master = master.lower()

#if the user selects it. this code block executes the homologysearch program
if master == "homologfinder" :
    fasta = raw_input("Fasta Filename:")
    my_query = SeqIO.read(fasta, format="fasta")
    proceed = raw_input("BLAST searches take anywhere from 1-10 minutes; do you wish to proceed? (please type 'yes' or 'no')")
    if proceed == "yes":
        print("Thank you for using homologfinder; BLAST searches average between 1-10 minutes dependent on the length of your sequence.")
        result_handle = NCBIWWW.qblast("blastp", "nr", my_query.seq)
        blast_record = NCBIXML.read(result_handle)
        exit_filename = raw_input("What would you like your output file to be named?")
        E_VALUE_THRESH = 0.000001
        out = open(exit_filename, "w")
        for alignment in blast_record.alignments:
            for hsp in alignment.hsps:
                if hsp.expect < E_VALUE_THRESH:
                    print >> out, '****Alignment****'
                    print >> out, '>', 'sequence:', alignment.title
                    print >> out, 'length:', alignment.length
                    print >> out, 'e value:', hsp.expect
                    print >> out, hsp.query[0:75] + '...'
                    print >> out, hsp.match[0:75] + '...'
                    print >> out, hsp.sbjct[0:75] + '...'
        out.close()
    elif Proceed == "no":
        print("Terminating program now")
        time.sleep(3)
        sys.exit()
    else:
        print("error: invalid input, terminating program")
        time.sleep(3)
        sys.exit()

#if the user selects it, this code block executes the align2phylo program
elif master == "align2phylo" :
    #MSA software initialized here
    in_file = raw_input("Fasta Filename:")
    out_file = raw_input("What would you like to name your alignment? ")
    program1 = raw_input("Which program would you like to use to create your alignment? (type either 'tcoffee', 'muscle', or 'clustalo')")
    program1 = program1.lower()
    if program1 == "clustalo" :
        clustalo_cline = ClustalOmegaCommandline(infile=in_file, outfile=out_file, verbose=True, auto=True)
        platform = raw_input("What platform are you using? (ex: mac32, mac64, win32, win64, etc.)")
        child = subprocess.call(str(clustalo_cline), shell=(sys.platform!=platform))
    elif program1 == "tcoffee" :
        tcoffee_cline = TCoffeeCommandline(infile=in_file, output="fasta", outfile=out_file)
        platform = raw_input("What platform are you using? (ex: mac32, mac64, win32, win64, etc.)")
        child = subprocess.call(str(tcoffee_cline), shell=(sys.platform!=platform))
    elif program1 == 'muscle' :
        muscle_cline = MuscleCommandline(input = in_file, out = out_file)
        platform = raw_input("What platform are you using? (ex: mac32, mac64, win32, win64, etc.)")
        child = subprocess.call(str(muscle_cline), shell=(sys.platform!=platform))
    else:
        print("error: invalid input, terminating program")
        time.sleep(3)
        sys.exit()
    #user given the option of using trimAl
    trimal = raw_input("Would you like to optimize your alignment using trimAl version 1.2? (type either 'yes' or 'no')")
    if trimal == 'yes':
        out_file2 = raw_input("What would you like to name your optimized alignment?")
        subprocess.call(['trimal', '-in', out_file, '-out', out_file2])
        print("Alignment optimization complete")
    elif trimal == 'no':
        out_file2 = out_file
    else:
        print("error: invalid input, terminating program")
        time.sleep(3)
        sys.exit
    #RAxML software initialized here 
    out_file3 = raw_input("What would you like to call your tree? ")
    raxml_cline = RaxmlCommandline(sequences=out_file2, model="PROTCATWAG", name=out_file3+".nwk")
    child = subprocess.call(str(raxml_cline), shell=(sys.platform!=platform))
    print("Process complete. You can open your newick files using any generic phylogenetic tree editor")

else:
    print("error: invalid selection, terminating program")
    time.sleep(5)
    sys.exit()
