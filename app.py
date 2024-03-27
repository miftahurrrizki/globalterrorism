import pandas as pd
import streamlit as st
from streamlit_echarts import st_echarts
from chart_utils import *


@st.cache_data
def get_csv_gcs(file_name):
    # csv_data = pd.read_csv('gs://' + bucket_name + '/' + file_name, encoding='utf-8')  
    # csv_data = pd.read_excel('gs://' + bucket_name + '/' + file_name, encoding='utf-8')
    csv_data = pd.read_csv(file_name)    
    return csv_data

bucket_name = "mainpads/dataset"
file_name = "globalterrorism1.csv"

judul = 'Global Terrorism Analysis'
sub = 'Kelompok Yaaaudah'

st.set_page_config(page_title = judul,
                   page_icon = ":skull:",
                   layout = "wide")

st.title(judul)
st.caption(sub)


df = get_csv_gcs(file_name)


# total events
total_events = df['Year'].count()
# total victims
total_victims = df['Killed'].sum() + df['Wounded'].sum()
# total groupname
total_groupnamex = df['GroupName'].unique()
total_groupname = len(total_groupnamex)

column1, column2, column3 = st.columns(3)
with column1:
    st.subheader('Total Events:')
    st.subheader(total_events)

with column2:
    st.subheader('Total Casualities:')
    st.subheader(int(total_victims))

with column3:
    st.subheader('Total Terrorist Group:')
    st.subheader(len(total_groupnamex))

# ----------SIDEBAR----------
selected_countries = st.sidebar.multiselect('Select Country(s)', options=[
    'Lihat Seluruh Negara'] + list(df['Country'].unique()))

if 'Lihat Seluruh Negara' in selected_countries:
    filtered_df = df
else:
    filtered_df = df[(df['Country'].isin(selected_countries))]

# ----------MAP PERSEBARAN----------
with st.container():
    st.map(filtered_df[["latitude","longitude"]])
# st.write(filtered_df.columns.values)
# ----------JML AKSI PER NEGARA----------
# Menghitung total aksi teroris per negara setelah diterapkan filter
with st.container():
    actionpercountry_plot(filtered_df)
# ----------BARCHART KILLED N WOUNDED----------

with st.container():
    # Mengelompokkan data berdasarkan tahun dan menghitung total korban tewas dan terluka
    killnwound_barplot(filtered_df)

# ----------LINECHART TAHUN KE TAHUN----------
with st.container():
    # Buat st.slider untuk memilih rentang tahun
    year_range = st.slider('Filter by Year Range', min_value=int(df['Year'].min()), max_value=int(df['Year'].max()), value=(int(df['Year'].min()), int(df['Year'].max())))
    filtered_data, chart_config = yearperyear_lineplot(df, selected_countries, year_range)
    st_echarts(chart_config, height=600)
# ----------LINERACE NEGARA PERTAHUN----------

with st.container():
    chart_config = actionperyear_plot(selected_countries, filtered_data)
    st_echarts(chart_config, height=500)

# ----------HIST KILLED N WOUNDED----------

with st.container():
    # Membuat histogram menggunakan Plotly Express
    killnwound_histplot(filtered_df)

### Dataframe
with st.container():
    # Menampilkan dataframe
    if st.checkbox("Show The Table"):
        show_df_filtered(filtered_df)

with st.container():
    
    # Menghitung total aksi teroris per jenis senjata setelah diterapkan filter
    terroristPerWeapon_plot(filtered_df)


with st.container():
    # Mengambil data WeaponType dan menghitung jumlahnya
    wp_plot(filtered_df)
