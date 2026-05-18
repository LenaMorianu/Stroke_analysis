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
st.title("Stroke Analysis Dashboard")
st.markdown("Analyze stroke data from IHME-GBD 2023 Dataset (2013-2023)")

# Load data directly from CSV file
@st.cache_data
def load_data():
    """Load the CSV file and filter by age groups"""
    try:
        df = pd.read_csv('IHME-GBD_2023_DATA-53bc0df1-1.csv')
        
        # Define age groups to filter
        age_groups = [
            '0-14 years',
            '15-19 years',
            '20-24 years',
            '25-29 years',
            '30-34 years',
            '35-39 years',
            '40-44 years',
            '45-49 years',
            '50-54 years',
            '55-59 years',
            '60-64 years',
            '65-69 years',
            '70-74 years',
            '75-79 years',
            '80-84 years',
            '85+ years'
        ]
        
        # Filter dataframe by age_name column
        if 'age_name' in df.columns:
            df = df[df['age_name'].isin(age_groups)].copy()
            # st.info(f"✅ Filtered data by {len(age_groups)} age groups")
        else:
            st.warning("⚠️ 'age_name' column not found in CSV. Loading all data.")
        
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
    # Separate dataframes: Global and Non-Global
    df_global = df[df['location_name'] == 'Global'].copy()
    df_non_global = df[df['location_name'] != 'Global'].copy()
    
    # Display success message
    # st.success(f"✅ Data loaded successfully from IHME-GBD_2023_DATA_53bc0df1-1.csv")
    # st.info(f"📊 Global records: {len(df_global)} | 🌍 Regional records: {len(df_non_global)}")
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Data", "📋 Statistics"])
    
    with tab1:
        st.markdown("### 🎯 Stroke Burden Analysis: Where is it highest and where is it increasing?")
        
        # Create subtabs for Global vs Regional analysis
        overview_tab1, overview_tab2 = st.tabs(["🌐 Global Analysis", "🌍 Regional Analysis (Non-Global)"])
        
        # ==================== GLOBAL ANALYSIS ====================
        with overview_tab1:
            st.markdown("#### Global Stroke Burden Analysis")
            
            if len(df_global) > 0:
                region_col = 'location_name'
                year_col = 'year'
                val_col = 'val'
                
                # Group by year for global data
                global_data = df_global.groupby(year_col)[val_col].sum().reset_index()
                
                # Display KPIs for Global
                st.subheader("📊 Global Key Performance Indicators")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    total_global_deaths = df_global[val_col].sum()
                    st.metric("Total Global Deaths", f"{total_global_deaths:,.0f}")
                
                with col2:
                    min_year = df_global[year_col].min()
                    max_year = df_global[year_col].max()
                    st.metric("Year Range", f"{int(min_year)}-{int(max_year)}")
                
                with col3:
                    avg_deaths = df_global[val_col].mean()
                    st.metric("Average Deaths/Record", f"{avg_deaths:,.0f}")
                
                with col4:
                    year_span = max_year - min_year
                    if year_span > 0 and len(global_data) >= 2:
                        first_year_deaths = global_data[val_col].iloc[0]
                        last_year_deaths = global_data[val_col].iloc[-1]
                        global_cagr = calculate_cagr(first_year_deaths, last_year_deaths, year_span)
                        st.metric("Global CAGR %", f"{global_cagr:.2f}%")
                
                # Global Trend Over Time
                st.subheader("📈 Global Stroke Burden Trend Over Time")
                fig_global = px.line(
                    global_data,
                    x=year_col,
                    y=val_col,
                    markers=True,
                    title="Global Stroke Deaths by Year",
                    labels={year_col: 'Year', val_col: 'Deaths'}
                )
                fig_global.update_layout(height=400, hovermode='x unified')
                st.plotly_chart(fig_global, use_container_width=True)
                
                # Global Statistics by Age and Sex
                if 'age_name' in df_global.columns and 'sex_name' in df_global.columns:
                    st.subheader("📊 Global Distribution by Age and Sex")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        age_data = df_global.groupby('age_name')[val_col].sum().sort_values(ascending=False).head(10)
                        fig_age = px.bar(
                            age_data.reset_index(),
                            x=val_col,
                            y='age_name',
                            orientation='h',
                            title="Top 10 Age Groups by Deaths",
                            labels={val_col: 'Deaths', 'age_name': 'Age Group'}
                        )
                        st.plotly_chart(fig_age, use_container_width=True)
                    
                    with col2:
                        sex_data = df_global.groupby('sex_name')[val_col].sum().reset_index()
                        fig_sex = px.pie(
                            sex_data,
                            values=val_col,
                            names='sex_name',
                            title="Global Deaths by Sex"
                        )
                        st.plotly_chart(fig_sex, use_container_width=True)
            else:
                st.warning("⚠️ No Global data found in dataset.")
        
        # ==================== REGIONAL ANALYSIS (NON-GLOBAL) ====================
        with overview_tab2:
            st.markdown("#### Regional Stroke Burden Analysis (Excluding Global)")
            
            if len(df_non_global) > 0:
                region_col = 'location_name'
                year_col = 'year'
                val_col = 'val'
                
                # Group by region and year
                regional_data = df_non_global.groupby([region_col, year_col])[val_col].sum().reset_index()
                
                # Calculate total burden by region
                total_burden = df_non_global.groupby(region_col)[val_col].sum().sort_values(ascending=False)
                
                # Display KPIs
                st.subheader("📊 Regional Key Performance Indicators")
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    total_deaths = df_non_global[val_col].sum()
                    st.metric("Total Regional Deaths", f"{total_deaths:,.0f}")
                
                with col2:
                    num_regions = df_non_global[region_col].nunique()
                    st.metric("Regions Analyzed", num_regions)
                
                with col3:
                    top_region = total_burden.index[0]
                    top_burden_pct = (total_burden.iloc[0] / total_burden.sum() * 100)
                    st.metric("Top Region Burden %", f"{top_burden_pct:.1f}%")
                
                with col4:
                    min_year = df_non_global[year_col].min()
                    max_year = df_non_global[year_col].max()
                    year_span = max_year - min_year
                    st.metric("Years Analyzed", int(year_span + 1))
                
                with col5:
                    st.metric("Top Region", top_region)
                
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
                        title="Regional Stroke Burden Distribution",
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
                for region in df_non_global[region_col].unique():
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
                            'Years': int(years_diff + 1)
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
                        title="Regional Growth Rate (CAGR)",
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
                top_n = st.slider("Number of top regions to display", 3, min(10, df_non_global[region_col].nunique()), 5)
                top_regions = total_burden.head(top_n).index.tolist()
                
                trend_data = regional_data[regional_data[region_col].isin(top_regions)]
                
                fig_trend = px.line(
                    trend_data,
                    x=year_col,
                    y=val_col,
                    color=region_col,
                    markers=True,
                    title=f"Regional Stroke Burden Trends: Top {top_n} Regions",
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
                    recent_years = sorted(df_non_global[year_col].unique())[-3:]
                    early_years = sorted(df_non_global[year_col].unique())[:3]
                    
                    acceleration_data = []
                    for region in df_non_global[region_col].unique():
                        recent_avg = df_non_global[(df_non_global[region_col] == region) & (df_non_global[year_col].isin(recent_years))][val_col].mean()
                        early_avg = df_non_global[(df_non_global[region_col] == region) & (df_non_global[year_col].isin(early_years))][val_col].mean()
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
                1. **Highest Burden**: {highest_region[region_col]} accounts for {highest_region['Contribution %']:.1f}% of total regional stroke deaths
                2. **Fastest Growing**: {fastest_region['Region']} has the highest growth rate at {fastest_region['CAGR %']:.2f}% CAGR
                3. **Growth Trajectory**: {fastest_region['Region']} grew from {fastest_region['Start Value']:,.0f} to {fastest_region['End Value']:,.0f} deaths
                4. **Slowest Growing**: {slowest_region['Region']} shows a CAGR of {slowest_region['CAGR %']:.2f}%
                5. **Strategic Focus**: Prioritize {highest_region[region_col]} for burden reduction and {fastest_region['Region']} for growth prevention
                """
                st.markdown(insights)
            
            else:
                st.warning("⚠️ No regional data found in dataset.")
    
    with tab2:
        st.subheader("Dataset Preview")
        
        # Option to view all or filtered data
        data_option = st.radio("View:", ["All Data", "Global Only", "Regional Only (Non-Global)"])
        
        if data_option == "Global Only":
            df_view = df_global
        elif data_option == "Regional Only (Non-Global)":
            df_view = df_non_global
        else:
            df_view = df
        
        rows = st.slider("Number of rows to display", 5, min(100, len(df_view)), 10)
        st.dataframe(df_view.head(rows), use_container_width=True)
    
    with tab3:
        st.subheader("Statistical Summary")
        
        # Option to view statistics
        stat_option = st.radio("Statistics for:", ["All Data", "Global Only", "Regional Only (Non-Global)"])
        
        if stat_option == "Global Only":
            st.dataframe(df_global.describe(), use_container_width=True)
        elif stat_option == "Regional Only (Non-Global)":
            st.dataframe(df_non_global.describe(), use_container_width=True)
        else:
            st.dataframe(df.describe(), use_container_width=True)

else:
    st.error("Unable to load data. Please ensure the CSV file is available.")
