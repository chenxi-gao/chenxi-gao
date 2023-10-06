#!user/bin/env python3
"""Test suite for econdary_structure_splitter.py"""
import pytest

from secondary_structure_splitter import get_filehandle, get_fasta_lists, \
    _verify_lists, output_result_to_file

def test_get_filehandle():
	"""
	"""
	filehandle = get_filehandle('ss.txt', "r")
	filehandle_test = open('ss.txt', "r")
	assert type(filehandle_test) == type(filehandle)


def test_get_fasta_lists_4_OSError():
	# does it raise OSError
    # this should exit
    with pytest.raises(OSError):
        get_filehandle("does_not_exist.ttttt", "r")


def test_get_fasta_lists_4_ValueError():
	# does it raise ValueError
    # this should exit
    with pytest.raises(ValueError):
        get_filehandle("ss.txt", "rrr")


def test_get_fasta_lists():
	file = open('ss.txt', "r")
	header_list, seq_list = get_fasta_lists(file)
	assert len(header_list) == len(seq_list)


def test__verify_lists():
	header_list = ['1', '2', '3']
	seq_list = ['a', 'b', 'c']
	assert _verify_lists(header_list, seq_list)


def test__verify_lists_do_not_match():
	header_list = ['1', '2']
	seq_list = ['a', 'b', 'c']
	with pytest.raises(SystemExit):
		_verify_lists(header_list, seq_list)


def output_result_to_file():
	header_list1 = ['1', '2', '3']
	seq_list = ['a', 'b', 'c']
	num_ss, num_protein = output_result_to_file(header_list1, seq_list, fh_out1, fh_out2)
	assert num_ss == 3
	assert num_protein == 3
