import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
import pandas as pd
import streamlit as st
import shap
import numpy as np

def plot_feature_distribution(df, selected_col):
    """Plots the distribution of a selected feature with error handling."""
    try:
        fig, ax = plt.subplots()
        df[selected_col].hist(bins=30, ax=ax)
        ax.set_title(f"Distribution of {selected_col}")
        ax.set_xlabel(selected_col)
        ax.set_ylabel("Frequency")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Failed to plot feature distribution: {e}")

def plot_correlation_matrix(df, numerical_cols):
    """Plots an enhanced correlation matrix with error handling."""
    try:
        corr = df[numerical_cols].corr()
        fig, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(
            corr, ax=ax, cmap="viridis", annot=(len(numerical_cols) < 20), fmt=".2f"
        )
        ax.set_title("Feature Correlation Matrix")
        plt.xticks(rotation=45, ha="right")
        plt.yticks(rotation=0)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Failed to plot correlation matrix: {e}")

def plot_pca(X_train, X_test, y_train, y_test):
    """Plots a more informative 2D PCA of features with error handling."""
    try:
        pca = PCA(n_components=2)
        X_train_pca = pca.fit_transform(X_train)
        X_test_pca = pca.transform(X_test)

        pca_df = pd.concat([
            pd.DataFrame(X_train_pca, columns=["PC1", "PC2"], index=y_train.index).assign(label=y_train, dataset="train"),
            pd.DataFrame(X_test_pca, columns=["PC1", "PC2"], index=y_test.index).assign(label=y_test, dataset="test")
        ])

        fig, ax = plt.subplots(figsize=(10, 8))
        sns.scatterplot(x="PC1", y="PC2", hue="label", style="dataset", data=pca_df, ax=ax, alpha=0.7)
        ax.set_title("2D PCA of Features (Train/Test Split)")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Failed to plot PCA: {e}")

def plot_confusion_matrix(cm):
    """Plots a clear and informative confusion matrix with error handling."""
    try:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
        ax.set_title("Confusion Matrix")
        ax.set_xlabel("Predicted Label")
        ax.set_ylabel("True Label")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Failed to plot confusion matrix: {e}")

def plot_shap_summary(shap_values, X_test, model=None):
    """
    Plots a comprehensive SHAP summary plot, handling multi-class outputs
    by allowing class selection.
    """
    try:
        if isinstance(shap_values, list) and model is not None:
            st.info("SHAP values for multi-class classification detected.")
            class_names = getattr(model, 'classes_', [f"Class {i}" for i in range(len(shap_values))])
            selected_class_idx = st.selectbox(
                "Select class to display SHAP values for:",
                range(len(class_names)),
                format_func=lambda x: class_names[x]
            )
            shap.summary_plot(shap_values[selected_class_idx], X_test, show=False)
            fig = plt.gcf()
            st.pyplot(fig)
        elif isinstance(shap_values, np.ndarray):
            shap.summary_plot(shap_values, X_test, show=False)
            fig = plt.gcf()
            st.pyplot(fig)
        else:
            st.warning("Unsupported SHAP values format or model not provided for multi-class case.")
    except Exception as e:
        st.error(f"Failed to plot SHAP summary: {e}")
