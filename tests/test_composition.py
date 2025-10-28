from seq2feature.features.composition import get_amino_acid_composition, get_dipeptide_composition

def test_get_amino_acid_composition():
    """Tests the get_amino_acid_composition function."""
    sequence = "ARNDCEQGHILKMFPSTWYV"
    composition = get_amino_acid_composition(sequence)
    assert len(composition) == 20
    for aa in sequence:
        assert composition[aa] == 0.05

    sequence = "AARND"
    composition = get_amino_acid_composition(sequence)
    assert abs(composition['A'] - 0.4) < 1e-9
    assert abs(composition['R'] - 0.2) < 1e-9
    assert abs(composition['N'] - 0.2) < 1e-9
    assert abs(composition['D'] - 0.2) < 1e-9

def test_get_dipeptide_composition():
    """Tests the get_dipeptide_composition function."""
    sequence = "ARND"
    composition = get_dipeptide_composition(sequence)
    assert len(composition) == 3
    assert abs(composition['AR'] - 1/3) < 1e-9
    assert abs(composition['RN'] - 1/3) < 1e-9
    assert abs(composition['ND'] - 1/3) < 1e-9

    sequence = "AARA"
    composition = get_dipeptide_composition(sequence)
    assert len(composition) == 3
    assert abs(composition['AA'] - 1/3) < 1e-9
    assert abs(composition['AR'] - 1/3) < 1e-9
    assert abs(composition['RA'] - 1/3) < 1e-9
