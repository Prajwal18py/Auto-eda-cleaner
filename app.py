import streamlit as st
import pandas as pd
import numpy as np

from utils.data_cleaner import (
    handle_missing_values,
    remove_duplicates,
    remove_outliers,
    auto_clean_data
)

from utils.eda_functions import (
    get_basic_stats,
    get_column_info,
    get_missing_values_summary,
    distribution_plot,
    box_plot,
    correlation_heatmap,
    count_plot
)

st.set_page_config("Auto EDA & Cleaner", "📊", layout="wide")
st.title("📊 Auto EDA & Data Cleaning Tool")

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    # Load data
    if "original_df" not in st.session_state:
        df = pd.read_csv(uploaded_file)
        st.session_state.original_df = df.copy()
        st.session_state.df = df.copy()
    
    # Use session state data
    df = st.session_state.df
    
    # Show metrics in sidebar
    st.sidebar.success("✅ File uploaded!")
    st.sidebar.metric("Rows", df.shape[0])
    st.sidebar.metric("Columns", df.shape[1])
    st.sidebar.metric("Missing", df.isna().sum().sum())

    tab1, tab2, tab3, tab4 = st.tabs(["📋 Overview", "🧹 Cleaning", "📊 EDA", "💾 Download"])

    # -------- TAB 1: Overview -------- #
    with tab1:
        st.subheader("Dataset Preview")
        st.dataframe(df.head(10))
        
        st.subheader("Column Information")
        st.dataframe(get_column_info(df))

        missing = get_missing_values_summary(df)
        if not missing.empty:
            st.subheader("Missing Values Summary")
            st.dataframe(missing)
        else:
            st.success("✅ No missing values!")

    # -------- TAB 2: Cleaning -------- #
    with tab2:
        st.header("Data Cleaning")
        
        # Quick Auto Clean
        st.subheader("⚡ Quick Auto-Clean")
        st.info("Remove duplicates + Fill missing values intelligently")
        if st.button("🚀 Auto Clean"):
            st.session_state.df = auto_clean_data(st.session_state.df)
            st.success("✅ Auto cleaning completed!")
            st.rerun()
        
        st.divider()
        
        # Manual cleaning
        st.subheader("Manual Cleaning Options")
        
        # Missing values
        strategy = st.selectbox(
            "1. Missing Value Strategy",
            ["None", "drop", "fill_mean", "fill_median", "fill_mode"]
        )

        if st.button("Apply Missing Value Strategy"):
            if strategy == "None":
                st.warning("⚠️ Please select a strategy")
            else:
                st.session_state.df = handle_missing_values(st.session_state.df, strategy)
                st.success(f"✅ Applied {strategy} strategy!")
                st.rerun()
        
        # Duplicates
        st.write("2. Remove Duplicates")
        dup_count = df.duplicated().sum()
        st.info(f"Found {dup_count} duplicate rows")
        
        if st.button("Remove Duplicates"):
            st.session_state.df = remove_duplicates(st.session_state.df)
            st.success(f"✅ Removed {dup_count} duplicates!")
            st.rerun()
        
        # Outliers
        st.write("3. Remove Outliers")
        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        
        if num_cols:
            col1, col2 = st.columns(2)
            with col1:
                outlier_col = st.selectbox("Select column", num_cols)
            with col2:
                outlier_method = st.selectbox("Method", ["IQR", "isolation_forest"])
            
            if st.button("Remove Outliers"):
                cleaned_df, count = remove_outliers(st.session_state.df, outlier_col, outlier_method)
                st.session_state.df = cleaned_df
                st.success(f"✅ Removed {count} outliers from '{outlier_col}'!")
                st.rerun()
        else:
            st.info("No numeric columns for outlier removal")
        
        st.divider()
        
        # Preview current data
        st.subheader("Current Data Preview")
        st.dataframe(df.head())
        st.info(f"Current: {df.shape[0]} rows × {df.shape[1]} columns")
        
        # Reset button
        if st.button("🔄 Reset to Original Data"):
            st.session_state.df = st.session_state.original_df.copy()
            st.success("✅ Data reset!")
            st.rerun()

    # -------- TAB 3: EDA -------- #
    with tab3:
        st.header("Exploratory Data Analysis")
        
        st.subheader("Statistical Summary")
        st.dataframe(get_basic_stats(df))

        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
        
        if num_cols:
            st.subheader("Numeric Column Visualization")
            col = st.selectbox("Select numeric column", num_cols)
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(distribution_plot(df, col), use_container_width=True)
            with col2:
                st.plotly_chart(box_plot(df, col), use_container_width=True)

            if len(num_cols) >= 2:
                st.subheader("Correlation Heatmap")
                heatmap = correlation_heatmap(df)
                if heatmap:
                    st.plotly_chart(heatmap, use_container_width=True)
        
        if cat_cols:
            st.subheader("Categorical Column Visualization")
            cat_col = st.selectbox("Select categorical column", cat_cols)
            top_n = st.slider("Top N values", 5, 20, 10)
            st.plotly_chart(count_plot(df, cat_col, top_n), use_container_width=True)

    # -------- TAB 4: Download -------- #
    with tab4:
        st.header("Download Cleaned Data")
        
        st.subheader("Preview")
        st.dataframe(df.head(10))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Original Rows", st.session_state.original_df.shape[0])
        with col2:
            st.metric("Current Rows", df.shape[0])
        with col3:
            removed = st.session_state.original_df.shape[0] - df.shape[0]
            st.metric("Rows Removed", removed)
        
        csv = df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="📥 Download Cleaned CSV",
            data=csv,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )
        
        st.success("✅ Click above to download!")

else:
    # Landing page
    st.info("👈 Upload a CSV file from the sidebar to begin!")
    
    st.markdown("""
    ### 🚀 Features:
    - **Auto-Clean**: One-click data cleaning
    - **Manual Cleaning**: Handle missing values, duplicates, outliers
    - **EDA**: Statistical analysis and visualizations
    - **Download**: Export cleaned data
    
    ### 🛠️ Tech Stack:
    - Python, Streamlit, Pandas
    - Scikit-learn, Plotly, NumPy
    
    ### 📊 Outlier Detection:
    - IQR (Interquartile Range)
    - Isolation Forest (ML-based)
    """)