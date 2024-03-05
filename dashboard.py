import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pathlib import Path

sns.set(style='dark')

def get_total_count_by_hour_data(hour_data):
  hour_count_data =  hour_data.groupby(by="hours").agg({"count_cr": ["sum"]})
  return hour_count_data

def count_by_day_data(day_data):
    day_data_count_2011 = day_data.query(str('dteday >= "2011-01-01" and dteday < "2012-12-31"'))
    return day_data_count_2011

def total_registered_data(day_data):
   reg_data =  day_data.groupby(by="dteday").agg({
      "registered": "sum"
    })
   reg_data = reg_data.reset_index()
   reg_data.rename(columns={
        "registered": "register_sum"
    }, inplace=True)
   return reg_data

def total_casual_data(day_data):
   cas_data =  day_data.groupby(by="dteday").agg({
      "casual": ["sum"]
    })
   cas_data = cas_data.reset_index()
   cas_data.rename(columns={
        "casual": "casual_sum"
    }, inplace=True)
   return cas_data

def sum_order (hour_data):
    sum_order_items_data = hour_data.groupby("hours").count_cr.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_data

def macem_season (day_data): 
    season_data = day_data.groupby(by="season").count_cr.sum().reset_index() 
    return season_data

days_data = Path(__file__).resolve().parent / 'cleaned_day_data.csv'
days_data = pd.read_csv(days_data)
days_data.head()

hours_data = Path(__file__).resolve().parent / 'cleaned_hour_data.csv'
hours_data = pd.read_csv(hours_data)
hours_data.head()

datetime_columns = ["dteday"]
days_data.sort_values(by="dteday", inplace=True)
days_data.reset_index(inplace=True)   

hours_data.sort_values(by="dteday", inplace=True)
hours_data.reset_index(inplace=True)

for column in datetime_columns:
    days_data[column] = pd.to_datetime(days_data[column])
    hours_data[column] = pd.to_datetime(hours_data[column])

min_date_days = days_data["dteday"].min()
max_date_days = days_data["dteday"].max()

min_date_hour = hours_data["dteday"].min()
max_date_hour = hours_data["dteday"].max()

with st.sidebar:
        
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])
  
main_df_days = days_data[(days_data["dteday"] >= str(start_date)) & 
                       (days_data["dteday"] <= str(end_date))]

main_df_hour = hours_data[(hours_data["dteday"] >= str(start_date)) & 
                        (hours_data["dteday"] <= str(end_date))]

hour_count_data = get_total_count_by_hour_data(main_df_hour)
day_df_count_2011 = count_by_day_data(main_df_days)
reg_df = total_registered_data(main_df_days)
cas_df = total_casual_data(main_df_days)
sum_order_items_df = sum_order(main_df_hour)
season_df = macem_season(main_df_hour)

#visualisasi data
st.header('Bike Sharing Dataset 🚲')

st.subheader('Daily Sharing')
col1, col2, col3 = st.columns(3)
 
with col1:
    total_orders = day_df_count_2011.count_cr.sum()
    st.metric("Total Sharing Bike", value=total_orders)

with col2:
    total_sum = reg_df.register_sum.sum()
    st.metric("Total Registered", value=total_sum)

with col3:
    total_sum = cas_df.casual_sum.sum()
    st.metric("Total Casual", value=total_sum)

#1
st.subheader("Pada musim apa penyewaan sepeda paling sedikit?")
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
        y="count_cr", 
        x="season",
        data=season_df.sort_values(by="season", ascending=False),
        ax=ax
    )
ax.set_title("Grafik Penyewaan Berdasarkan Musim", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.write("Berdasarkan tampilan analisis di atas, penyewaan sepeda paling sedikit terdapat pada musim semi, kemudian disusul pada musim dingin, musim panas dan penyewaan sepeda paling banyak pada musim gugur")
st.pyplot(fig)

#2
st.subheader("Berapa banyak penyewa casual dibandingkan registered?")
labels = 'casual', 'registered'
sizes = [18.8, 81.2]
explode = (0, 0.1) 

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal') 
st.write("Berdasarkan tampilan analisis di atas terlihat bahwa penyewa casual sebanyak 18.8% hal ini berbanding jauh dengan registered sebanyak 81.2%")
st.pyplot(fig1)

#3
st.subheader("Bagaimana grafik penggunaan sepeda pada tahun 2011 dan 2012?")
days_data['month'] = pd.Categorical(days_data['month'], categories=
    ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
    ordered=True)

monthly_counts = days_data.groupby(by=["month","year"]).agg({
    "count_cr": "sum"
}).reset_index()

fig, ax = plt.subplots()
sns.lineplot(
    data=monthly_counts,
    x="month",
    y="count_cr",
    hue="year",
    palette="cividis",
    marker="o",
    ax=ax
)
ax.set_title("Penyewaan berdasarkan Bulan dan Tahun")
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.legend(title="Tahun", loc="upper right")
st.write("Berdasarkan analisis di atas, terlihat penyewaan sepeda pada tahun 2012 lebih besar dibandingkan pada tahun 2011. hal ini juga terlihat pada penyewaan sepeda tiap bulannya, dimana penyewaan sepeda di setiap bulan pada tahun 2012 lebih banyak dibandingkan di setiap bulan 2011.")
st.pyplot(fig)

st.caption('Copyright (c) I Kadek Widi Adnyana 2024')
