import os
import pandas as pd
from seq2feature.main import extract_features

def test_extract_features():
    """Tests the extract_features function."""
    # Create a dummy fasta file
    file_path = "tests/temp_test.fasta"
    with open(file_path, "w") as f:
        f.write(">protein1\nARND\n")
        f.write(">dna1\nAGCT\n")

    # Test amino acid composition
    df = extract_features(file_path, feature_types=['amino_acid_composition'])
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert "A" in df.columns
    assert df[df['id'] == 'protein1']['A'].iloc[0] == 0.25

    # Test k-mer frequencies
    df = extract_features(file_path, feature_types=['kmer_frequencies'], k=2)
    assert "AG" in df.columns
    assert df[df['id'] == 'dna1']['AG'].iloc[0] == 1/3

    # Test physicochemical features
    df = extract_features(file_path, feature_types=['physicochemical'])
    assert "molecular_weight" in df.columns

    # Clean up the dummy file
    os.remove(file_path)
