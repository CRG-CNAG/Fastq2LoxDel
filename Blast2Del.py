#!/usr/bin/env python3

def process_blast(fil, evalue_thr=1e-3, aln_len_thr=20, identity_thr=90):
    """
    Parser of blast results satisfying the threshold conditions.
    Takes a blast file in format 6 and returns a dictionary:
        {identifier:[evalue, query start, query end, subject start, subject end]}
    """
    rs = {}
    discarded = {}
    with open(fil, 'r') as fi:
        for line in fi:
            line = line.strip().split()
            evalue = float(line[-2])
            if evalue<=evalue_thr and float(line[2])>=identity_thr and int(line[3])>=aln_len_thr:
                ide = ':'.join(line[0].split(':')[-2:])
                qstart, qend = sorted([int(i) for i in line[6:8]])
                sstart, send = sorted([int(i) for i in line[-4:-2]])
                minirs = [evalue, qstart, qend, sstart, send]
                if ide in rs:
                    rs[ide].append(minirs)
                else:
                    rs[ide] = [minirs]
    return rs

def filter_deletions(inFile, n=2,
                     evalue_thr=1e-3, aln_len_thr=20, identity_thr=90,
                     mapping_place_filter=1):
    """
    Extract deletions from a <inFile> blast format 6 file looking for pasted
    reads mapping to <n> different regions. For example, with <n> default 2:

    ------------deleted_region-----------------
          r1++++              r2++++

    Different filter conditions can be applied using the following thresholds:
        <evalue_thr>, <aln_len_thr> (alignment length), <identity_thr>

    <mapping_place_filter>: ensure the two gDNA are subsequent in the read.
        this can be a numerical value representing the number of bps allowed
        between the two positions.

    """
    blast_all = process_blast(inFile, evalue_thr=evalue_thr, aln_len_thr=aln_len_thr, identity_thr=identity_thr)
    comp_rs = {}
    rs = {}
    for k, v in blast_all.items():
        if len(v)==2:
            evalueA, qstartA, qendA, sstartA, sendA = v[0]
            evalueB, qstartB, qendB, sstartB, sendB = v[1]

            if abs(qendA-qstartB)==mapping_place_filter or abs(qendB-qstartA)==mapping_place_filter:
                print(k)
                st, en = sorted([sstartA, sendA, sstartB, sendB])[1:3]
                del_ide = str(bin_dictionary[st])+'..'+str(bin_dictionary[en])
                comp_rs[k] = [st, en, del_ide]
                if del_ide in rs:
                    rs[del_ide].append(k)
                else:
                    rs[del_ide] = [k]
    return comp_rs, rs

all_dels, filt_dels = filter_deletions('<file generated with LoxDel_paired or LoxDel_singe>')
