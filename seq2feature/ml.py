import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix
import shap
import streamlit as st


def train_model(df, labels_df, numerical_cols, model_type, imputation_strategy):
    """
    Trains a machine learning model.

    Args:
        df (pd.DataFrame): The dataframe with features.
        labels_df (pd.DataFrame): The dataframe with labels.
        numerical_cols (list): The list of numerical columns.
        model_type (str): The type of model to train ('RandomForest' or 'SVM').
        imputation_strategy (str): Strategy for handling missing values.

    Returns:
        tuple: A tuple containing the trained model, X_train, X_test, y_train, y_test, accuracy, and confusion matrix.
    """
    merged_df = pd.merge(df, labels_df, on="id")

    X = merged_df[numerical_cols]
    y = merged_df["label"]

    if imputation_strategy == "Fill with 0":
        X = X.fillna(0)
    elif imputation_strategy == "Fill with Mean":
        X = X.fillna(X.mean())
    elif imputation_strategy == "Fill with Median":
        X = X.fillna(X.median())
    elif imputation_strategy == "Drop rows":
        original_rows = len(X)
        X = X.dropna()
        y = y.loc[X.index]  # Ensure y aligns with X after dropping rows
        if len(X) < original_rows:
            st.info(f"Dropped {original_rows - len(X)} rows due to missing values.")

    if len(X) < 5:
        st.warning(
            "The dataset is too small for a meaningful train/test split and accuracy score after imputation."
        )
        return None, None, None, None, None, None, None

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    if model_type == "RandomForest":
        model = RandomForestClassifier(random_state=42)
    else:
        model = SVC(random_state=42, probability=True)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    return model, X_train, X_test, y_train, y_test, accuracy, cm


def calculate_shap_values(model, X_test):
    """
    Calculates SHAP values for a given model.

    Args:
        model: The trained model.
        X_test (pd.DataFrame): The test set.

    Returns:
        The SHAP values.
    """
    if isinstance(model, RandomForestClassifier):
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_test)
    elif isinstance(model, SVC):
        st.info(
            "Calculating SHAP values for SVM models using KernelExplainer can be very slow. For faster results, consider using a smaller subset of X_test for SHAP calculation."
        )
        if hasattr(model, "predict_proba"):
            explainer = shap.KernelExplainer(model.predict_proba, X_test.iloc[:20])
            shap_values = explainer.shap_values(X_test.iloc[:100])
        else:
            st.warning(
                "SVM model not trained with probability estimates. SHAP values cannot be calculated."
            )
            shap_values = None
    else:
        st.warning("SHAP not supported for this model type yet.")
        shap_values = None

    return shap_values
