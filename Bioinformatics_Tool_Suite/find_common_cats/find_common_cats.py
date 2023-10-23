#!/usr/bin/env python3
# find_common_cats.py

"""
This program will count how many genes are in each category based on data from the input file.

Sample command for executing the program:

$ python3 find_common_cats.py -i1 chr21_genes.txt -i2 chr21_genes_categories.txt
"""
import collections
import argparse
from get_file.io_utils import get_filehandle


def main():
    """ Business Logic """
    # get the file name
    args = get_file_args()
    filename1 = args.infile1
    filename2 = args.infile2
    outfile = "OUTPUT/categories.txt"

    # open/write the file
    fh1 = get_filehandle(filename1, "r")
    fh2 = get_filehandle(filename2, "r")
    fh_out = get_filehandle(file=outfile, mode="w")

    # get the dictionary that maps the gene numbers and categories
    counts = get_cat_num(fh1)
    # get the dictionary that maps the gene descriptions and categories
    cat_des_dic = get_cat_des_dict(fh2)

    # write the results into outfile
    fh_out.write("Category	Occurrence	Description\n")
    for gene_cat, gene_occur in counts.items():
        fh_out.write(f"{gene_cat}  {gene_occur} {cat_des_dic[gene_cat]}\n")


def get_file_args():
    """
    Just get the command line options using argparse
    @return: Instance of argparse arguments
    """

    parser = argparse.ArgumentParser(
        description='Open chr21_genes.txt, and ask user for a gene name')

    parser.add_argument('-i1', '--infile1',
                        dest='infile1',
                        type=str,
                        help='Path to the file to open',
                        required=True)
    parser.add_argument('-i2', '--infile2',
                        dest='infile2',
                        type=str,
                        help='Path to the file to open',
                        required=True)

    return parser.parse_args()


def get_cat_num(fh_gen):
    '''
    get the dictionary that maps the gene numbers and categories
    @param fh_gen: the file including the data of categories of genes
    @return counts_new: the dictionary that maps the gene numbers and categories
    '''
    cat_list = []
    fh_gen.readline()
    for line in fh_gen:
        line = line.rstrip()
        line_gen_list = line.split('	')
        try:
            cat_list.append(line_gen_list[2])
        except IndexError:
            continue

    # sort the numbers of each category arranged in ascending order
    sorted_counts = dict(sorted(counts.items(), key=lambda x: x[1]))

    return sorted_counts


def get_cat_des_dict(fh_cat):
    '''
    get the dictionary that maps the gene descriptions and categories
    @param fh_cat: the file including the descriptions of categories of genes
    @return cat_des_dic: the dictionary that maps the gene descriptions and categories
    '''
    cat_des_dic = {}
    for line in fh_cat:
        line = line.rstrip()
        line_des_list = line.split('	')
        cat_des_dic[line_des_list[0]] = line_des_list[1]

    return cat_des_dic


if __name__ == '__main__':
    main()
