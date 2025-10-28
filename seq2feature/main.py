import pandas as pd
import argparse
import streamlit as st
from .io import read_fasta
from .utils import detect_sequence_type
from .features.composition import get_amino_acid_composition, get_dipeptide_composition
from .features.kmers import get_kmer_frequencies
from .features.physicochem import get_physicochemical_features


@st.cache_data
def extract_features(fasta_content, feature_types, k=None):
    """
    Extracts features from a FASTA string.

    Args:
        fasta_content (str): The string containing the FASTA data.
        feature_types (list): A list of feature types to extract.
            Possible values: 'amino_acid_composition', 'dipeptide_composition',
                             'kmer_frequencies', 'physicochemical'.
        k (int, optional): The k-mer length. Required if 'kmer_frequencies' is in feature_types.

    Returns:
        pandas.DataFrame: A DataFrame with the extracted features.
    """
    records = read_fasta(fasta_content)
    all_features = []

    for record in records:
        sequence = str(record.seq)
        seq_type = detect_sequence_type(sequence)
        features = {"id": record.id, "sequence": sequence, "type": seq_type}

        if "amino_acid_composition" in feature_types and seq_type == "Protein":
            features.update(get_amino_acid_composition(sequence))

        if "dipeptide_composition" in feature_types and seq_type == "Protein":
            features.update(get_dipeptide_composition(sequence))

        if "kmer_frequencies" in feature_types and k is not None:
            features.update(get_kmer_frequencies(sequence, k))

        if "physicochemical" in feature_types and seq_type == "Protein":
            features.update(get_physicochemical_features(sequence))

        all_features.append(features)

    return pd.DataFrame(all_features)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract features from biological sequences."
    )
    parser.add_argument(
        "--input", type=str, required=True, help="Path to the input FASTA file."
    )
    parser.add_argument(
        "--output", type=str, required=True, help="Path to the output CSV file."
    )
    parser.add_argument(
        "--feature_types",
        nargs="+",
        required=True,
        choices=[
            "amino_acid_composition",
            "dipeptide_composition",
            "kmer_frequencies",
            "physicochemical",
        ],
        help="A list of feature types to extract.",
    )
    parser.add_argument("--k", type=int, help="The k-mer length for k-mer frequencies.")

    args = parser.parse_args()

    if "kmer_frequencies" in args.feature_types and args.k is None:
        parser.error("--k is required when 'kmer_frequencies' is specified.")

    try:
        with open(args.input, "r") as f:
            fasta_content = f.read()
        df = extract_features(fasta_content, args.feature_types, args.k)
        df.to_csv(args.output, index=False)
        print(f"Features extracted and saved to {args.output}")
    except FileNotFoundError:
        print(f"Error: Input file not found at {args.input}")
