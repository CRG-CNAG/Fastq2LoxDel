#!/usr/bin/env python3

import glob
import sys, os

# detect files
for fil in glob.glob('*_read1.fastq'):
    r1 = fil
    r2 = fil.replace('read1', 'read2')

    basename1 = r1.split('.')[0]
    basename2 = r2.split('.')[0]
    print("running "+basename1+" "+basename2)

    if 'G1' in basename1:
        genome = "./genomes/mgenitalium.fa"
    else:
        genome = "./genomes/mpneumoniae.fa"

    # filter by motif and create fasta
    cmd = "grep -B1 'GATA[ACGT]\{18\}AAAAGGG\|CGCTTTT[ACGT]\{18\}TATC' "+r1+" | sed 's/@/>/g' | grep -v '\-\-' > "+basename1+".fa"
    os.system(cmd)
    cmd = "grep -B1 'GATA[ACGT]\{18\}AAAAGGG\|CGCTTTT[ACGT]\{18\}TATC' "+r2+" | sed 's/@/>/g' | grep -v '\-\-' > "+basename2+".fa"
    os.system(cmd)
    print("motifs filtered")

    # merge and filter by double motif
    cmd = "paste -d X "+basename1+".fa "+basename2+".fa | grep -B1 'GATA[ACGT]\{18\}AAAAGGG.*CGCTTTT[ACGT]\{18\}TATC' | grep -v '\-\-' > "+basename1.replace('_read1', '')+".filtmerge"
    os.system(cmd)
    print("double motifs filtered")

    # remove the motif
    cmd = "sed 's/GATA[ACGT]\{18\}AAAAGGG.*CGCTTTT[ACGT]\{18\}TATC//g' "+basename1.replace('_read1', '')+".filtmerge > "+basename1.replace('_read1', '')+".query"
    os.system(cmd)
    print("double motifs removed")

    # run blast
    print("about to run blast")
    cmd = "blastn -db "+genome+" -query "+basename1.replace('_read1', '')+".query -out "+basename1.replace('_read1', '')+".blast -outfmt 6"
    os.system(cmd)

    print(basename1+" finished")
