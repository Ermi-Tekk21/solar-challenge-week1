import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set page title and layout
st.set_page_config(page_title="Solar Data Dashboard", layout="wide")
st.title("Solar Data Dashboard")
st.markdown("""
This dashboard visualizes solar data insights for Benin, Sierra Leone, and Togo.
Use the controls below to explore the data interactively.
""")

# Load data
@st.cache_data
def load_data(country):
    return pd.read_csv(f'data/{country.lower()}_clean.csv')

# Sidebar for user inputs
st.sidebar.header("Dashboard Controls")
countries = ['Benin', 'Sierra Leone', 'Togo']
selected_countries = st.sidebar.multiselect(
    "Select Countries", countries, default=countries
)
metric = st.sidebar.selectbox(
    "Select Metric to Visualize", ['GHI', 'DNI', 'DHI']
)

# Load and combine data based on selected countries
if selected_countries:
    dfs = []
    for country in selected_countries:
        df = load_data(country)
        df['Country'] = country
        dfs.append(df)
    combined = pd.concat(dfs, ignore_index=True)

    # Main content
    st.header("Data Visualizations")

    # Boxplot
    st.subheader(f"{metric} Comparison Across Selected Countries")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='Country', y=metric, data=combined, palette='Set2', ax=ax)
    ax.set_title(f'{metric} Comparison')
    ax.set_xlabel('Country')
    ax.set_ylabel(f'{metric} (W/m^2)')
    st.pyplot(fig)

    # Summary Table
    st.subheader("Summary Statistics")
    summary = combined.groupby('Country')[[metric]].agg(['mean', 'median', 'std']).round(2)
    summary.columns = [f'{metric}_mean', f'{metric}_median', f'{metric}_std']
    st.write(summary)

    # Additional Interactive Feature: Filter by GHI Range
    st.subheader("Filter Data by GHI Range")
    ghi_min, ghi_max = st.slider(
        "Select GHI Range",
        float(combined['GHI'].min()),
        float(combined['GHI'].max()),
        (float(combined['GHI'].min()), float(combined['GHI'].max()))
    )
    filtered_data = combined[(combined['GHI'] >= ghi_min) & (combined['GHI'] <= ghi_max)]
    st.write(f"Filtered Data (GHI between {ghi_min} and {ghi_max}):")
    st.write(filtered_data.head())

else:
    st.warning("Please select at least one country to display the visualizations.")