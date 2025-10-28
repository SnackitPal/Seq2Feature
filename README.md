# Seq2Feature: AI-Ready Sequence Feature Extractor

## 🧬 Project Goal

To create a user-friendly tool that automatically extracts meaningful **numerical features** from **DNA, RNA, or protein sequences**, making them ready for **machine learning or statistical modeling** — without requiring users to code.

## ✨ Features

*   **Input Handling:** Read FASTA file content directly from uploaded files (no temporary files).
*   **Sequence Type Detection:** Automatically identifies sequence type (DNA, RNA, Protein).
*   **Feature Extraction Engine:**
    *   Amino Acid Composition
    *   Dipeptide Composition (optimized for efficiency)
    *   K-mer Frequencies (configurable k, optimized for efficiency)
    *   Physicochemical Properties (Molecular Weight, Aromaticity, Instability Index, Isoelectric Point, Gravy)
    *   **Performance:** Feature extraction is cached for faster re-runs with the same input.
*   **Interactive Visualizations:**
    *   Histograms of individual feature distributions (interactive slider).
    *   Correlation Matrix Heatmap for feature relationships.
    *   2D PCA Projection Plot for dimensionality reduction and sequence clustering, now visualizing train/test splits to prevent data leakage.
*   **Machine Learning Integration:**
    *   Upload custom labels for classification tasks.
    *   Train RandomForest and Support Vector Machine (SVM) models.
    *   **Missing Value Handling:** User-selectable strategies for imputing missing values (fill with 0, mean, median, or drop rows).
    *   Evaluate model performance with Accuracy and Confusion Matrices.
    *   Interpret feature importance using SHAP (SHapley Additive exPlanations) values.
    *   **Reproducibility:** A fixed random state (42) is used for model training and data splitting.
*   **Export Options:**
    *   Download extracted features as a CSV file.
    *   Download all generated plots as a ZIP archive.
    *   Download the trained machine learning model and a performance report as a ZIP archive.
*   **Command-Line Interface (CLI):** Extract features directly from the terminal.
*   **Streamlit Web Application:** A user-friendly, interactive web interface for all functionalities, with improved error/success messages and streamlined session state management.

## 🚀 Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   Python 3.8+
*   `pip` (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/SnackitPal/Seq2Feature.git
    cd seq2feature
    ```
    *(Replace `<your-github-repo-url>` with the actual URL of your GitHub repository)*

2.  **Create and activate a virtual environment:**
    It's highly recommended to use a virtual environment to manage project dependencies.
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `.\venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -e .
    pip install -r requirements.txt
    ```
    *(This will install all necessary packages, including `black` for code formatting and `ruff` for linting.)*

4.  **Prepare the dataset (for testing):**
    To test the full pipeline, you can download a sample protein classification dataset and prepare it using the provided script.

    *   **Download the dataset:**
        Navigate to [http://afproject.org/dataset/protein-low-ident/](http://afproject.org/dataset/protein-low-ident/) and download `protein-low-ident.zip`. Save it to the `data/` directory in your project.

    *   **Unzip the dataset:**
        ```bash
        cd data
        unzip protein-low-ident.zip
        cd ..
        ```
        *(If `unzip` is not found, install it: `sudo apt install unzip`)*

    *   **Generate `sequences.fasta` and `labels.csv`:**
        ```bash
        python prepare_dataset.py
        ```
        This script will combine the individual FASTA files and create a `labels.csv` based on the major protein class.

## 💻 How to Run the Web Application

Once you have installed the dependencies and optionally prepared the dataset:

1.  **Start the Streamlit app:**
    ```bash
    streamlit run app/streamlit_app.py
    ```
2.  Open your web browser and navigate to `http://localhost:8501` (or the Network URL provided in your terminal).

### Using the App

1.  **Upload FASTA File:** Use the sidebar to upload your FASTA file (e.g., `data/sequences.fasta`).
2.  **Upload Labels (Optional):** If you want to train a machine learning model, upload your `labels.csv` file (e.g., `data/labels.csv`).
3.  **Select Features:** Choose the feature types you want to extract. If `kmer_frequencies` is selected, specify the k-mer length.
4.  **Extract Features:** Click the "Extract Features" button.
5.  **Explore Results:**
    *   View the extracted features in a data table.
    *   Use the slider in "Summary Charts" to visualize individual feature distributions.
    *   Click "Show Correlation Matrix" to see feature relationships.
    *   Click "Show PCA Plot" for a 2D projection of your feature space.
6.  **Machine Learning (if labels uploaded):**
    *   Select a model (RandomForest or SVM).
    *   Click "Train Model" to see accuracy and a confusion matrix.
    *   Click "Show SHAP Plot" to understand feature importance.
7.  **Download Results:** Download features, plots, or the trained model and report.

## ⚙️ Command-Line Interface (CLI) Usage

You can also extract features directly from the terminal:

```bash
python -m seq2feature.main --input data/sequences.fasta --output extracted_features.csv --feature_types amino_acid_composition physicochemical kmer_frequencies --k 3
```

*   `--input`: Path to your input FASTA file.
*   `--output`: Path to save the extracted features CSV.
*   `--feature_types`: Space-separated list of feature types.
*   `--k`: (Optional) K-mer length if `kmer_frequencies` is selected.

## 📁 Project Structure

```
Seq2Feature/
├── seq2feature/
│   ├── __init__.py
│   ├── io.py             # File reading functions (FASTA content)
│   ├── features/         # Feature extraction modules
│   │   ├── composition.py
│   │   ├── physicochem.py
│   │   └── kmers.py
│   ├── ml.py             # Machine Learning functions (model training, SHAP)
│   ├── utils.py          # Utility functions (sequence type detection)
│   └── main.py           # Integrates modules, CLI entry point
│
├── app/
│   ├── streamlit_app.py  # Streamlit web interface
│   └── plots.py          # Plotting utilities for the Streamlit app
│
├── tests/
│   ├── test_composition.py
│   ├── test_io.py
│   ├── test_kmers.py
│   ├── test_main.py
│   ├── test_physicochem.py
│   └── test_utils.py
│
├── data/
│   ├── example_sequences.fasta # Small example FASTA
│   ├── labels.csv        # Small example labels
│   ├── protein-low-ident/ # Unzipped dataset from AFproject
│   ├── sequences.fasta   # Combined FASTA from prepare_dataset.py
│   └── labels.csv        # Generated labels from prepare_dataset.py
│
├── prepare_dataset.py    # Script to prepare AFproject dataset
├── README.md             # Project documentation
├── PROGRESS.md           # Development progress log
├── requirements.txt      # Python dependencies
└── setup.py              # Package installation configuration
```

## 🤝 Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## 📞 Contact

For any questions or feedback, please contact sanketpalwe@gmail.com.
