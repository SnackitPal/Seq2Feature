from collections import Counter


def get_kmer_frequencies(sequence, k):
    """
    Calculates the k-mer frequencies of a sequence.

    Args:
        sequence (str): The biological sequence.
        k (int): The length of the k-mer.

    Returns:
        dict: A dictionary with k-mers as keys and their frequencies as values.
    """
    total = len(sequence) - k + 1
    if total <= 0:
        return {}
    count = Counter(sequence[i : i + k] for i in range(total))
    frequencies = {kmer: c / total for kmer, c in count.items()}
    return frequencies
