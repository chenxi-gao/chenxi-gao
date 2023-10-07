#!/usr/bin/env python3
# secondary_structure_splitter.py

"""
this program will open a file included the information of
amino acids sequence and its secondary sturcture,
generating two files, one is includes its amino sequence
and the other includes its secondary structure in fasta format

Sample command for executing the program:

$ python3 ./secondary_structure_splitter.py --infile ss.txt

"""

import sys
import argparse


def main():
    """ Business Logic """
    args = get_file_args()
    filename = args.infile

    # Hardcoded output files
    outfile1 = "pdb_protein.fasta"
    outfile2 = "pdb_ss.fasta"

    # Using get_filehandle() for one input, two output files
    fh_in = get_filehandle(filename, "r")
    fh_out1 = get_filehandle(filename=outfile1, mode="w")
    fh_out2 = get_filehandle(filename=outfile2, mode="w")

    # get the two lists of data from the FASTA file
    header, seqs = get_fasta_lists(fh_in)  # get the two lists of data

    # print out the results, and get some final output variables
    num_protein, num_ss = output_result_to_file(header_list=header,
                                                seq_list=seqs, fh_out1=fh_out1, fh_out2=fh_out2)

    # writing this to STDERR
    sys.stderr.write("Found {} protein sequences\n".format(num_protein))
    sys.stderr.write("Found {} ss sequences\n".format(num_ss))

    # # just clean up
    fh_in.close()
    fh_out1.close()
    fh_out2.close()


def get_file_args():
    """
    Just get the command line options using argparse
    @return: Instance of argparse arguments
    """

    parser = argparse.ArgumentParser(
        description='Provide a FASTA file to perform splitting on sequence and secondary structure')

    parser.add_argument('-i', '--infile',
                        dest='infile',
                        type=str,
                        help='Path to the file to open',
                        required=True)

    return parser.parse_args()


def get_filehandle(filename, mode):
    """
    To open the file name passed in, and passes back two files object
    @param filenname: file to open
    @param mode: operation mode
    @return: the opened filehandle
    """
    try:
        filehandle = open(filename, mode)
        return filehandle
    except OSError as err:
        print('OSError: the file cannot be opened, please check the format of the file')
        raise err
    except ValueError as err:
        print('ValueError: the file does not exist for opening, or the wrong open mode')
        raise err


def get_fasta_lists(filename):
    """
    Generating two one-to-one correspondence to the data lists, separating the headers and sequences
    @param filename: a file handle to the fasta file used in this program
    @return header_list: the headers list
    @return seq_list: the sequences list
    """
    sequence = {}
    header = None
    data = ''
    header_list = []
    seq_list = []

    for line in filename:
        if line.endswith('sequence\n') or line.endswith('secstr\n') \
                or line.endswith('sequence') or line.endswith('secstr'):
            if header and data:
                sequence[header] = data
            data = ''
            header = line.rstrip()
        else:
            data += line.rstrip()

    if header and data:
        sequence[header] = data
    elif header:
        sequence[header] = ""

    for header, data in sequence.items():
        header_list.append(header)
        seq_list.append(data)

    the_last = seq_list[-1]
    # check the last line
    if the_last == "":
        seq_list.pop()

    if the_last.endswith('sequence') or the_last.endswith('secstr'):
        for character in the_last:
            if character == '>':
                get_index = the_last.index(character)
                get_header = the_last[get_index:-1]
                header_list.append(get_header)
    if _verify_lists(header_list, seq_list):
        return header_list, seq_list
    return None


def _verify_lists(header_list, sequence_list):
    """
    This is a helper function helping to verify if the sizes
    of the two headers and sequences lists are the same
    @param header_list: the header lists got from get_fasta_lists()
    @param sequence_list: the sequence lists got from get_fasta_lists()
    @return header_list: the verified header lists got from get_fasta_lists()
    @return sequence_list: the verified sequence lists got from get_fasta_lists()
    """
    len_header = len(header_list)
    len_seq = len(sequence_list)
    if len_seq == len_header:
        return True

    print('Error: the length of two files does not match')
    sys.exit()


def output_result_to_file(header_list, seq_list, fh_out1, fh_out2):
    """
    Outputting all the data handling within this program
    and write out two files including the sequence of amino acids,
    and secondary structure of proteins seperately
    @param header_list: the verified header lists got from get_fasta_lists()
    @param seq_list: the verified sequence lists got from get_fasta_lists()
    @param fh_out1: the output protein file we are going to write in
    @param fh_out2: the output secondary structure file we are going to write in
    @retuen num_ss: the numbers of secondart structures we found from the input file
    @return num_protein: the numbers of proteins we found from the input file
    """
    protein = []
    secondary_structure = []

    for header in header_list:
        index_num = header_list.index(header)
        if header.endswith('sequence'):
            protein.append(seq_list[index_num])
        else:
            secondary_structure.append(seq_list[index_num])
    fh_out1.write(str(protein))
    fh_out2.write(str(secondary_structure))

    num_protein = len(protein)
    num_ss = len(secondary_structure)

    return num_protein, num_ss


if __name__ == '__main__':
    main()
