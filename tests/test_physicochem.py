from seq2feature.features.physicochem import get_physicochemical_features


def test_get_physicochemical_features():
    """Tests the get_physicochemical_features function."""
    sequence = "ARNDCEQGHILKMFPSTWYV"
    features = get_physicochemical_features(sequence)

    assert "molecular_weight" in features
    assert "aromaticity" in features
    assert "instability_index" in features
    assert "isoelectric_point" in features
    assert "gravy" in features

    # You can add more specific assertions here if you have expected values
    # For example:
    # assert abs(features["molecular_weight"] - expected_value) < 1e-6
