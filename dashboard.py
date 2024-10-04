import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style for seaborn
sns.set(style='dark')

# Define helper functions
def create_daily_pollution_df(df):
    daily_pollution_df = df.resample(rule='D', on='datetime').agg({
        "No": "nunique",
        "PM2.5": "mean",
        "PM10": "mean",
        "SO2": "mean",
        "NO2": "mean",
        "CO": "mean",
        "O3": "mean",
        "pollution_score": "mean"
    })
    daily_pollution_df = daily_pollution_df.reset_index()
    return daily_pollution_df

def create_avg_pollutants_df(df):
    avg_pollutants_df = df.drop('datetime', axis=1)
    avg_pollutants_df = avg_pollutants_df.apply(pd.to_numeric, errors='coerce')
    avg_pollutants_df = avg_pollutants_df.mean().reset_index()
    avg_pollutants_df.columns = ["pollutant", "average_level"]
    return avg_pollutants_df

def create_pollutants_by_station_df(df):
    if 'station' in df.columns:
        pollutants_by_station_df = df.groupby("station").mean(numeric_only=True).reset_index()
    else:
        pollutants_by_station_df = None
    return pollutants_by_station_df

# Load data
try:
    all_df = pd.read_csv(r'./All Data.csv')
except FileNotFoundError:
    st.error("File not found. Please check the file path.")
    st.stop()

# Ensure datetime columns are in datetime format
all_df['datetime'] = pd.to_datetime(all_df['datetime'], errors='coerce')

# Create filters
min_date = all_df["datetime"].min()
max_date = all_df["datetime"].max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["datetime"] >= str(start_date)) & 
                  (all_df["datetime"] <= str(end_date))]

# Create DataFrames for visualization
daily_pollution_df = create_daily_pollution_df(main_df)
avg_pollutants_df = create_avg_pollutants_df(main_df)
pollutants_by_station_df = create_pollutants_by_station_df(main_df)

# Dashboard
st.header('Air Pollution Dashboard :cloud:')

st.subheader('Daily Pollution Levels')

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_pollution_df["datetime"],
    daily_pollution_df["pollution_score"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.set_xlabel("Date")
ax.set_ylabel("Pollution Score")
ax.set_title("Daily Pollution Score")
st.pyplot(fig)

st.subheader("Average Levels of Pollutants")

fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(x="average_level", y="pollutant", data=avg_pollutants_df, palette="viridis", ax=ax)
ax.set_xlabel("Average Level")
ax.set_ylabel("Pollutant")
ax.set_title("Average Levels of Pollutants")
st.pyplot(fig)

if pollutants_by_station_df is not None:
    st.subheader("Pollutants by Station")

    fig, ax = plt.subplots(figsize=(16, 8))
    sns.barplot(x="station", y="pollution_score", data=pollutants_by_station_df, palette="plasma", ax=ax)
    ax.set_xlabel("Station")
    ax.set_ylabel("Pollution Score")
    ax.set_title("Average Pollution Score by Station")
    ax.tick_params(axis='x', rotation=90)
    st.pyplot(fig)
else:
    st.subheader("Pollutants by Station")
    st.write("No station data available.")

# Question 1: O3 and Temperature Correlation
st.subheader("Correlation between O3 and Temperature (TEMP)")

# Calculate correlation
correlation = main_df[['O3', 'TEMP']].corr()
st.write("Korelasi antara O3 dan suhu (TEMP):")
st.write(correlation)

# Scatter plot for O3 and TEMP
fig, ax = plt.subplots(figsize=(12, 6))
ax.scatter(main_df['O3'], main_df['TEMP'], alpha=0.5)
ax.set_title('Scatter Plot antara O3 dan Suhu (TEMP)')
ax.set_xlabel('Konsentrasi O3 (µg/m³)')
ax.set_ylabel('Suhu (°C)')
ax.grid()
st.pyplot(fig)

# Question 2: Correlation between Dew Point (DEWP) and Temperature (TEMP)
st.subheader("Correlation between Dew Point (DEWP) and Temperature (TEMP)")

# Calculate correlation matrix
corr_matrix_humidity_temp = main_df[['TEMP', 'DEWP']].corr()

# Heatmap for DEWP and TEMP correlation
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr_matrix_humidity_temp, annot=True, cmap='coolwarm', fmt=".2f", 
            cbar_kws={"label": "Correlation Coefficient"}, ax=ax)
ax.set_title('Matriks Korelasi antara Suhu dan Titik Embun')
st.pyplot(fig)

# Pollution Data Insights
st.subheader("Pollution Data Insights")

col1, col2 = st.columns(2)

with col1:
    avg_pm25 = round(main_df["PM2.5"].mean(), 2)
    st.metric("Average PM2.5", value=avg_pm25)

with col2:
    avg_pm10 = round(main_df["PM10"].mean(), 2)
    st.metric("Average PM10", value=avg_pm10)

col3, col4 = st.columns(2)

with col3:
    avg_no2 = round(main_df["NO2"].mean(), 2)
    st.metric("Average NO2", value=avg_no2)

with col4:
    avg_so2 = round(main_df["SO2"].mean(), 2)
    st.metric("Average SO2", value=avg_so2)

col5, col6 = st.columns(2)

with col5:
    avg_co = round(main_df["CO"].mean(), 2)
    st.metric("Average CO", value=avg_co)

with col6:
    avg_o3 = round(main_df["O3"].mean(), 2)
    st.metric("Average O3", value=avg_o3)

st.caption('Copyright (c) Rizki Kristian H. Nainggolan - Dicoding 2024')
