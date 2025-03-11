import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import matplotlib.ticker as ticker

#sns.set(style='dark')

def create_daily_rentals_df(df):
    daily_rentals_df = df.resample(rule = 'D', on = 'dteday').agg({'total_rental' : 'sum'})
    return daily_rentals_df

def create_rental_perjam_df(df) :
    rental_perjam_df = df.groupby(by='hr').cnt.sum().reset_index()
    return rental_perjam_df

def create_season_rentals_df(df) :
    season_rental_df = df.groupby(by='season').total_rental.sum().sort_values(ascending=False)
    return season_rental_df

def create_status_user_df(df) :
    status_user_df = df.resample(rule='M', on='dteday').agg({
        'casual' : 'sum',
        'registered' : 'sum'
    })
    return status_user_df

datahour_df = pd.read_csv('hour_data.csv')
dataday_df = pd.read_csv('day_df.csv')


dataday_df['dteday'] = pd.to_datetime(dataday_df['dteday'])
datahour_df['dteday'] = pd.to_datetime(datahour_df['dteday'])
min_date = dataday_df['dteday'].min()
max_date = dataday_df['dteday'].max()

with st.sidebar :
    st.image("https://www.freevector.com/uploads/vector/preview/27655/rental3.jpg")
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

utama_df = dataday_df[(dataday_df['dteday']>=str(start_date))&
                   (dataday_df['dteday']<=str(end_date))]

kedua_df = datahour_df[(datahour_df['dteday']>=str(start_date))&
                   (datahour_df['dteday']<=str(end_date))]

daily_rentals_df = create_daily_rentals_df(utama_df)
rental_perjam_df = create_rental_perjam_df(kedua_df)
season_rental_df = create_season_rentals_df(utama_df)
status_user_df = create_status_user_df(utama_df)

st.header('Bike Rental Dashboard :bike: :sparkles:')
st.subheader('Daily Rentals')
col1, col2 = st.columns(2)
with col1 :
    jumlah_rentals = daily_rentals_df.total_rental.sum()
    st.metric('Total rentals', value=jumlah_rentals)

with col2 :
    avg_rentals = daily_rentals_df.total_rental.mean()
    st.metric('Avg daily rentals', value=f"{avg_rentals:.2f}")

fig, ax = plt.subplots(figsize=(16,8))
ax.plot(
    daily_rentals_df.index,
    daily_rentals_df["total_rental"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
) 
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.subheader("Total Rental by Season :cloud:")
fig, ax = plt.subplots(figsize=(15,10))
bars = ax.bar(season_rental_df.index, season_rental_df.values, color="gray")
bars[0].set_color("#90CAF9")
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x):,}'))
ax.set_ylabel("Total Rentals", fontsize=15)
ax.set_xlabel("Season", fontsize=15)
ax.set_title("Seasonal Bike Rental Trends", loc="center", fontsize=30)
ax.set_xticklabels(season_rental_df.index, fontsize=15)
st.pyplot(fig)

st.subheader("Understanding User Trends")
fig, ax = plt.subplots(figsize=(15,10))
status_user_df.plot(kind='bar', ax=ax, color=["orange", "blue"])
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x):,}'))
ax.set_xlabel(None)
ax.set_ylabel("Total rental")
ax.set_title("Casual VS Registered (Monthly)", loc="center", fontsize=30)
ax.legend(["Casual", "Registered"])
st.pyplot(fig)

st.subheader("Hourly Bike Rental Trends")
fig, ax = plt.subplots(figsize=(16,8))
ax.plot(
    rental_perjam_df.index,
    rental_perjam_df["cnt"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
) 
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_title("Total Rental Per Hour", loc="center", fontsize=30)
st.pyplot(fig)

byworkingday_comparison_df = dataday_df.groupby('workingday')[['casual', 'registered']].mean()
st.subheader("Rental User Comparisan by Weekday (Average)")
fig, ax = plt.subplots(figsize=(16,8))
byworkingday_comparison_df.plot(kind='bar', ax=ax, color=["orange", "blue"])
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x):,}'))
ax.set_xlabel("Working Day")
ax.set_ylabel("Total Rental")
st.pyplot(fig)