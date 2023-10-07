#!/usr/bin/env python3
# intersection_of_gene_names.py

"""
This program will find all gene symbols that appear both in the first infile and the second infile.

Sample command for executing the program:

$ python3 intersection_of_gene_names.py -i1 test_data/chr21_genes.txt -i2 test_data/HUGO_genes.txt

"""
import argparse
import sys
from get_file.io_utils import get_filehandle


def main():
    """ Business Logic """
    # get the file name
    args = get_file_args()
    filename1 = args.file1
    filename2 = args.file2
    outfile = "OUTPUT/intersection_output.txt"

    # open/write the file
    fh1 = get_filehandle(filename1, "r")
    fh2 = get_filehandle(filename2, "r")
    fh_out = get_filehandle(file=outfile, mode="w")

    # get two sets that contains all kind of genes' numbers and names from two files
    fh1_name_set, fh1_gene_num = get_fh_name_num(fh1)
    fh2_name_set, fh2_gene_num = get_fh_name_num(fh2)

    # find how many common genes they have and the names of common genes
    common_set, common_num = get_common(fh1_name_set, fh2_name_set)

    # sort the names of common genes in alphabetical order
    common_list = list(common_set)
    common_list.sort()

    # write the results into outfile and STDOUT
    fh_out.write(f"Number of unique gene names in chr21_genes.txt: {fh1_gene_num}\n" +
                 f"Number of unique gene names in HUGO_genes.txt: {fh2_gene_num}\n" +
                 f"Number of common gene symbols found: {common_num}\n" +
                 f"Output stored in OUTPUT/intersection_output.txt")
    for common_gene in common_list:
        sys.stdout.write(f"{common_gene}\n")


def get_file_args():
    """
    Just get the command line options using argparse
    @return: Instance of argparse arguments
    """

    parser = argparse.ArgumentParser(
        description='Open chr21_genes.txt, and ask user for a gene name')

    parser.add_argument('-i1', '--file1',
                        dest='file1',
                        type=str,
                        help='Gene list 1 to open',
                        required=True)
    parser.add_argument('-i2', '--file2',
                        dest='file2',
                        type=str,
                        help='Gene list 2 to open',
                        required=True)

    return parser.parse_args()


def get_fh_name_num(fh_in):
    '''
    get the set that contains all kind of genes names
    and the numbers of different genes it has totally
    @param fh_in: the file including the names of genes
    @return name_fh_set: the set that contains all kind of genes names
    @return num_fh: the numbers of different genes it has totally
    '''
    name_fh = []
    fh_in.readline()
    for line in fh_in:
        line = line.rstrip()
        line_list = line.split('	')
        name_fh.append(line_list[0])
    name_fh_set = set(name_fh)
    num_fh = len(name_fh)

    return name_fh_set, num_fh


def get_common(fh1, fh2):
    '''
    get the value of how many common genes the two files have
    and the set of names of common genes
    @param fh1: the set includes all different gene names from the first file
    @param fh2: the set includes all different gene names from the second file
    @return common: the set of names of common genes
    @return num_common: the value of how many common genes the two files have
    '''
    common = fh1.intersection(fh2)
    num_common = len(common)
    return common, num_common


if __name__ == '__main__':
    main()
