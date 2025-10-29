import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix
import shap
import streamlit as st

def train_model(df, labels_df, numerical_cols, model_type, imputation_strategy):
    """
    Trains a machine learning model with improved data handling and user feedback.
    """
    merged_df = pd.merge(df, labels_df, on="id")
    X = merged_df[numerical_cols]
    y = merged_df["label"]

    imputation_map = {
        "Fill with 0": 0,
        "Fill with Mean": X.mean(),
        "Fill with Median": X.median(),
    }
    if imputation_strategy in imputation_map:
        X = X.fillna(imputation_map[imputation_strategy])
    elif imputation_strategy == "Drop rows":
        original_rows = len(X)
        X = X.dropna()
        y = y.loc[X.index]
        if len(X) < original_rows:
            st.info(f"Dropped {original_rows - len(X)} rows with missing values.")

    if len(X) < 10:
        st.warning("Dataset too small for a meaningful train/test split.")
        return None, None, None, None, None, None, None

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model_factory = {
        "RandomForest": RandomForestClassifier(random_state=42),
        "SVM": SVC(random_state=42, probability=True),
    }
    model = model_factory.get(model_type)

    if model:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)
        return model, X_train, X_test, y_train, y_test, accuracy, cm
    return None, None, None, None, None, None, None

def calculate_shap_values(model, X_test):
    """
    Calculates SHAP values with a progress bar for long computations,
    especially for SVM's KernelExplainer.
    """
    st.info("Calculating SHAP values... This may take a while.")
    progress_bar = st.progress(0)

    try:
        if isinstance(model, RandomForestClassifier):
            explainer = shap.TreeExplainer(model)
        elif isinstance(model, SVC) and hasattr(model, "predict_proba"):
            # Use a smaller subset for the background data to speed up KernelExplainer
            background_data = shap.sample(X_test, 50)
            explainer = shap.KernelExplainer(model.predict_proba, background_data)
        else:
            st.warning("SHAP analysis is not supported for this model type or configuration.")
            return None
        
        # This is a simplified progress update. For more granular control,
        # one might need to hook into the explainer's internals if possible.
        progress_bar.progress(50)
        shap_values = explainer.shap_values(X_test)
        progress_bar.progress(100)
        return shap_values

    except Exception as e:
        st.error(f"An error occurred during SHAP value calculation: {e}")
        return None
    finally:
        progress_bar.empty()
