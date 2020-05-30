# Fastq2LoxDel

Scripts used to extract lox-derived deletions.

The example described here allows to reproduce the results observed in 'LoxTnSeq: Transposon mutagenesis coupled with ultra sequencing to study large random genome reductions' by Daniel Shaw *et al.* (to be published).

# Requirements

Python3, blast command line tool

# Example

1. Locate all fastq files in the same directory with the scripts from this repository.

2. Run [peFastq2LoxDel](peFastq2LoxDel.py) to generate the blast files from the raw paired-end fastq:
```{bash}
python3 peFastq2LoxDel.py
```
User can change the inverted repeat to detect, the genome and blast settings directly in that script. As alternative, [seFastq2LoxDel](seFastq2LoxDel.py) process the paired reads separatedly to detect inverted repeats and then pastes the sequences, allowing for extra coverage but also, in our experience, a lot of off-target signals.

3. Filter the blast file to take those reads covering a deletion point:

   **3.1**) Edit [Blast2LoxDel](Blast2LoxDel.py) with the file of interest to process and run:
```{bash}
python3 Blast2LoxDel.py
```

   **3.2**) Alternatively and preferred, this step is thought to be performed in a python environment importing the function *filter_deletions* from this script.
