#!/usr/bin/env python

from random import randint, seed
from bx.intervals.intersection import IntervalTree
import pybedtools
import sys
import os

def parse_snp_line(line):
    """
    Parses a single line of the SNP file

    Parameters
    ----------
    line : str
        The line from a SNP file

    Returns
    -------
    chrom : str
        The chromosome location of the SNP in the form of 'chr1'
    bp : int
        The bp location of the SNP
    
    """

    data = line.split()
    rsid = data[0]
    chrom = data[1]
    if chrom.find('chr') < 0:
        chrom = 'chr' + chrom
    bp = int(data[2])
    return rsid, chrom, bp


def listdir_absolute(d):
    return [os.path.join(d, f) for f in os.listdir(d)]


def list_to_boolean_string(inlist, length):
    result = ['0'] * length
    for el in inlist:
        result[el] = '1'
    return '\t'.join(result)

def find_snp_intersections(annot_dir, snp_file_loc, result_file_loc):
    """
    Create a dictionary of intervals where

    interval_trees[chromosome] = interval tree

    and checks against the snp file
    """

    interval_trees = {}
    chroms = range(1, 23) + ['X', 'Y']
    for chrom in chroms:
        interval_trees['chr' + str(chrom)] = IntervalTree()

    isbed = lambda x: os.path.split(x)[1].find('.bed') >= 0
    bed_files = filter(isbed, listdir_absolute(annot_dir))
    n_bed_files = len(bed_files)
    for fi, f in enumerate(bed_files):
        annotation = pybedtools.BedTool(f)
        for line in annotation:
            interval_trees[line.chrom].insert(line.start, line.stop, fi)

    snp_file = open(snp_file_loc)
    snp_lines = snp_file.readlines()
    snp_file.close()

    results = open(result_file_loc, 'w')

    for snp_line in snp_lines[1:]:  # skipping because it is assumed there is a header
        snp_rsid, snp_chrom, snp_bp = parse_snp_line(snp_line)
        overlap = interval_trees[snp_chrom].find(snp_bp - 1 , snp_bp + 1)
        print overlap
        results.write('{}\t{}\t{}\t{}\n'.format(snp_rsid, snp_chrom, snp_bp, list_to_boolean_string(overlap, n_bed_files)))

    results.close()

if __name__ == '__main__':
    try:
        annot_dir, snp_file_loc, result_file_loc = sys.argv[1:4]
    except:
        print('Need to provide location of annotation file, snp file, result file')

    find_snp_intersections(annot_dir, snp_file_loc, result_file_loc)