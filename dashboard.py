import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime as dt
sns.set_theme(style='dark')

def create_daily_df(df):
    daily_orders_df = df.resample(rule='D', on='dteday').agg({
        "instant": "nunique",
        "user_count": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    
    return daily_orders_df

def create_monthly_df(df):
    df['dteday'] = pd.to_datetime(day_df['dteday']) 
    monthly_users_df = df.resample(rule='ME', on='dteday').agg({
        "instant": "nunique",
        "user_count": "sum"
    })

    monthly_users_df = monthly_users_df.reset_index()

    return monthly_users_df

def create_hourly_df(df):
    def number_to_hour(num):
        hours = [dt.time(i).strftime('%H:%M') for i in range(0, 24)]
        return hours[num]
    df["hour"] = df["hr"].apply(number_to_hour)
    return df

def create_seasonly_df(df):
    seasonal_max_users = df.groupby(by="season_name").agg({
        "casual": "sum",
        "registered": "sum",
        "user_count": "sum"
    })
    return seasonal_max_users

day_df = pd.read_csv("data/daily_edited.csv")
hour_df = pd.read_csv("data/hourly_edited.csv")

day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    st.image("logo.jpg")
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

filter_day_df = day_df[(day_df["dteday"] >= str(start_date)) & (day_df["dteday"] <= str(end_date))]

daily_users_df = create_daily_df(filter_day_df)
monthly_users_df = create_monthly_df(filter_day_df)
hourly_users_df = create_hourly_df(hour_df)
seasonly_users_df = create_seasonly_df(day_df)

st.header('Bike Rental Dashboard :bike:')

st.subheader('Number of Users per Day')
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_users_df["dteday"],
    daily_users_df["user_count"],
    marker='o', 
    linewidth=2,
    color="#E3A76B"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_xlabel("Daily Users", fontsize=18)
ax.set_ylabel("User Count", fontsize=18)
st.pyplot(fig)

st.subheader("Number of Users per Month") 

fig, ax = plt.subplots(figsize=(24, 8))
ax.plot(
    monthly_users_df["dteday"], 
    monthly_users_df["user_count"], 
    marker='o', 
    linewidth=2, 
    color="#E3A76B"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)
ax.set_xlabel("Monthly Users", fontsize=28)
ax.set_ylabel("User Count", fontsize=28)
st.pyplot(fig)

st.subheader('Bike Rental Trending Hours')

fig, ax = plt.subplots(figsize=(28, 16))
ax.barh(
    y=hourly_users_df["hour"], 
    width=hourly_users_df["cnt"],
    color="#E3A76B",
    edgecolor="#E3A76B"
)
ax.tick_params(axis='x', labelsize=24)
ax.tick_params(axis='y', labelsize=24)
ax.set_xlabel("User Count", fontsize=28)
ax.set_ylabel("Hours", fontsize=28)
st.pyplot(fig)

st.subheader('Proportion of Users per Season')

fig, ax = plt.subplots(figsize=(16, 16))
ax.pie(
    seasonly_users_df["user_count"], 
    labels=seasonly_users_df.index, 
    autopct='%1.1f%%', 
    pctdistance=0.8, 
    startangle=90, 
    wedgeprops = {'width': 0.4},
    textprops={'fontsize': 24}
)
st.pyplot(fig)