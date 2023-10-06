#!/usr/bin/env python3
# get_gene_level_information.py
'''
Getting data from the Unigene database Links to an external site.
'''
import sys
import re
import argparse
from config import config
from config import io_utils


def main():
    """Business Logic"""

    # get the host and gene name
    args = get_file_args()
    host_name = args.host
    gene_name = args.gene

    # standardize the input host name
    updated_host_name = update_host_name(host_name)

    # get the full file path
    file = "/".join((config.get_directory_for_unigene(),
                     updated_host_name, gene_name + "." + config.get_extension_for_unigene()))

    # check for the existence of file
    if io_utils.is_gene_file_valid(file):
        # using f-strings
        print(f"\nFound Gene {gene_name} for {updated_host_name.replace('_', ' ')}")
    else:
        print("Not found")
        print(f"Gene {gene_name} does not exist for {updated_host_name}. exiting now...", file=sys.stderr)
        sys.exit(1)

    # get the filehandle
    file_handle = io_utils.get_filehandle(file, "r")

    # get the data information of target gene
    extracted_tissue_list = get_data_for_gene_file(file_handle)

    # print the results
    print_host_to_gene_name_output(updated_host_name, gene_name, extracted_tissue_list)


def update_host_name(host_name) -> str:
    """
    This function take the host name and checks for the available conversions \
    from common to scientific names and return the scientific name
    """
    update_name = host_name.lower().replace('_', ' ')
    check_dict = config.get_keywords_for_hosts()
    if update_name in check_dict.keys():
        return check_dict[update_name]
    else:
        _print_directories_for_hosts()
        sys.exit(1)


def get_file_args():
    """
    Just get the command line options using argparse
    @return: Instance of argparse arguments
    """
    parser = argparse.ArgumentParser(
        description='Give the Host and Gene name')

    parser.add_argument('--host',
                        dest='host',
                        type=str,
                        help='Name of Host',
                        default='Human')

    parser.add_argument('-g', '--gene',
                        dest='gene',
                        type=str,
                        help='Name of Gene',
                        default='A1BG')

    return parser.parse_args()


def _print_directories_for_hosts():
    """
    to alert the user what directories do exist (see outputs below) and the exit the program.
    """
    print(f'\n\nEither the Host Name you are searching for is not in the database\
        \n\nor If you are trying to use the scientific name please put the name in double quotes:\
        \n\n"Scientific name"\
        \n\nHere is a (non-case sensitive) list of available Hosts by scientific name\n\
        ')
    check_dict = config.get_keywords_for_hosts()
    set_value = sorted(set(check_dict.values()))
    count_value = 1
    for value in set_value:
        print(f"{count_value:>3d}. {value}")
        count_value += 1

    print('\n\n\nHere is a (non-case sensitive) list of available Hosts by common name\n')

    count_key = 1
    for value in check_dict:
        print(f"{count_key:>3d}. {value[0].upper()}{value[1:].lower()}")
        count_key += 1


def get_data_for_gene_file(file_handle):
    """
    extracts the list of tissues in which this gene is expressed and returns a sorted list of the tissues.
    """
    for line in file_handle:
        match = re.search('^EXPRESS(.*)', line)
        if match:
            tissue_string = match.group(1)
            tissue_list = tissue_string.lstrip().split('|')
            for tissue in tissue_list:
                index = tissue_list.index(tissue)
                tissue_list[index] = tissue.lstrip().rstrip()
            tissue_list_sorted = sorted(tissue_list)

    return tissue_list_sorted


def print_host_to_gene_name_output(host_name, gene_name, data_from_gene_file):
    """
    This function should print the tissue expression data for the gene.
    """
    updated_host_name = host_name.replace("_", " ")
    print(f"In {updated_host_name}, There are {len(data_from_gene_file)} tissues that {gene_name} is expressed in:\n")
    count = 1
    for tissue in data_from_gene_file:
        print(f"{count:>3d}. {tissue[0].upper()}{tissue[1:].lower()}")
        count += 1


if __name__ == '__main__':
    main()
