import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
import pandas as pd
import streamlit as st
import shap
import numpy as np


def plot_feature_distribution(df, selected_col):
    """Plots the distribution of a selected feature."""
    fig, ax = plt.subplots()
    df[selected_col].hist(ax=ax)
    ax.set_title(selected_col)
    st.pyplot(fig)


def plot_correlation_matrix(df, numerical_cols):
    """Plots the correlation matrix."""
    corr = df[numerical_cols].corr()
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(
        corr, ax=ax, cmap="viridis", annot=(len(numerical_cols) < 20), fmt=".2f"
    )
    ax.set_title("Feature Correlation Matrix")
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    st.pyplot(fig)


def plot_pca(X_train, X_test, y_train, y_test):
    """Plots the 2D PCA of features, showing train/test split."""
    pca = PCA(n_components=2)
    X_train_pca = pca.fit_transform(X_train)
    X_test_pca = pca.transform(X_test)

    pca_train_df = pd.DataFrame(
        data=X_train_pca, columns=["principal component 1", "principal component 2"]
    )
    pca_train_df["label"] = y_train.values
    pca_train_df["dataset"] = "train"

    pca_test_df = pd.DataFrame(
        data=X_test_pca, columns=["principal component 1", "principal component 2"]
    )
    pca_test_df["label"] = y_test.values
    pca_test_df["dataset"] = "test"

    pca_df = pd.concat([pca_train_df, pca_test_df])

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.scatterplot(
        x="principal component 1",
        y="principal component 2",
        hue="label",
        style="dataset",
        data=pca_df,
        ax=ax,
    )
    ax.set_title("2D PCA of Features (Train/Test Split)")
    st.pyplot(fig)


def plot_confusion_matrix(cm):
    """Plots the confusion matrix."""
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
    ax.set_title("Confusion Matrix")
    ax.set_xlabel("Predicted Label")
    ax.set_ylabel("True Label")
    st.pyplot(fig)


def plot_shap_summary(shap_values, X_test):
    """Plots the SHAP summary plot."""
    fig, ax = plt.subplots(figsize=(10, 6))
    if isinstance(shap_values, list):
        if len(shap_values) > 0 and shap_values[0].shape[0] > 0:
            shap.summary_plot(shap_values[0], X_test, show=False)
            st.pyplot(fig)
        else:
            st.warning("SHAP values for the first class are empty. Cannot plot.")
    elif isinstance(shap_values, np.ndarray) and shap_values.ndim == 3:
        if shap_values.shape[2] > 0 and shap_values.shape[0] > 0:
            shap.summary_plot(shap_values[:, :, 0], X_test, show=False)
            st.pyplot(fig)
        else:
            st.warning("SHAP values array is empty or has no classes. Cannot plot.")
    elif isinstance(shap_values, np.ndarray) and shap_values.ndim == 2:
        if shap_values.shape[0] > 0:
            shap.summary_plot(shap_values, X_test, show=False)
            st.pyplot(fig)
        else:
            st.warning("SHAP values array is empty. Cannot plot.")
    else:
        st.warning("Unsupported SHAP values format. Cannot plot.")
