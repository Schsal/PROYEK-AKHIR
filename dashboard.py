import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Load Data

def load_data():
    return pd.read_csv("datahour.csv")

data_df = load_data()

st.title("Dashboard Bike Rental")

# 1. Visualisasi Total Rental Per Jam
st.subheader("Total Rental Per Jam")
by_hour = data_df.groupby("hr")["total_rental"].sum().reset_index() 
fig, ax = plt.subplots()
ax.plot(by_hour["hr"], by_hour["total_rental"], marker='o', linestyle="-")
ax.set_xlabel("Hour")
ax.set_ylabel("Total Rental")
st.pyplot(fig)

# 2. Perbandingan Casual vs Registered Berdasarkan Working Day
st.subheader("Casual vs Registered Users")
by_workingday = data_df.groupby("workingday")[["casual", "registered"]].sum()
fig, ax = plt.subplots()
by_workingday.plot(kind="bar", ax=ax, color=["orange", "blue"])
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x):,}'))
ax.set_xlabel("Working Day (0 = No, 1 = Yes)")
ax.set_ylabel("Total Rental")
st.pyplot(fig)

# 3. Total Rental Per Season
st.subheader("Total Rental Per Season")
by_season = data_df.groupby("season")["total_rental"].sum().sort_values(ascending=False)
fig, ax = plt.subplots()
bars = ax.bar(by_season.index, by_season.values, color="gray")
bars[0].set_color("blue")  # Warna biru untuk yang paling banyak
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x):,}'))
ax.set_xlabel("Season")
ax.set_ylabel("Total Rental")
st.pyplot(fig)
