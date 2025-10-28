import os
import pandas as pd

# Define paths
data_dir = "data"
unzipped_dir = os.path.join(data_dir, "protein-low-ident")
output_fasta = os.path.join(data_dir, "sequences.fasta")
output_labels = os.path.join(data_dir, "labels.csv")

# Initialize lists to store data
all_sequences = []
labels_data = []

# Iterate through each FASTA file in the unzipped directory
for filename in os.listdir(unzipped_dir):
    if filename.endswith(".fasta"):
        file_path = os.path.join(unzipped_dir, filename)
        
        # Extract protein ID from filename (e.g., d1a0aa_ from d1a0aa_.fasta)
        protein_id = filename.replace(".fasta", "")
        
        # Extract the major protein class from the protein ID
        # e.g., d1a0aa_ -> 1 (for all alpha proteins)
        if len(protein_id) >= 2 and protein_id.startswith('d'):
            class_label = protein_id[1] # The character after 'd'
        else:
            class_label = "unknown" # Fallback for unexpected formats

        # Read the content of the FASTA file
        with open(file_path, "r") as f:
            content = f.read()
            all_sequences.append(content)
        
        labels_data.append({"id": protein_id, "label": class_label})

# Combine all sequences into a single FASTA file
with open(output_fasta, "w") as outfile:
    for seq_content in all_sequences:
        outfile.write(seq_content)

# Create the labels DataFrame and save to CSV
labels_df = pd.DataFrame(labels_data)
labels_df.to_csv(output_labels, index=False)

print(f"Combined FASTA file created: {output_fasta}")
print(f"Labels CSV file created: {output_labels}")
print(f"Number of sequences processed: {len(all_sequences)}")
print(f"Number of unique labels created: {labels_df['label'].nunique()}")
