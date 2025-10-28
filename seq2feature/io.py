from Bio import SeqIO
import io


def read_fasta(data):
    """
    Reads a FASTA file from a string and returns a list of SeqRecord objects.

    Args:
        data (str): The string containing the FASTA data.

    Returns:
        list: A list of SeqRecord objects.
    """
    try:
        with io.StringIO(data) as handle:
            return list(SeqIO.parse(handle, "fasta"))
    except Exception as e:
        print(f"An unexpected error occurred while parsing FASTA data. Details: {e}")
        return []
