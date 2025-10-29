import pandas as pd
import argparse
import streamlit as st
from .io import read_fasta
from .utils import detect_sequence_type
from .features.composition import get_amino_acid_composition, get_dipeptide_composition
from .features.kmers import get_kmer_frequencies
from .features.physicochem import get_physicochemical_features

FEATURE_REGISTRY = {
    "amino_acid_composition": (get_amino_acid_composition, ["Protein"]),
    "dipeptide_composition": (get_dipeptide_composition, ["Protein"]),
    "kmer_frequencies": (get_kmer_frequencies, ["DNA", "RNA", "Protein"]),
    "physicochemical": (get_physicochemical_features, ["Protein"]),
}

def _extract_single_sequence_features(sequence, seq_type, feature_types, k=None):
    """Extracts features for a single sequence based on its type."""
    features = {}
    for feature in feature_types:
        func, supported_types = FEATURE_REGISTRY.get(feature, (None, []))
        if func and seq_type in supported_types:
            if feature == "kmer_frequencies" and k is not None:
                features.update(func(sequence, k))
            else:
                features.update(func(sequence))
    return features

@st.cache_data
def extract_features(fasta_content, feature_types, k=None, sequence_type="auto"):
    """
    Extracts features from a FASTA string, with enhanced modularity and performance.

    Args:
        fasta_content (str): The string containing the FASTA data.
        feature_types (list): A list of feature types to extract.
        k (int, optional): The k-mer length for k-mer frequencies.
        sequence_type (str): The type of sequence, e.g., 'DNA', 'RNA', 'Protein', or 'auto'.
    
    Returns:
        pandas.DataFrame: A DataFrame with the extracted features.
    """
    records = read_fasta(fasta_content)
    all_features = []

    with st.spinner("Extracting features..."):
        progress_bar = st.progress(0)
        for i, record in enumerate(records):
            sequence = str(record.seq)
            seq_type = sequence_type if sequence_type != "auto" else detect_sequence_type(sequence)
            
            features = {"id": record.id, "sequence": sequence, "type": seq_type}
            features.update(_extract_single_sequence_features(sequence, seq_type, feature_types, k))
            all_features.append(features)
            progress_bar.progress((i + 1) / len(records))

    return pd.DataFrame(all_features)

def main():
    """Command-line interface for feature extraction."""
    parser = argparse.ArgumentParser(description="Extract features from biological sequences.")
    parser.add_argument("--input", type=str, required=True, help="Path to the input FASTA file.")
    parser.add_argument("--output", type=str, required=True, help="Path to the output CSV file.")
    parser.add_argument(
        "--feature_types", nargs="+", required=True, choices=FEATURE_REGISTRY.keys(),
        help="A list of feature types to extract."
    )
    parser.add_argument("--k", type=int, help="The k-mer length for k-mer frequencies.")
    parser.add_argument(
        "--sequence_type", type=str, default="auto", choices=["auto", "DNA", "RNA", "Protein"],
        help="Specify the sequence type or 'auto' for detection."
    )

    args = parser.parse_args()

    if "kmer_frequencies" in args.feature_types and not args.k:
        parser.error("--k is required when 'kmer_frequencies' is specified.")

    try:
        with open(args.input, "r") as f:
            fasta_content = f.read()
        df = extract_features(fasta_content, args.feature_types, args.k, args.sequence_type)
        df.to_csv(args.output, index=False)
        print(f"Features extracted and saved to {args.output}")
    except FileNotFoundError:
        print(f"Error: Input file not found at {args.input}")

if __name__ == "__main__":
    main()
