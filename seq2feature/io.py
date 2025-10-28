from Bio import SeqIO

def read_fasta(file_path):
    """
    Reads a FASTA file and returns a list of SeqRecord objects.

    Args:
        file_path (str): The path to the FASTA file.

    Returns:
        list: A list of SeqRecord objects.
    """
    try:
        with open(file_path, "r") as handle:
            return list(SeqIO.parse(handle, "fasta"))
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []
