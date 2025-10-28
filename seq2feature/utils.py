import re

def detect_sequence_type(sequence):
    """
    Detects the type of a biological sequence (DNA, RNA, or Protein).

    Args:
        sequence (str): The biological sequence.

    Returns:
        str: The sequence type ('DNA', 'RNA', 'Protein', or 'Unknown').
    """
    sequence = sequence.upper()
    if re.match('^[ACGT]+$', sequence):
        return 'DNA'
    elif re.match('^[ACGU]+$', sequence):
        return 'RNA'
    # A more comprehensive check for protein sequences
    elif re.match('^[ACDEFGHIKLMNPQRSTVWY]+$', sequence):
        return 'Protein'
    else:
        return 'Unknown'
