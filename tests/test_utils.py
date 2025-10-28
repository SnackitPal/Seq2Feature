from seq2feature.utils import detect_sequence_type

def test_detect_sequence_type():
    """Tests the detect_sequence_type function."""
    assert detect_sequence_type("ACGT") == "DNA"
    assert detect_sequence_type("ACGU") == "RNA"
    assert detect_sequence_type("ACDEFGHIKLMNPQRSTVWY") == "Protein"
    assert detect_sequence_type("ACGTU") == "Unknown"
    assert detect_sequence_type("J") == "Unknown"
    assert detect_sequence_type("") == "Unknown"
