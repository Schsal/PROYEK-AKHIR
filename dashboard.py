import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def load_data():
    return pd.read_csv("datahour.csv")
def load_DATA():
    return pd.read_csv("day.csv")
day_df = load_DATA()
data_df = load_data()

st.title("Dashboard Bike Rental")

# Sidebar Filters
st.sidebar.header("Filter Data")
selected_year = st.sidebar.selectbox("Pilih Tahun", data_df["yr"].unique())
selected_season = st.sidebar.selectbox("Pilih Musim", data_df["season"].unique())

filtered_data = data_df[(data_df["yr"] == selected_year) & (data_df["season"] == selected_season)]

#Total Rental Berdasarkan Hari dan Cuaca Tertentu
st.header("Total Rental for Selected Day and Weather")
if not filtered_data.empty:
    total_rental_filtered = filtered_data["total_rental"].sum()
    st.write(f"Jumlah sewa pada tahun  **{selected_year}** di musim  **{selected_season}**: {total_rental_filtered:,}")
else:
    st.write("Data tidak tersedia untuk filter yang dipilih")

#Visualisasi Total Rental Per Jam tahun 2011
st.subheader("Total Rental Per Jam Tahun 2011")
byhour2011_df=data_df[data_df['yr']==2011].groupby(by="hr")["total_rental"].sum().reset_index()
fig, ax = plt.subplots()
ax.plot(byhour2011_df["hr"], byhour2011_df["total_rental"], marker='o', linestyle="-")
ax.set_xlabel("Hour")
ax.set_ylabel("Total Rental")
st.pyplot(fig)

#Visualisasi Total Rental Per Jam tahun 2011
st.subheader("Total Rental Per Jam Tahun 2012")
byhour2012_df=data_df[data_df['yr']==2012].groupby(by="hr")["total_rental"].sum().reset_index()
fig, ax = plt.subplots()
ax.plot(byhour2012_df["hr"], byhour2012_df["total_rental"], marker='o', linestyle="-")
ax.set_xlabel("Hour")
ax.set_ylabel("Total Rental")
st.pyplot(fig)

#Perbandingan Casual vs Registered Berdasarkan Working Day
st.subheader("Casual vs Registered Users")
by_workingday = day_df.groupby("workingday")[["casual", "registered"]].mean()
fig, ax = plt.subplots()
by_workingday.plot(kind="bar", ax=ax, color=["orange", "blue"])
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x):,}'))
ax.set_xlabel("Working Day (0 = No, 1 = Yes)")
ax.set_ylabel("Total Rental")
st.pyplot(fig)

#Total Rental Per Season
st.subheader("Total Rental Per Season")
by_season = data_df.groupby("season")["total_rental"].sum().sort_values(ascending=False)
fig, ax = plt.subplots()
bars = ax.bar(by_season.index, by_season.values, color="gray")
bars[0].set_color("blue")
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x):,}'))
ax.set_xlabel("Season")
ax.set_ylabel("Total Rental")
st.pyplot(fig)

