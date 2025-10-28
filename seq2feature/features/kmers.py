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
    kmers = [sequence[i:i+k] for i in range(len(sequence) - k + 1)]
    count = Counter(kmers)
    total = len(kmers)
    frequencies = {kmer: count[kmer] / total for kmer in count}
    return frequencies
