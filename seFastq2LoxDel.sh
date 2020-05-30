#!/bin/sh

# 1. Extract sequence and identifier
# 2. 2 pipes Filter out reverse lectures of the scar and remove --s
# 3. Filter scar-IR (left side)
# 4. Filter IR-scar (right side) --> if both --> keep only the inner region
# 5. awk to clean empty fasta sequences
# Send to blast

echo "filtering R1"
grep -B1 'GATAAAGTCCGTA\|TACGGACTTTATC' P1_read1.fastq | grep -v 'GATAAAGTCCGTA.*TACGGACTTTATC' |  grep -v '\-\-' | sed 's/@/>/g' | sed 's/.*TACGGACTTTATC//g' | sed 's/GATAAAGTCCGTA.*//g'| awk 'BEGIN {RS = ">" ; FS = "\n" ; ORS = ""} {if ($2) print ">"$0}' > P1_onlyread1.query
echo "filtering R2"
grep -B1 'GATAAAGTCCGTA\|TACGGACTTTATC' P1_read2.fastq | grep -v 'GATAAAGTCCGTA.*TACGGACTTTATC' |  grep -v '\-\-' | sed 's/@/>/g' | sed 's/.*TACGGACTTTATC//g' | sed 's/GATAAAGTCCGTA.*//g'| awk 'BEGIN {RS = ">" ; FS = "\n" ; ORS = ""} {if ($2) print ">"$0}' > P1_onlyread2.query

# genitalium genome = "/users/lserrano/smiravet/random_deletions_circularized/mgenitalium.fa"
# pneumoniae genome = "/users/lserrano/smiravet/random_deletions_circularized/NC_000912.fna"

# run blast
echo "about to run blast for R1"
blastn -db /users/lserrano/smiravet/random_deletions_circularized/NC_000912.fna -query P1_onlyread1.query -out /users/lserrano/smiravet/random_deletions_circularized/P1_onlyread1.blast -outfmt 6
echo "about to run blast for R2"
blastn -db /users/lserrano/smiravet/random_deletions_circularized/NC_000912.fna -query P1_onlyread2.query -out /users/lserrano/smiravet/random_deletions_circularized/P1_onlyread2.blast -outfmt 6
echo "Finished to run blast"
