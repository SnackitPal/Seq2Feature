from seq2feature.features.kmers import get_kmer_frequencies

def test_get_kmer_frequencies():
    """Tests the get_kmer_frequencies function."""
    sequence = "AGTAGT"
    # Test for k=1
    k1_freq = get_kmer_frequencies(sequence, 1)
    assert abs(k1_freq['A'] - 2/6) < 1e-9
    assert abs(k1_freq['G'] - 2/6) < 1e-9
    assert abs(k1_freq['T'] - 2/6) < 1e-9

    # Test for k=2
    k2_freq = get_kmer_frequencies(sequence, 2)
    assert abs(k2_freq['AG'] - 2/5) < 1e-9
    assert abs(k2_freq['GT'] - 2/5) < 1e-9
    assert abs(k2_freq['TA'] - 1/5) < 1e-9

    # Test for k=3
    k3_freq = get_kmer_frequencies(sequence, 3)
    assert abs(k3_freq['AGT'] - 2/4) < 1e-9
    assert abs(k3_freq['GTA'] - 1/4) < 1e-9
    assert abs(k3_freq['TAG'] - 1/4) < 1e-9
