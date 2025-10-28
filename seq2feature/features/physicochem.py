from Bio.SeqUtils.ProtParam import ProteinAnalysis

def get_physicochemical_features(sequence):
    """
    Calculates physicochemical features of a protein sequence.

    Args:
        sequence (str): The protein sequence.

    Returns:
        dict: A dictionary with physicochemical features.
    """
    try:
        analysed_seq = ProteinAnalysis(sequence)
        features = {
            "molecular_weight": analysed_seq.molecular_weight(),
            "aromaticity": analysed_seq.aromaticity(),
            "instability_index": analysed_seq.instability_index(),
            "isoelectric_point": analysed_seq.isoelectric_point(),
            "gravy": analysed_seq.gravy(),
        }
        return features
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}
