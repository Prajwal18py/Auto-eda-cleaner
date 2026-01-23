import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.ensemble import IsolationForest


# ------------------ Missing Values ------------------ #

def handle_missing_values(df, strategy="drop", fill_value=None):
    df = df.copy()

    if strategy == "drop":
        return df.dropna()

    if strategy in ["fill_mean", "fill_median"]:
        numeric_cols = df.select_dtypes(include=np.number).columns
        imputer = SimpleImputer(
            strategy="mean" if strategy == "fill_mean" else "median"
        )
        df[numeric_cols] = imputer.fit_transform(df[numeric_cols])

    elif strategy == "fill_mode":
        imputer = SimpleImputer(strategy="most_frequent")
        df[:] = imputer.fit_transform(df)

    elif strategy == "fill_value" and fill_value is not None:
        df.fillna(fill_value, inplace=True)

    return df


# ------------------ Duplicates ------------------ #

def remove_duplicates(df):
    return df.drop_duplicates()


# ------------------ Outliers ------------------ #

def detect_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = df[(df[column] < lower) | (df[column] > upper)]
    return outliers, lower, upper


def detect_outliers_isolation_forest(df, column, contamination=0.1):
    model = IsolationForest(contamination=contamination, random_state=42)
    preds = model.fit_predict(df[[column]])
    return df[preds == -1]


def remove_outliers(df, column, method="IQR"):
    if method == "IQR":
        outliers, low, high = detect_outliers_iqr(df, column)
        return df[(df[column] >= low) & (df[column] <= high)].copy(), len(outliers)

    if method == "isolation_forest":
        outliers = detect_outliers_isolation_forest(df, column)
        return df.drop(outliers.index).copy(), len(outliers)

    return df, 0


# ------------------ Scaling ------------------ #

def scale_features(df, columns, method="standard"):
    df = df.copy()

    scaler = StandardScaler() if method == "standard" else MinMaxScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df


# ------------------ Encoding ------------------ #

def encode_categorical(df, columns, method="label"):
    df = df.copy()

    if method == "label":
        for col in columns:
            le = LabelEncoder()
            df.loc[:, col] = le.fit_transform(df[col].astype(str))

    elif method == "onehot":
        df = pd.get_dummies(df, columns=columns, drop_first=True)

    return df


# ------------------ Auto Clean ------------------ #

def auto_clean_data(df):
    # Create a clean copy
    df = df.copy()
    
    # Remove duplicates
    df = remove_duplicates(df)

    # Get column types
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    # Handle numeric columns
    if num_cols:
        imputer = SimpleImputer(strategy="median")
        df[num_cols] = imputer.fit_transform(df[num_cols])

    # Handle categorical columns
    if cat_cols:
        imputer = SimpleImputer(strategy="most_frequent")
        df[cat_cols] = imputer.fit_transform(df[cat_cols])

    return df
                                



        