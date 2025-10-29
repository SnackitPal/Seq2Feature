import os
from seq2feature.io import read_fasta


def test_read_fasta():
    """Tests the read_fasta function with valid FASTA content."""
    fasta_content = ">test1\nACGT\n>test2\nGCTA\n"
    records = read_fasta(fasta_content)
    assert len(records) == 2
    assert records[0].id == "test1"
    assert str(records[0].seq) == "ACGT"
    assert records[1].id == "test2"
    assert str(records[1].seq) == "GCTA"


def test_read_fasta_empty_content():
    """Tests read_fasta with empty content."""
    records = read_fasta("")
    assert len(records) == 0


def test_read_fasta_invalid_format():
    """Tests read_fasta with an invalid FASTA format."""
    invalid_content = "This is not a FASTA file"
    records = read_fasta(invalid_content)
    assert len(records) == 0
