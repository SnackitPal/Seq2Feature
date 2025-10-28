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
    if re.match('^[ACGTN]+$', sequence):
        return 'DNA'
    elif re.match('^[ACGUN]+$', sequence):
        return 'RNA'
    # A more comprehensive check for protein sequences including ambiguous codes
    elif re.match('^[ACDEFGHIKLMNPQRSTVWYBJZXO]+$', sequence):
        return 'Protein'
    else:
        return 'Unknown'
