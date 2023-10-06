#!/usr/bin/env python3
# nt_fasta_stats.py

"""
This program will open a file and get the length of the sequence
and also the percentage of 'C' and 'G' bases of the entire sequence

Sample command for executing the program:

$ python3 ./nt_fasta_stats.py --infile influenza.fasta --outfile influenza.stats.txt

"""

import sys
import argparse


def main():
    """ Business Logic """

    # get file handle to sequences in the fasta file
    args = get_file_args()
    filename = args.infile
    fh_in = get_filehandle(filename, "r")

    # open one outfile
    # (use get_filehandle function
    # the name of the output file will come from a command line option)
    outfile = "influenza.stats.txt"
    fh_out = get_filehandle(filename=outfile, mode="a")

    # loop over fasta filehandle and store the data in two lists
    # one for the header line and the other for the sequence data
    # (use get_fasta_lists function, see below).
    header, seqs = get_fasta_lists(fh_in)

    # process the lists, and determine the necessary output seen below
    # (use output_seq_statistics function, see below).
    output_seq_statistics(header_list=header, sequence_list=seqs, fh_out=fh_out)

    # # just clean up
    fh_in.close()
    fh_out.close()


def get_file_args():
    """
    Just get the command line options using argparse
    @return: Instance of argparse arguments
    """

    parser = argparse.ArgumentParser(
        description='Provide a FASTA file to generate nucleotide statistics')

    parser.add_argument('-i', '--infile',
                        dest='infile',
                        type=str,
                        help='Path to the file to open',
                        required=True)
    parser.add_argument('-o', '--outfile',
                        dest='outfile',
                        type=str,
                        help='Path to the file to write',
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
    except OSError as err:
        print('OSError: the file cannot be opened, please check the format of the file')
        raise err
    except ValueError as err:
        print('ValueError: the file does not exist for opening, or the wrong open mode')
        raise err
    else:
        return filehandle


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
        if line.startswith('>'):
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

    # check the last line
    the_last = seq_list[-1]
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
    This is a helper function helping to verify
    if the sizes of the two headers and sequences lists are the same
    @param header_list: the header lists got from get_fasta_lists()
    @param sequence_list: the sequence lists got from get_fasta_lists()
    @return header_list: the verified header lists got from get_fasta_lists()
    @return sequence_list: the verified sequence lists got from get_fasta_lists()
    """
    len_header = len(header_list)
    len_seq = len(sequence_list)
    if len_seq == len_header:
        return(header_list, sequence_list)

    print('Error: the length of two files does not match')
    sys.exit()


def output_seq_statistics(header_list, sequence_list, fh_out):
    """
    Outputing all the data we have handled and writing them into outfile
    @param header_list:the verified header lists got from get_fasta_lists()
    @param sequence_list:the verified sequence lists got from get_fasta_lists()
    @fh_out:the output bases' statistics we are going to write in

    """
    fh_out.write("Number   Accession     A's    G's    C's    T's    N's    Length    GC%\n")
    count = 0
    for index, header in enumerate(header_list):
        sequence = sequence_list[index]

        accession_string = _get_ncbi_accession(header)
        count += 1
        fh_out.write(f'{count}    {accession_string}    ')

        a_nt = str(_get_num_nucleotides('A', sequence)) + '    '
        c_nt = str(_get_num_nucleotides('C', sequence)) + '    '
        g_nt = str(_get_num_nucleotides('G', sequence)) + '    '
        t_nt = str(_get_num_nucleotides('T', sequence)) + '    '
        n_nt = str(_get_num_nucleotides('N', sequence)) + '    '
        length = len(sequence)
        gc_portion = 100 * (int(c_nt) + int(g_nt)) / length
        fh_out.write(f'{a_nt}{g_nt}{c_nt}{t_nt}{n_nt}{length}    {gc_portion:.1f}\n')


def _get_num_nucleotides(base, sequence):
    """
    This is a helper function to calculate the total numbers of every single base
    @param base: the base we are going to calculate
    @param sequence: the sequence where the bases come from
    @return num: the numbers of the certain base we are going to calculate
    """
    base_set = {'A', 'C', 'G', 'T', 'N'}
    if base in base_set:
        num = sequence.count(base)
        return num
    print('Did not code this condition')
    sys.exit()


def _get_ncbi_accession(header):
    """
    This is a helper function to extract the exact value of accession number
    @param header: the header including the accession number
    @return get_accession: the accession number we need

    """
    for character in header:
        if character == ' ':
            get_index = header.index(character)
    get_accession = header[1:get_index]
    return get_accession


if __name__ == '__main__':
    main()
