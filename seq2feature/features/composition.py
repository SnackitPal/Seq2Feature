from collections import Counter
import itertools

def get_amino_acid_composition(sequence):
    """
    Calculates the amino acid composition of a protein sequence.

    Args:
        sequence (str): The protein sequence.

    Returns:
        dict: A dictionary with amino acids as keys and their frequencies as values.
    """
    count = Counter(sequence)
    total = len(sequence)
    composition = {aa: count[aa] / total for aa in count}
    return composition

def get_dipeptide_composition(sequence):
    """
    Calculates the dipeptide composition of a protein sequence.

    Args:
        sequence (str): The protein sequence.

    Returns:
        dict: A dictionary with dipeptides as keys and their frequencies as values.
    """
    dipeptides = [sequence[i:i+2] for i in range(len(sequence) - 1)]
    count = Counter(dipeptides)
    total = len(dipeptides)
    composition = {dp: count[dp] / total for dp in count}
    return composition
