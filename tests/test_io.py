import os
from seq2feature.io import read_fasta

def test_read_fasta():
    """Tests the read_fasta function."""
    # Create a dummy fasta file
    file_path = "tests/temp_test.fasta"
    with open(file_path, "w") as f:
        f.write(">test1\nACGT\n")
        f.write(">test2\nGCTA\n")

    records = read_fasta(file_path)
    assert len(records) == 2
    assert records[0].id == "test1"
    assert str(records[0].seq) == "ACGT"
    assert records[1].id == "test2"
    assert str(records[1].seq) == "GCTA"

    # Clean up the dummy file
    os.remove(file_path)
