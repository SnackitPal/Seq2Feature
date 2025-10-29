import pandas as pd
from seq2feature.main import extract_features


def test_extract_features():
    """Tests the extract_features function with various feature types."""
    fasta_content = ">protein1\nARND\n>dna1\nAGCT\n"

    # Test amino acid composition
    df_aac = extract_features(fasta_content, feature_types=["amino_acid_composition"])
    assert isinstance(df_aac, pd.DataFrame)
    assert len(df_aac) == 2
    assert "A" in df_aac.columns
    # Protein1: A=1, R=1, N=1, D=1 -> A_comp = 1/4 = 0.25
    assert df_aac[df_aac["id"] == "protein1"]["A"].iloc[0] == 0.25

    # Test k-mer frequencies
    df_kmer = extract_features(fasta_content, feature_types=["kmer_frequencies"], k=2)
    assert "AG" in df_kmer.columns
    # dna1: AG, GC, CT -> AG_freq = 1/3
    assert df_kmer[df_kmer["id"] == "dna1"]["AG"].iloc[0] == 1 / 3

    # Test physicochemical features
    df_physchem = extract_features(fasta_content, feature_types=["physicochemical"])
    assert "molecular_weight" in df_physchem.columns
