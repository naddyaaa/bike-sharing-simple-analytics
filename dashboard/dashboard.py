import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#Menghitung jumlah cnt di setiap season
def create_by_season(df):
    byseason_df = df.groupby(by="season")["cnt"].sum().reset_index()
    return byseason_df

#Menghitung jumlah cnt di setiap hour
def create_by_hr(df):
    sum_hr = df.groupby("hr")["cnt"].sum().reset_index()
    return sum_hr

#Menghitung jumlah penyewaan berdasarkan hour dan weather
def create_rfm(df):
    hour_weather_group = df.groupby(['hr', 'weathersit'])['cnt'].sum().reset_index()

    #Mengisi nilai 0 pada cnt dengan interpolasi
    hour_weather_group = hour_weather_group.pivot(index='hr', columns='weathersit', values='cnt').fillna(0)
    hour_weather_group = hour_weather_group.interpolate(method='linear')
    hour_weather_group = hour_weather_group.reset_index()
    hour_weather_group = hour_weather_group.melt(id_vars='hr', var_name='weathersit', value_name='cnt')
    return hour_weather_group

#read data yang disimpan sebelumnya
all_df = pd.read_csv("main_data.csv")

#ubah 1-7 menjadi nama hari, ini untuk kolom weekday
day_map = {
    0: "Sunday",
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
}

#Menambahkan kolom baru yaitu 'day' ke DataFrame
all_df['day'] = all_df['weekday'].map(day_map)

#Mengambil daftar hari yang unik untuk dijadikan filter
unique_days = all_df['day'].unique()

#Membuat dropdown hari sebagai filter
with st.sidebar:
    selected_day = st.selectbox(
        label='Pilih Hari',
        options=unique_days
    )

#Filtering berdasarkan hari yang dipilih
main_df = all_df[all_df['day'] == selected_day]

#Memanggil fungsi penghitung
byseason_df = create_by_season(main_df)
sum_hr = create_by_hr(main_df)
hour_weather_group = create_rfm(main_df)

#Judul aplikasi
st.header('Bike Rent Dashboard :sparkles:')

#Visualisasi Penyewaan Berdasarkan Musim
st.subheader("Penyewaan Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    y="cnt", 
    x="season",
    data=byseason_df.sort_values(by="cnt", ascending=True), 
    palette=sns.color_palette("Greens_d", n_colors=4),
)
ax.set_title("Penyewaan Berdasarkan Musim", loc="center", fontsize=15)
ax.tick_params(axis='y', labelsize=12)
ax.grid(False)
st.pyplot(fig) 

#Visualisasi Penyewaan Berdasarkan Jam
st.subheader("Penyewaan Berdasarkan Jam")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(
    sum_hr["hr"],  
    sum_hr["cnt"], 
    marker='o',
    linewidth=2,
    color="#72BCD4"
)
ax.set_title("Tren Penyewaan Berdasarkan Jam", loc="center", fontsize=20)
ax.set_xlabel("Jam", fontsize=15)
ax.set_ylabel("Jumlah Penyewaan", fontsize=15)
ax.grid(False)
st.pyplot(fig) 

#Visualisasi Penyewaan Berdasarkan Jam dan Weather
st.subheader("Penyewaan Berdasarkan Jam dan Weather")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=hour_weather_group,
    x='hr',
    y='cnt',
    hue='weathersit',
    marker='o',
    ax=ax,
    palette='deep'
)
plt.title('Jumlah Penyewaan Berdasarkan Jam dan Kondisi Cuaca')
plt.xlabel('Jam')
plt.ylabel('Jumlah Penyewaan')
plt.legend(title='Kondisi Cuaca')
plt.xticks(range(0, 24))
plt.grid()
st.pyplot(fig)
