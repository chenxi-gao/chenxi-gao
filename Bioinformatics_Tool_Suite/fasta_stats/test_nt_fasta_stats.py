#!user/bin/env python3
"""Test suite for nt_fasta_stats.py"""
import pytest

from nt_fasta_stats import get_filehandle, get_fasta_lists, \
	_verify_lists, output_seq_statistics, _get_num_nucleotides, _get_ncbi_accession

def test_get_filehandle():
	filehandle = get_filehandle('ss.txt', "r")
	filehandle_test = open('ss.txt', "r")
	assert type(filehandle_test) == type(filehandle)

def test_get_fasta_lists_4_OSError():
	# does it raise OSError
    # this should exit
    with pytest.raises(OSError):
        get_filehandle("does_not_exist.zdczds", "r")


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


def test__get_num_nucleotides():
	base = 'A'
	sequence = 'ACGTA'
	num = _get_num_nucleotides(base, sequence)
	assert num == 2


def test__get_ncbi_accession():
	header = '>EU521893 A/Arequipa/FLU3833/2006 2006// 4 (HA)'
	acession = _get_ncbi_accession(header)
	assert acession == 'EU521893'
