import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import zipfile
import joblib
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix
import shap
import numpy as np
from seq2feature.main import extract_features

st.title("🧬 Seq2Feature - AI-Ready Sequence Feature Extractor")

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'labels_df' not in st.session_state:
    st.session_state.labels_df = None
if 'model' not in st.session_state:
    st.session_state.model = None
if 'X_test' not in st.session_state:
    st.session_state.X_test = None
if 'accuracy' not in st.session_state:
    st.session_state.accuracy = None
if 'model_type' not in st.session_state:
    st.session_state.model_type = None

st.sidebar.header("1. Upload your FASTA file")
uploaded_file = st.sidebar.file_uploader("", type=["fasta", "fa"], key="fasta_uploader")

st.sidebar.header("2. Upload your labels (optional)")
label_file = st.sidebar.file_uploader("", type=["csv"], key="label_uploader")

if uploaded_file is not None:
    st.sidebar.success("FASTA file uploaded successfully!")
    string_data = uploaded_file.getvalue().decode("utf-8")
    with open("temp.fasta", "w") as f:
        f.write(string_data)

    if label_file is not None:
        st.sidebar.success("Label file uploaded successfully!")
        labels_df = pd.read_csv(label_file)
        st.session_state.labels_df = labels_df

    st.header("Sequence Preview")
    st.text(string_data[:1000])

    st.header("Feature Selection")
    feature_types = st.multiselect(
        "Select feature types to extract",
        ['amino_acid_composition', 'dipeptide_composition', 'kmer_frequencies', 'physicochemical']
    )

    k = None
    if 'kmer_frequencies' in feature_types:
        k = st.number_input("Enter k-mer length", min_value=1, value=2)

    if st.button("Extract Features"):
        if not feature_types:
            st.warning("Please select at least one feature type.")
        else:
            with st.spinner("Extracting features..."):
                st.session_state.df = extract_features("temp.fasta", feature_types, k)

if st.session_state.df is not None:
    df = st.session_state.df
    st.header("Extracted Features")
    st.dataframe(df)

    st.header("Summary Charts")
    numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
    selected_col = st.select_slider("Select a feature to plot", options=numerical_cols)
    
    fig, ax = plt.subplots()
    df[selected_col].hist(ax=ax)
    ax.set_title(selected_col)
    st.pyplot(fig)

    st.header("Correlation Matrix")
    if st.button("Show Correlation Matrix"):
        corr = df[numerical_cols].corr()
        fig, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(corr, ax=ax, cmap='viridis', annot=(len(numerical_cols) < 20), fmt=".2f")
        ax.set_title("Feature Correlation Matrix")
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        st.pyplot(fig)

    st.header("Dimensionality Reduction")
    if st.button("Show PCA Plot"):
        pca = PCA(n_components=2)
        # Fill NaNs before fitting PCA
        filled_df = df[numerical_cols].fillna(0)
        principal_components = pca.fit_transform(filled_df)
        pca_df = pd.DataFrame(data = principal_components, columns = ['principal component 1', 'principal component 2'])
        pca_df['type'] = df['type']

        fig, ax = plt.subplots(figsize=(10, 8))
        sns.scatterplot(x='principal component 1', y='principal component 2', hue='type', data=pca_df, ax=ax)
        ax.set_title('2D PCA of Features')
        st.pyplot(fig)

    if st.session_state.labels_df is not None:
        st.header("Machine Learning")
        model_type = st.selectbox("Select a model", ["RandomForest", "SVM"])

        if st.button("Train Model"):
            with st.spinner("Training model..."):
                # Merge features and labels
                merged_df = pd.merge(df, st.session_state.labels_df, on="id")
                
                # Prepare data for training
                X = merged_df[numerical_cols].fillna(0)
                y = merged_df['label']
                
                if len(X) < 5:
                    st.warning("The dataset is too small for a meaningful train/test split and accuracy score.")
                else:
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

                    # Train model
                    if model_type == "RandomForest":
                        model = RandomForestClassifier(random_state=42)
                    else:
                        model = SVC(random_state=42)
                    
                    model.fit(X_train, y_train)
                    y_pred = model.predict(X_test)
                    accuracy = accuracy_score(y_test, y_pred)
                    cm = confusion_matrix(y_test, y_pred)

                    st.session_state.model = model
                    st.session_state.X_test = X_test
                    st.session_state.accuracy = accuracy
                    st.session_state.model_type = model_type

                    st.success(f"{model_type} model trained successfully!")
                    st.metric("Accuracy", f"{accuracy:.2f}")

                    fig, ax = plt.subplots(figsize=(6, 4))
                    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
                    ax.set_title("Confusion Matrix")
                    ax.set_xlabel("Predicted Label")
                    ax.set_ylabel("True Label")
                    st.pyplot(fig)

        if st.session_state.model is not None and st.session_state.X_test is not None:
            st.header("Feature Importance (SHAP)")
            if st.button("Show SHAP Plot"):
                with st.spinner("Calculating SHAP values..."):
                    # For tree-based models (RandomForest), use TreeExplainer
                    if isinstance(st.session_state.model, RandomForestClassifier):
                        explainer = shap.TreeExplainer(st.session_state.model)
                    # For other models (like SVM), use KernelExplainer (slower)
                    elif isinstance(st.session_state.model, SVC):
                        # KernelExplainer requires a background dataset
                        # For simplicity, we'll use a subset of X_test
                        # Also, SVC doesn't have predict_proba by default for KernelExplainer
                        # We might need to train SVC with probability=True
                        if hasattr(st.session_state.model, 'predict_proba'):
                            explainer = shap.KernelExplainer(st.session_state.model.predict_proba, st.session_state.X_test.iloc[:50])
                        else:
                            st.warning("SVM model not trained with probability estimates. SHAP values cannot be calculated.")
                            explainer = None
                    else:
                        explainer = None
                        st.warning("SHAP not supported for this model type yet.")

                    if explainer is not None:
                        shap_values = explainer.shap_values(st.session_state.X_test)
                        
                        # Create a figure and axes for the plot
                        fig, ax = plt.subplots(figsize=(10, 6))

                        # If it's a multi-class classification, shap_values will be a list of arrays
                        # or a 3D numpy array (n_samples, n_features, n_classes)
                        if isinstance(shap_values, list):
                            # For multi-class, plot the SHAP values for the first class
                            if len(shap_values) > 0 and shap_values[0].shape[0] > 0:
                                shap.summary_plot(shap_values[0], st.session_state.X_test, show=False)
                                st.pyplot(fig)
                            else:
                                st.warning("SHAP values for the first class are empty. Cannot plot.")
                        elif isinstance(shap_values, np.ndarray) and shap_values.ndim == 3:
                            # If it's a 3D array (n_samples, n_features, n_classes), plot for the first class
                            if shap_values.shape[2] > 0 and shap_values.shape[0] > 0:
                                shap.summary_plot(shap_values[:, :, 0], st.session_state.X_test, show=False)
                                st.pyplot(fig)
                            else:
                                st.warning("SHAP values array is empty or has no classes. Cannot plot.")
                        elif isinstance(shap_values, np.ndarray) and shap_values.ndim == 2:
                            # Binary classification case
                            if shap_values.shape[0] > 0:
                                shap.summary_plot(shap_values, st.session_state.X_test, show=False)
                                st.pyplot(fig)
                            else:
                                st.warning("SHAP values array is empty. Cannot plot.")
                        else:
                            st.warning("Unsupported SHAP values format. Cannot plot.")
