#!/usr/bin/env python3
# gene_names_from_chr21.py

"""
This program will ask the user to enter a gene symbol
and then prints the description for that gene based on data from the input file.

Sample command for executing the program:

$ python3 gene_names_from_chr21.py -i test_data/chr21_genes.txt

"""
import sys
import argparse
from get_file.io_utils import get_filehandle


def main():
    """ Business Logic """
    # get the file name
    args = get_file_args()
    filename = args.infile

    # open the file
    fh_in = get_filehandle(filename, "r")

    # get the dictionary that maps all the gene names and descriptions
    name_des_dict = get_name_description_dict(fh_in)

    # output the data we need
    while True:
        input_name = input("Enter gene name of interest. Type quit to exit:  ")
        if input_name in name_des_dict.keys():
            sys.stdout.write(f'\n{input_name} found! Here is the description:\n{name_des_dict[input_name]}\n\n')
        else:
            if input_name.lower() == "quit":
                print("Thanks for querying the data.")
                sys.exit()
            else:
                print("Not a valid gene name.\n")


def get_file_args():
    """
    Just get the command line options using argparse
    @return: Instance of argparse arguments
    """
    parser = argparse.ArgumentParser(
        description='Open chr21_genes.txt, and ask user for a gene name')

    parser.add_argument('-i', '--infile',
                        dest='infile',
                        type=str,
                        help='Path to the file to open',
                        required=True)

    return parser.parse_args()


def get_name_description_dict(fh_in):
    """
    get the dictionary that maps all the gene names and descriptions
    @param fh_in: The file handle from where we will get the gene names and their descriptions
    @return name_des: the dictionary that maps all the gene names and descriptions
    """
    name_des = {}
    fh_in.readline()
    for line in fh_in:
        line = line.rstrip()
        line_list = line.split('	')
        name_des[line_list[0]] = line_list[1]

    return name_des


if __name__ == '__main__':
    main()
