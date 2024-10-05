import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='whitegrid')

# Define helper functions
def create_hourly_pollution_df(df):
    hourly_pollution_df = df.resample(rule='H', on='datetime').agg({
        "No": "nunique",
        "PM1.0": "mean",
        "PM2.5": "mean",
        "CO": "mean",
        "NOx": "mean",
        "pollution_score": "mean"
    })
    hourly_pollution_df = hourly_pollution_df.reset_index()
    return hourly_pollution_df

def create_max_pollutants_df(df):
    max_pollutants_df = df.drop('datetime', axis=1)
    max_pollutants_df = max_pollutants_df.apply(pd.to_numeric, errors='coerce')
    max_pollutants_df = max_pollutants_df.max().reset_index()
    max_pollutants_df.columns = ["pollutant", "max_level"]
    return max_pollutants_df

def create_pollutants_by_region_df(df):
    if 'region' in df.columns:
        pollutants_by_region_df = df.groupby("region").mean(numeric_only=True).reset_index()
    else:
        pollutants_by_region_df = None
    return pollutants_by_region_df

# Load data
try:
    air_quality_df = pd.read_csv('/mnt/data/All Data.csv')
except FileNotFoundError:
    st.error("File not found. Please check the file path.")
    st.stop()

# Ensure datetime columns are in datetime format
air_quality_df['datetime'] = pd.to_datetime(air_quality_df['datetime'], errors='coerce')

# Create filters
min_date = air_quality_df["datetime"].min()
max_date = air_quality_df["datetime"].max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label='Select Date Range', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

filtered_df = air_quality_df[(air_quality_df["datetime"] >= str(start_date)) & 
                            (air_quality_df["datetime"] <= str(end_date))]

# Create DataFrames for visualization
hourly_pollution_df = create_hourly_pollution_df(filtered_df)
max_pollutants_df = create_max_pollutants_df(filtered_df)
pollutants_by_region_df = create_pollutants_by_region_df(filtered_df)

# Dashboard
st.header('Air Quality Monitoring Dashboard :earth_asia:')

st.subheader('Hourly Pollution Levels')

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    hourly_pollution_df["datetime"],
    hourly_pollution_df["pollution_score"],
    marker='o', 
    linewidth=2,
    color="#FFA726"
)
ax.set_xlabel("Datetime")
ax.set_ylabel("Pollution Score")
ax.set_title("Hourly Pollution Score")
st.pyplot(fig)

st.subheader("Maximum Levels of Pollutants")

fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(x="max_level", y="pollutant", data=max_pollutants_df, palette="coolwarm", ax=ax)
ax.set_xlabel("Max Level")
ax.set_ylabel("Pollutant")
ax.set_title("Maximum Levels of Pollutants")
st.pyplot(fig)

if pollutants_by_region_df is not None:
    st.subheader("Pollutants by Region")

    fig, ax = plt.subplots(figsize=(16, 8))
    sns.barplot(x="region", y="pollution_score", data=pollutants_by_region_df, palette="Spectral", ax=ax)
    ax.set_xlabel("Region")
    ax.set_ylabel("Pollution Score")
    ax.set_title("Average Pollution Score by Region")
    ax.tick_params(axis='x', rotation=90)
    st.pyplot(fig)
else:
    st.subheader("Pollutants by Region")
    st.write("No region data available.")

st.subheader("Pollution Insights")

col1, col2 = st.columns(2)

with col1:
    avg_pm1 = round(filtered_df["PM1.0"].mean(), 2)
    st.metric("Average PM1.0", value=avg_pm1)

with col2:
    avg_pm25 = round(filtered_df["PM2.5"].mean(), 2)
    st.metric("Average PM2.5", value=avg_pm25)

col3, col4 = st.columns(2)

with col3:
    avg_nox = round(filtered_df["NOx"].mean(), 2)
    st.metric("Average NOx", value=avg_nox)

with col4:
    avg_co = round(filtered_df["CO"].mean(), 2)
    st.metric("Average CO", value=avg_co)

st.caption('Air Quality Dashboard © 2024')
