import streamlit as st
import pandas as pd
from seq2feature.main import extract_features
from seq2feature.ml import train_model, calculate_shap_values
from app.plots import (
    plot_feature_distribution,
    plot_correlation_matrix,
    plot_pca,
    plot_confusion_matrix,
    plot_shap_summary,
)

def initialize_session_state():
    if "df" not in st.session_state:
        st.session_state.df = None
    if "labels_df" not in st.session_state:
        st.session_state.labels_df = None
    if "model" not in st.session_state:
        st.session_state.model = None
    if "X_train" not in st.session_state:
        st.session_state.X_train = None
    if "X_test" not in st.session_state:
        st.session_state.X_test = None
    if "y_train" not in st.session_state:
        st.session_state.y_train = None
    if "y_test" not in st.session_state:
        st.session_state.y_test = None
    if "accuracy" not in st.session_state:
        st.session_state.accuracy = None
    if "model_type" not in st.session_state:
        st.session_state.model_type = None
    if "cm" not in st.session_state:
        st.session_state.cm = None

st.title("🧬 Seq2Feature - AI-Ready Sequence Feature Extractor")

# Initialize session state
initialize_session_state()

st.sidebar.header("1. Upload your FASTA file")
uploaded_file = st.sidebar.file_uploader(
    "Upload FASTA File",
    type=["fasta", "fa"],
    key="fasta_uploader",
    label_visibility="hidden",
)

st.sidebar.header("2. Upload your labels (optional)")
label_file = st.sidebar.file_uploader(
    "Upload Labels (CSV)", type=["csv"], key="label_uploader", label_visibility="hidden"
)

if uploaded_file is not None:
    st.sidebar.success("FASTA file uploaded successfully!")
    string_data = uploaded_file.getvalue().decode("utf-8")

    if label_file is not None:
        st.sidebar.success("Label file uploaded successfully!")
        labels_df = pd.read_csv(label_file)
        st.session_state.labels_df = labels_df

    st.header("Sequence Preview")
    st.text(string_data[:1000])

    st.header("Feature Selection")
    feature_types = st.multiselect(
        "Select feature types to extract",
        [
            "amino_acid_composition",
            "dipeptide_composition",
            "kmer_frequencies",
            "physicochemical",
        ],
    )

    k = None
    if "kmer_frequencies" in feature_types:
        k = st.number_input("Enter k-mer length", min_value=1, value=2)

    if st.button("Extract Features"):
        if not feature_types:
            st.warning("Please select at least one feature type.")
        else:
            with st.spinner("Extracting features..."):
                st.session_state.df = extract_features(string_data, feature_types, k)
            st.success("Features extracted successfully!")

if st.session_state.df is not None:
    df = st.session_state.df
    if df.empty:
        st.warning(
            "Feature extraction resulted in an empty dataframe. Please check your input file and selected features."
        )
    else:
        st.header("Extracted Features")
        st.dataframe(df)

        st.header("Summary Charts")
        numerical_cols = df.select_dtypes(include=["float64", "int64"]).columns
        if len(numerical_cols) > 0:
            selected_col = st.select_slider(
                "Select a feature to plot", options=numerical_cols
            )
            plot_feature_distribution(df, selected_col)

        st.header("Correlation Matrix")
        if st.button("Show Correlation Matrix"):
            with st.spinner("Generating correlation matrix..."):
                plot_correlation_matrix(df, numerical_cols)

        if st.session_state.labels_df is not None:
            st.header("Machine Learning")
            model_type = st.selectbox("Select a model", ["RandomForest", "SVM"])

            imputation_strategy = st.selectbox(
                "Select missing value imputation strategy",
                ["Fill with 0", "Fill with Mean", "Fill with Median", "Drop rows"]
            )

            st.info("Note: For reproducibility, a fixed random state (42) is used for model training and data splitting.")

            if st.button("Train Model"):
                with st.spinner("Training model...
"):
                    model, X_train, X_test, y_train, y_test, accuracy, cm = train_model(
                        df, st.session_state.labels_df, numerical_cols, model_type, imputation_strategy
                    )
                    if model:
                        st.session_state.model = model
                        st.session_state.X_train = X_train
                        st.session_state.X_test = X_test
                        st.session_state.y_train = y_train
                        st.session_state.y_test = y_test
                        st.session_state.accuracy = accuracy
                        st.session_state.model_type = model_type
                        st.session_state.cm = cm

                        st.success(f"{model_type} model trained successfully!")
                        st.metric("Accuracy", f"{accuracy:.2f}")
                        plot_confusion_matrix(cm)

            if st.session_state.model is not None:
                st.header("Dimensionality Reduction (PCA)")
                if st.button("Show PCA Plot"):
                    with st.spinner("Generating PCA plot...
"):
                        plot_pca(
                            st.session_state.X_train,
                            st.session_state.X_test,
                            st.session_state.y_train,
                            st.session_state.y_test,
                        )

                st.header("Feature Importance (SHAP)")
                if st.button("Show SHAP Plot"):
                    with st.spinner("Calculating SHAP values...
"):
                        shap_values = calculate_shap_values(
                            st.session_state.model, st.session_state.X_test
                        )
                        if shap_values is not None:
                            plot_shap_summary(shap_values, st.session_state.X_test)
