import pandas as pd
import numpy as np
import plotly.express as px


def get_basic_stats(df):
    return df.describe()


def get_column_info(df):
    return pd.DataFrame({
        "Column": df.columns.tolist(),
        "Data Type": [str(dtype) for dtype in df.dtypes],
        "Non-Null Count": df.count().tolist(),
        "Unique Values": df.nunique().tolist()
    })


def get_missing_values_summary(df):
    missing_count = df.isna().sum()
    missing_pct = (missing_count / len(df) * 100).round(2)
    
    result = pd.DataFrame({
        "Column": df.columns.tolist(),
        "Missing Count": missing_count.tolist(),
        "Missing %": missing_pct.tolist()
    })
    
    return result[result["Missing Count"] > 0]


def distribution_plot(df, column):
    return px.histogram(df, x=column, nbins=30, title=f"Distribution of {column}")


def box_plot(df, column):
    return px.box(df, y=column, title=f"Box Plot of {column}")


def correlation_heatmap(df):
    num_df = df.select_dtypes(include=np.number)
    if num_df.shape[1] < 2:
        return None
    return px.imshow(num_df.corr(), text_auto=True, title="Correlation Heatmap", 
                     color_continuous_scale='RdBu_r')


def count_plot(df, column, top_n=10):
    vc = df[column].value_counts().head(top_n)
    return px.bar(x=vc.index, y=vc.values, 
                  labels={"x": column, "y": "Count"},
                  title=f"Top {top_n} values in {column}")