import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
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
        df = pd.read_csv('IHME-GBD_2023_DATA-53bc0df1-1.csv')
        return df
    except FileNotFoundError:
        st.error("❌ CSV file not found. Make sure 'IHME-GBD_2023_DATA_53bc0df1-1.csv' is in the same directory.")
        return None

# Calculate CAGR (Compound Annual Growth Rate)
@st.cache_data
def calculate_cagr(start_value, end_value, num_years):
    """Calculate CAGR between two values"""
    if start_value <= 0 or end_value <= 0:
        return 0
    cagr = (((end_value / start_value) ** (1 / num_years)) - 1) * 100
    return cagr

# Load the data
df = load_data()

if df is not None:
    # Display success message
    st.success(f"✅ Data loaded successfully from IHME-GBD_2023_DATA_53bc0df1-1.csv")
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Data", "📋 Statistics", "🔍 Details"])
    
    with tab1:
        st.markdown("### 🎯 Stroke Burden Analysis: Where is it highest and where is it increasing?")
        
        # Prepare data for regional analysis
        # Assuming the data has columns like 'location', 'year', 'deaths', 'val' (value)
        region_col = 'location' if 'location' in df.columns else None
        year_col = 'year' if 'year' in df.columns else None
        val_col = 'val' if 'val' in df.columns else 'deaths'
        
        if region_col and year_col and val_col:
            # Group by region and year
            regional_data = df.groupby([region_col, year_col])[val_col].sum().reset_index()
            
            # Calculate total burden by region
            total_burden = df.groupby(region_col)[val_col].sum().sort_values(ascending=False)
            
            # Display KPIs
            st.subheader("📊 Key Performance Indicators (KPIs)")
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                total_deaths = df[val_col].sum()
                st.metric("Total Stroke Deaths", f"{total_deaths:,.0f}")
            
            with col2:
                num_regions = df[region_col].nunique()
                st.metric("Regions Analyzed", num_regions)
            
            with col3:
                top_region = total_burden.index[0]
                top_burden_pct = (total_burden.iloc[0] / total_burden.sum() * 100)
                st.metric("Top Region Burden %", f"{top_burden_pct:.1f}%")
            
            with col4:
                min_year = df[year_col].min()
                max_year = df[year_col].max()
                year_span = max_year - min_year
                st.metric("Years Analyzed", year_span + 1)
            
            with col5:
                growth_factor = total_burden.sum()
                st.metric("Total Regions", num_regions)
            
            # Regional contribution breakdown
            st.subheader("🌍 Regional Contribution Analysis")
            
            col1, col2 = st.columns([1.5, 1])
            
            with col1:
                # Calculate regional contribution %
                regional_contribution = total_burden.reset_index()
                regional_contribution.columns = [region_col, 'Total Deaths']
                regional_contribution['Contribution %'] = (regional_contribution['Total Deaths'] / regional_contribution['Total Deaths'].sum() * 100).round(2)
                regional_contribution = regional_contribution.sort_values('Total Deaths', ascending=False)
                
                # Create pie chart
                fig_pie = go.Figure(data=[go.Pie(
                    labels=regional_contribution[region_col],
                    values=regional_contribution['Total Deaths'],
                    textposition='inside',
                    textinfo='label+percent'
                )])
                fig_pie.update_layout(
                    title="Stroke Burden Distribution by Region",
                    height=400,
                    showlegend=True
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Display regional contribution table
                st.dataframe(
                    regional_contribution[[region_col, 'Total Deaths', 'Contribution %']],
                    use_container_width=True,
                    hide_index=True
                )
            
            # CAGR and Growth Analysis
            st.subheader("📈 Growth Analysis (CAGR by Region)")
            
            # Calculate CAGR for each region
            cagr_data = []
            for region in df[region_col].unique():
                region_df = regional_data[regional_data[region_col] == region].sort_values(year_col)
                if len(region_df) >= 2:
                    start_val = region_df[val_col].iloc[0]
                    end_val = region_df[val_col].iloc[-1]
                    years_diff = region_df[year_col].iloc[-1] - region_df[year_col].iloc[0]
                    cagr = calculate_cagr(start_val, end_val, years_diff)
                    cagr_data.append({
                        'Region': region,
                        'Start Value': start_val,
                        'End Value': end_val,
                        'CAGR %': cagr,
                        'Years': years_diff + 1
                    })
            
            cagr_df = pd.DataFrame(cagr_data).sort_values('CAGR %', ascending=False)
            
            col1, col2 = st.columns([1, 1.5])
            
            with col1:
                # CAGR Bar chart
                fig_cagr = px.bar(
                    cagr_df,
                    x='CAGR %',
                    y='Region',
                    orientation='h',
                    color='CAGR %',
                    color_continuous_scale='RdYlGn_r',
                    title="Growth Rate (CAGR) by Region",
                    labels={'CAGR %': 'CAGR (%)'}
                )
                fig_cagr.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig_cagr, use_container_width=True)
            
            with col2:
                # CAGR Table
                st.dataframe(
                    cagr_df[['Region', 'CAGR %', 'Start Value', 'End Value', 'Years']],
                    use_container_width=True,
                    hide_index=True
                )
            
            # Trend Analysis
            st.subheader("📊 Trend Lines by Region")
            
            # Select top regions for trend visualization
            top_n = st.slider("Number of top regions to display", 3, min(10, df[region_col].nunique()), 5)
            top_regions = total_burden.head(top_n).index.tolist()
            
            trend_data = regional_data[regional_data[region_col].isin(top_regions)]
            
            fig_trend = px.line(
                trend_data,
                x=year_col,
                y=val_col,
                color=region_col,
                markers=True,
                title=f"Stroke Burden Trends: Top {top_n} Regions",
                labels={year_col: 'Year', val_col: 'Deaths'}
            )
            fig_trend.update_layout(height=400, hovermode='x unified')
            st.plotly_chart(fig_trend, use_container_width=True)
            
            # Regional Ranking and Strategic Priorities
            st.subheader("🎯 Strategic Priorities")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Highest Burden Regions**")
                highest_burden = regional_contribution.head(5)
                for idx, row in highest_burden.iterrows():
                    st.markdown(f"• {row[region_col]}: {row['Contribution %']:.1f}%")
            
            with col2:
                st.markdown("**Fastest Growing Regions (CAGR)**")
                fastest_growing = cagr_df.head(5)
                for idx, row in fastest_growing.iterrows():
                    st.markdown(f"• {row['Region']}: +{row['CAGR %']:.2f}%")
            
            with col3:
                st.markdown("**Growth Acceleration Index**")
                # Calculate acceleration: compare recent years vs early years
                recent_years = sorted(df[year_col].unique())[-3:]
                early_years = sorted(df[year_col].unique())[:3]
                
                acceleration_data = []
                for region in df[region_col].unique():
                    recent_avg = df[(df[region_col] == region) & (df[year_col].isin(recent_years))][val_col].mean()
                    early_avg = df[(df[region_col] == region) & (df[year_col].isin(early_years))][val_col].mean()
                    if early_avg > 0:
                        acceleration = ((recent_avg - early_avg) / early_avg * 100)
                        acceleration_data.append({'Region': region, 'Acceleration %': acceleration})
                
                acceleration_df = pd.DataFrame(acceleration_data).sort_values('Acceleration %', ascending=False)
                accel_top = acceleration_df.head(5)
                for idx, row in accel_top.iterrows():
                    st.markdown(f"• {row['Region']}: {row['Acceleration %']:.1f}%")
            
            # Summary Insights
            st.subheader("💡 Key Insights")
            
            highest_region = regional_contribution.iloc[0]
            fastest_region = cagr_df.iloc[0]
            slowest_region = cagr_df.iloc[-1]
            
            insights = f"""
            1. **Highest Burden**: {highest_region[region_col]} accounts for {highest_region['Contribution %']:.1f}% of total stroke deaths
            2. **Fastest Growing**: {fastest_region['Region']} has the highest growth rate at {fastest_region['CAGR %']:.2f}% CAGR
            3. **Growth Trajectory**: {fastest_region['Region']} grew from {fastest_region['Start Value']:,.0f} to {fastest_region['End Value']:,.0f} deaths
            4. **Slowest Growing**: {slowest_region['Region']} shows a CAGR of {slowest_region['CAGR %']:.2f}%
            5. **Strategic Focus**: Prioritize {highest_region[region_col]} for burden reduction and {fastest_region['Region']} for growth prevention
            """
            st.markdown(insights)
        
        else:
            st.warning("⚠️ Required columns (location, year, or value columns) not found in dataset. Please check data structure.")
    
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
