import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Stroke Analysis",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("🏥 Stroke Analysis Dashboard")
st.markdown("Analyze stroke data from IHME-GBD 2023 Dataset (2013-2023)")

# Load data directly from CSV file
@st.cache_data
def load_data():
    """Load the CSV file directly"""
    try:
        df = pd.read_csv('IHME-GBD_2023_DATA_53bc0df1-1.csv')
        return df
    except FileNotFoundError:
        st.error("❌ CSV file not found. Make sure 'IHME-GBD_2023_DATA_53bc0df1-1.csv' is in the same directory.")
        return None

# Load the data
df = load_data()

if df is not None:
    # Display success message
    st.success(f"✅ Data loaded successfully from IHME-GBD_2023_DATA_53bc0df1-1.csv")
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Data", "📋 Statistics", "🔍 Details"])
    
    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", len(df))
        with col2:
            st.metric("Columns", len(df.columns))
        with col3:
            st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
        
        st.subheader("Column Information")
        st.dataframe(
            pd.DataFrame({
                'Column': df.columns,
                'Type': df.dtypes,
                'Non-Null Count': df.count(),
                'Missing': df.isnull().sum()
            }),
            use_container_width=True
        )
    
    with tab2:
        st.subheader("Dataset Preview")
        rows = st.slider("Number of rows to display", 5, min(100, len(df)), 10)
        st.dataframe(df.head(rows), use_container_width=True)
    
    with tab3:
        st.subheader("Statistical Summary")
        st.dataframe(df.describe(), use_container_width=True)
    
    with tab4:
        st.subheader("Missing Data Analysis")
        missing_data = pd.DataFrame({
            'Column': df.columns,
            'Missing Count': df.isnull().sum(),
            'Missing Percentage': (df.isnull().sum() / len(df) * 100).round(2)
        })
        missing_data = missing_data[missing_data['Missing Count'] > 0].sort_values('Missing Count', ascending=False)
        
        if len(missing_data) > 0:
            st.dataframe(missing_data, use_container_width=True)
        else:
            st.success("✅ No missing data found!")

else:
    st.error("Unable to load data. Please ensure the CSV file is available.")
