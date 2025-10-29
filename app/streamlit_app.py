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
    """Initializes the session state variables."""
    session_defaults = {
        "df": None,
        "labels_df": None,
        "model": None,
        "X_train": None,
        "X_test": None,
        "y_train": None,
        "y_test": None,
        "accuracy": None,
        "model_type": None,
        "cm": None,
    }
    for key, value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def ui_sidebar():
    """Handles the sidebar UI elements."""
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

    if uploaded_file:
        st.sidebar.success("FASTA file uploaded successfully!")
        if label_file:
            st.sidebar.success("Label file uploaded successfully!")
            st.session_state.labels_df = pd.read_csv(label_file)
        return uploaded_file.getvalue().decode("utf-8")
    return None

def ui_main_content(string_data):
    """Handles the main content area of the UI."""
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

    k = st.number_input("Enter k-mer length", min_value=1, value=2) if "kmer_frequencies" in feature_types else None

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
            st.warning("Feature extraction resulted in an empty dataframe.")
        else:
            st.header("Extracted Features")
            st.dataframe(df)
            render_charts_and_ml(df)

def render_charts_and_ml(df):
    """Renders the charts and machine learning sections."""
    st.header("Summary Charts")
    numerical_cols = df.select_dtypes(include=["float64", "int64"]).columns
    if not numerical_cols.empty:
        selected_col = st.select_slider("Select a feature to plot", options=numerical_cols)
        plot_feature_distribution(df, selected_col)

        st.header("Correlation Matrix")
        if st.button("Show Correlation Matrix"):
            with st.spinner("Generating correlation matrix..."):
                plot_correlation_matrix(df, numerical_cols)

    if st.session_state.labels_df is not None:
        render_ml_section(df, numerical_cols)

def render_ml_section(df, numerical_cols):
    """Renders the machine learning section."""
    st.header("Machine Learning")
    model_type = st.selectbox("Select a model", ["RandomForest", "SVM"])
    imputation_strategy = st.selectbox(
        "Select missing value imputation strategy",
        ["Fill with 0", "Fill with Mean", "Fill with Median", "Drop rows"],
    )

    st.info("Note: A fixed random state (42) is used for reproducibility.")

    if st.button("Train Model"):
        with st.spinner("Training model..."):
            model, X_train, X_test, y_train, y_test, accuracy, cm = train_model(
                df, st.session_state.labels_df, numerical_cols, model_type, imputation_strategy
            )
            if model:
                st.session_state.update({
                    "model": model, "X_train": X_train, "X_test": X_test,
                    "y_train": y_train, "y_test": y_test, "accuracy": accuracy,
                    "model_type": model_type, "cm": cm
                })
                st.success(f"{model_type} model trained successfully!")
                st.metric("Accuracy", f"{accuracy:.2f}")
                plot_confusion_matrix(cm)

    if st.session_state.model is not None:
        render_post_training_plots()

def render_post_training_plots():
    """Renders plots after model training."""
    st.header("Dimensionality Reduction (PCA)")
    if st.button("Show PCA Plot"):
        with st.spinner("Generating PCA plot..."):
            plot_pca(st.session_state.X_train, st.session_state.X_test, st.session_state.y_train, st.session_state.y_test)

    st.header("Feature Importance (SHAP)")
    if st.button("Show SHAP Plot"):
        with st.spinner("Calculating SHAP values..."):
            shap_values = calculate_shap_values(st.session_state.model, st.session_state.X_test)
            if shap_values is not None:
                plot_shap_summary(shap_values, st.session_state.X_test, st.session_state.model)

def main():
    """
    Main function to run the Streamlit application.
    This function initializes the session state, sets up the UI,
    and handles the main application logic.
    """
    st.set_page_config(
        page_title="Seq2Feature",
        page_icon="🧬",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.title("🧬 Seq2Feature - AI-Ready Sequence Feature Extractor")

    initialize_session_state()
    string_data = ui_sidebar()

    if string_data:
        ui_main_content(string_data)

if __name__ == "__main__":
    main()
