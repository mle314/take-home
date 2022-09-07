"""
Create repeatable model training and gridsearch pipelines.
"""
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


def create_preprocessor(numeric, categorical):
    """Create a repeatable data preprocessor for numerical and categorical
    features.

    :param numeric: A list of numerical features
    :param categorical: A list of categorical features
    :return: A column transformer for numerical and categorical features
    """
    numeric_transformer = Pipeline(
        steps=[("imputer", SimpleImputer(missing_values=np.nan, strategy="median"))]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric),
            ("cat", categorical_transformer, categorical),
        ]
    )
    return preprocessor


def build_logistic_regression_pipeline(numeric, categorical, seed=42, metric="roc_auc"):
    """Creates a reproducible logistic regression modeling pipeline for
    hyperparameter tuning.

    :param categorical: A list of categorical feature names
    :param numeric: A list of numeric feature names
    :param seed: A random seed
    :param metric: A metric used of optimizing the hyperparameters
    :return: A logistic regression grid search pipeline
    """
    data_preprocessor = create_preprocessor(numeric, categorical)
    param_grid = {
        "lr__solver": ["newton-cg", "lbfgs", "liblinear"],
        "lr__penalty": ["none", "l1", "l2", "elasticnet"],
        "lr__C": [1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100],
    }

    lr_pipe = Pipeline(
        steps=[
            ("preprocessor", data_preprocessor),
            ("lr", LogisticRegression(random_state=seed)),
        ]
    )

    lr_grid = GridSearchCV(lr_pipe, param_grid, scoring=metric)

    return lr_grid


def build_random_forest_pipeline(numeric, categorical, seed=42, metric="roc_auc"):
    """Creates a reproducible random forest modeling pipeline for
    hyperparameter tuning.

    :param numeric: A list of numeric feature names
    :param categorical: A list of categorical feature names
    :param seed: A random seed
    :param metric: A metric used of optimizing the hyperparameters
    :return: A random forest grid search pipeline
    """
    data_preprocessor = create_preprocessor(numeric, categorical)
    param_grid = {
        "rf__n_estimators": [200, 500],
        "rf__max_features": ["auto", "sqrt", "log2"],
        "rf__max_depth": [4, 5, 6, 7, 8],
        "rf__criterion": ["gini", "entropy"],
    }

    clf_pipe = Pipeline(
        steps=[
            ("preprocessor", data_preprocessor),
            ("rf", RandomForestClassifier(random_state=seed)),
        ]
    )

    rf_grid = GridSearchCV(clf_pipe, param_grid, scoring=metric)

    return rf_grid
