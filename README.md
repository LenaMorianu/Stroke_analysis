
https://stroke-analysis.streamlit.app/

# 🏥 Stroke Analysis 2013-2023

Comprehensive analysis of global and regional stroke burden using IHME-GBD 2023 data, examining trends, growth patterns and geographical disparities in stroke mortality and morbidity.

---

## 📊 Project Overview

This project provides an in-depth analysis of stroke data from 2013 to 2023, leveraging the **IHME-GBD (Institute for Health Metrics and Evaluation - Global Burden of Disease) 2023 dataset**. The analysis progresses from global-level insights to detailed regional breakdowns, identifying hotspots and trends in stroke burden globally.

---

## 📥 Data Source & Characteristics

### Data Imported
- **Dataset**: IHME-GBD 2023 Global Burden of Disease Study
- **File**: `IHME-GBD_2023_DATA-53bc0df1-1.csv` (1.18 MB)
- **Coverage**: Global and regional stroke data spanning 2013-2023

### Data Type
- **Primary Focus**: Stroke-related mortality and morbidity metrics
- **Geographic Scope**: Global aggregate + Country/Regional breakdown
- **Temporal Scope**: 11-year period (2013-2023)

### Data Dimensions
- **Time Period**: 2013-2023 (11 years)
- **Age Groups**: 16 age categories from 0-14 years to 85+ years
- **Sex Categories**: Male and Female breakdown
- **Geographic Coverage**: 195+ countries/regions plus Global aggregate
- **Metrics**: Deaths and Disease burden measurements

### Key Data Attributes
- `location_name`: Geographic location (country/region or "Global")
- `year`: Year of observation (2013-2023)
- `age_name`: Age group classification
- `sex_name`: Sex category (Male/Female)
- `val`: Stroke burden value (deaths/cases)

---

## ❓ Business Questions

The analysis addresses critical public health questions:

1. **Where is stroke burden highest?** - Identifying regions with the greatest stroke mortality and morbidity
2. **Is stroke burden growing or declining?** - Understanding temporal trends in stroke prevalence
3. **Where is stroke burden increasing fastest?** - Detecting regions with accelerating disease burden
4. **Which demographics are most affected?** - Analyzing age and sex distribution of stroke deaths
5. **What is the growth trajectory?** - Calculating and comparing growth rates across regions
6. **Which regions require strategic intervention?** - Prioritizing public health resources

---

## 💡 Summary of Insights

### Global Level
- **Total Global Stroke Deaths (2013-2023)**: Aggregated burden across all recorded observations
- **Global Trend**: Compound Annual Growth Rate (CAGR) calculated to measure overall progression
- **Year Coverage**: Complete data spanning 2013 to 2023 period
- **Age Pattern**: Age groups 65+ represent the majority of stroke deaths
- **Sex Distribution**: Comparative analysis of male vs. female stroke burden

### Regional Level
- **Regional Contribution**: Identification of top burden-bearing regions (percentage contribution analysis)
- **Regional CAGR Rankings**: Growth rates ranked from fastest to slowest growing regions
- **Strategic Priorities**: 
  - **Highest Burden Regions**: Concentrated in high-mortality geographical areas
  - **Fastest Growing Regions**: Early intervention targets showing exponential growth
  - **Growth Acceleration Index**: Recent vs. historical growth comparison to detect acceleration
- **Key Findings**: 
  - Top regions account for significant proportion of global burden
  - Regional growth rates vary dramatically
  - Acceleration patterns identify emerging crisis areas

---

## 🔧 Analysis Methodology

### Architecture: From Global to Regional

#### **Stage 1: Global Summary**
- Load complete IHME-GBD dataset
- Filter by defined age groups (0-14 through 85+ years)
- Aggregate stroke metrics at global level
- Calculate global KPIs and trends

#### **Stage 2: Regional Breakdown**
- Separate global aggregate from individual regions
- Group by location, year, and demographic factors
- Calculate regional contribution percentages
- Identify top burden-bearing regions

#### **Stage 3: Growth Analysis**
- Compute CAGR (Compound Annual Growth Rate) for each region
- Compare start values (2013) vs. end values (2023)
- Rank regions by growth trajectory
- Calculate acceleration rates

#### **Stage 4: Strategic Insights**
- Identify highest burden regions for resource allocation
- Detect fastest-growing regions for preventive intervention
- Analyze growth acceleration patterns
- Provide actionable public health insights

---

## 📈 Key Performance Indicators (KPIs)

### Global KPIs
| KPI | Description |
|-----|-------------|
| **Total Global Deaths** | Sum of all stroke deaths globally over 2013-2023 |
| **Year Range** | Coverage period (2013-2023) |
| **Average Deaths/Record** | Mean stroke deaths per data point |
| **Global CAGR %** | Compound Annual Growth Rate of global stroke burden |

### Regional KPIs
| KPI | Description |
|-----|-------------|
| **Total Regional Deaths** | Combined stroke deaths across all regions (excluding Global) |
| **Regions Analyzed** | Number of countries/regions in dataset |
| **Top Region Burden %** | Percentage of total burden in highest-burden region |
| **Years Analyzed** | Number of years covered per region |
| **Top Region Name** | Identification of highest burden region |

### Growth & Trend KPIs
| KPI | Description |
|-----|-------------|
| **Regional CAGR %** | Growth rate for each region over 2013-2023 |
| **Start Value** | Stroke burden at beginning of period |
| **End Value** | Stroke burden at end of period |
| **Growth Acceleration %** | Comparison of recent years vs. early years growth |

---

## 🛠️ How the Analysis Was Built

### Technology Stack
- **Python 3.x**
- **Streamlit**: Interactive dashboard framework
- **Pandas**: Data manipulation and aggregation
- **NumPy**: Numerical computations
- **Plotly**: Interactive visualizations

### Core Components

#### **1. Data Processing** (`Stroke_analysis.py`)
```
✓ Load CSV with caching for performance
✓ Filter by 16 age groups
✓ Separate global vs. regional data
✓ Handle missing data scenarios
```

#### **2. Metric Calculations**
```
✓ CAGR Calculation: ((End Value / Start Value)^(1/Years) - 1) × 100
✓ Contribution %: (Regional Deaths / Total Deaths) × 100
✓ Growth Acceleration: ((Recent Avg - Early Avg) / Early Avg) × 100
✓ Year-over-year aggregations
```

#### **3. Visualization Pipeline**
- **Global Trends**: Line charts showing temporal progression
- **Regional Burden**: Pie charts with percentage distribution
- **CAGR Comparison**: Horizontal bar charts with color scaling
- **Growth Trends**: Multi-line charts for top regions
- **Demographics**: Age and sex distribution charts

#### **4. Dashboard Structure**
```
📊 Overview Tab
  ├─ 🌐 Global Analysis (KPIs + Trends)
  └─ 🌍 Regional Analysis (Burden + Growth)

📈 Data Tab
  └─ Interactive dataset preview and filtering

📋 Statistics Tab
  └─ Descriptive statistics by segment

🔍 Details Tab
  └─ Missing data analysis and data quality
```

### Analysis Flow
1. **Data Import** → CSV loading with age group filtering
2. **Segmentation** → Global vs. Regional separation
3. **Aggregation** → Group by time, geography, demographics
4. **Calculation** → KPIs, CAGR, growth rates
5. **Visualization** → Interactive charts and tables
6. **Insight Generation** → Strategic priority ranking

---

## 📁 Project Structure

```
LenaMorianu/Stroke_analysis/
├── Stroke_analysis.py              # Main Streamlit dashboard
├── check_columns.py                # Data exploration utility
├── IHME-GBD_2023_DATA-53bc0df1-1.csv  # Dataset (1.18 MB)
├── requirements.txt                # Python dependencies
└── README.md                       # Documentation
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- pip package manager

### Installation
```bash
# Clone the repository
git clone https://github.com/LenaMorianu/Stroke_analysis.git
cd Stroke_analysis

# Install dependencies
pip install -r requirements.txt
```

### Running the Dashboard
```bash
streamlit run Stroke_analysis.py
```

The dashboard will open in your default browser at `http://localhost:8501`

---

## 📊 Dashboard Features

- **Interactive Tabs**: Switch between Overview, Data, Statistics, and Details
- **Sub-tabs**: Separate Global and Regional analysis views
- **Dynamic Filtering**: Adjust number of regions to display in trends
- **Downloadable Data**: View and export analysis tables
- **Real-time Calculations**: CAGR, growth rates, and acceleration metrics
- **Responsive Design**: Wide layout optimized for large screens

---

## 🎯 Strategic Applications

This analysis supports:
- **Public Health Planning**: Prioritize resources to highest-burden regions
- **Disease Prevention**: Identify fastest-growing areas for intervention
- **Research**: Understand stroke epidemiology patterns globally
- **Policy Making**: Data-driven decisions on stroke management strategies
- **Monitoring**: Track progress towards stroke burden reduction targets

---

## 📝 Notes

- Data is filtered to include age groups 0-14 through 85+ years
- Global aggregate is analyzed separately from individual regions/countries
- CAGR calculations include only regions with 2+ years of data
- All values are from the IHME-GBD 2023 official release

---

## 👤 Author
**Lena Morianu**

---

## 📄 License
This project uses data from the IHME Global Burden of Disease Study 2023. Please refer to IHME's terms of use.

---

**Last Updated**: 2026-05-18
