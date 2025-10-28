from seq2feature.utils import detect_sequence_type


def test_detect_sequence_type():
    """Tests the detect_sequence_type function."""
    assert detect_sequence_type("ACGTN") == "DNA"
    assert detect_sequence_type("ACGUN") == "RNA"
    assert detect_sequence_type("ACDEFGHIKLMNPQRSTVWYBJZXO") == "Protein"
    assert detect_sequence_type("ACGTU") == "Unknown"
    assert detect_sequence_type("J") == "Protein"
    assert detect_sequence_type("") == "Unknown"
