
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import folium
from streamlit_folium import st_folium
from streamlit_folium import folium_static
from streamlit_echarts import st_echarts
import plotly.graph_objects as go


@st.cache_resource()
def map_plot(filtered_df):
    'Map Persebaran Aksi Terorisme'
    # Mendapatkan nilai rata-rata latitude dan longitude dari data yang telah difilter
    avg_latitude = filtered_df['Latitude'].mean()
    avg_longitude = filtered_df['Longitude'].mean()

    # Membuat peta dengan zoom awal pada titik latitude dan longitude yang dipilih
    map = folium.Map(prefer_canvas=True)#location=[avg_latitude, avg_longitude], zoom_start=3)

    # Menambahkan marker pada peta untuk setiap baris dalam dataframe yang memiliki data koordinat
    for index, row in filtered_df.iterrows():
        if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']):
            location = [row['Latitude'], row['Longitude']]
            total_casualties = int(row['Killed'] + row['Wounded'])
            group_name = row['GroupName']

            tooltip = f"Group: {group_name}<br>Total Casualties: {total_casualties}"

            folium.Marker(location, tooltip=tooltip).add_to(map)

    # Menampilkan peta di Streamlit
    return map

@st.cache_data(show_spinner=True)
def actionpercountry_plot(filtered_df):
    country_counts = filtered_df['Country'].value_counts()

    # Mengurutkan berdasarkan total aksi teroris secara menurun
    country_counts_sorted = country_counts.sort_values(ascending=False)

    # Membuat dataframe baru dengan data yang terurut
    df_sorted = pd.DataFrame({'Country': country_counts_sorted.index,
                            'Total Attacks': country_counts_sorted.values})
    
    # Membuat histogram menggunakan plotly
    fig = px.histogram(df_sorted, x='Country', y='Total Attacks',
                       title=f'Total Aksi Teroris per Negara',
                       labels={'Country': 'Negara',
                               'Total Attacks': 'Total Aksi Teroris'},
                       text_auto='.2s',
                       nbins=len(df_sorted))

    # Mengurutkan histogram dari terbesar
    fig.update_xaxes(categoryorder='total descending')

    # Menampilkan histogram menggunakan Streamlit
    st.plotly_chart(fig, use_container_width=True)


@st.cache_data(show_spinner=True)
def killnwound_barplot(filtered_df):
    filtered_df_grouped = filtered_df.groupby(
        'Year')[['Killed', 'Wounded']].sum().reset_index()

    # Membuat bar chart menggunakan plotly
    fig = px.bar(filtered_df_grouped, x='Year', y=['Killed', 'Wounded'], barmode='group',
                 color_discrete_sequence=['lightsalmon', 'lightblue'],
                 title='Total Korban Tewas dan Terluka per Tahun')
    fig.update_layout(xaxis_title='Tahun',
                      yaxis_title='Jumlah', legend_title='')

    # Menampilkan bar chart menggunakan Streamlit
    st.plotly_chart(fig, use_container_width=True)


@st.cache_data(show_spinner=True)
def yearperyear_lineplot(df, selected_countries, year_range):
    # Ambil data yang telah difilter berdasarkan rentang tahun
    filtered_data = df[(df['Country'].isin(selected_countries)) & (df['Year'].between(year_range[0], year_range[1]))]

    # Buat dataframe baru untuk menghitung jumlah total aksi tahun ke tahun
    total_actions = filtered_data.groupby('Year').size().reset_index(name='Total Actions')

    # Konfigurasi grafik line race dengan efek hover
    chart_config = {
        "xAxis": {"type": "category", "data": total_actions['Year'].astype(str).tolist()},
        "yAxis": {"type": "value"},
        "series": [
            {
                "type": "line",
                "data": total_actions['Total Actions'].tolist(),
                "emphasis": {
                    "focus": "series",
                    "lineStyle": {"opacity": 1, "width": 4},
                    "label": {"show": False},
                },
                "itemStyle": {"normal": {"opacity": 0.7, "width": 2}},
            }
        ],
        "tooltip": {"trigger": "axis"},
    }

    return filtered_data, chart_config

@st.cache_data(show_spinner=True)
def actionperyear_plot(selected_countries, filtered_data):
    total_actions = filtered_data.groupby(
        ['Year', 'Country']).size().reset_index(name='Total Actions')

    # Buat list kosong untuk menyimpan series garis per negara
    series_data = []

    # Loop melalui setiap negara
    for country in selected_countries:
        country_data = total_actions[total_actions['Country'] == country]
        series = {
            "name": country,
            "type": "line",
            "data": country_data['Total Actions'].tolist(),
            "emphasis": {
                "focus": "series",
                "lineStyle": {"opacity": 1, "width": 4},
                "label": {"show": False},
            },
            "itemStyle": {"normal": {"opacity": 0.7, "width": 2}},
        }
        series_data.append(series)

    # Konfigurasi grafik line race dengan efek hover
    chart_config = {
        "title": {"text": "Total Actions by Year"},
        "xAxis": {"type": "category", "data": total_actions['Year'].astype(str).unique().tolist()},
        "yAxis": {"type": "value"},
        "series": series_data,
        "tooltip": {"trigger": "axis"},
    }

    return chart_config

@st.cache_data(show_spinner=True)
def killnwound_histplot(filtered_df):
    fig = px.histogram(filtered_df, x=['Killed', 'Wounded'], nbins=50,
                    color_discrete_sequence=['lightsalmon', 'lightblue'],
                    labels={'value': 'Jumlah', 'variable': 'Kategori'})

    # Menambahkan judul dan mengatur sumbu x dan y
    fig.update_layout(title='Histogram Jumlah Korban Tewas dan Terluka',
                    xaxis_title='Jumlah Korban',
                    yaxis_title='Jumlah Kejadian')

    # Menampilkan histogram menggunakan Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
@st.cache_data(show_spinner=True)
def show_df_filtered(filtered_df):
    
    st.write(filtered_df[['Year', 'Month', 'Day', 'Region', 'Country', 'City', 'Latitude', 'Longitude', 'GroupName', 'AttackType',
                            'WeaponType', 'Target', 'TargetType', 'Success', 'Suicide', 'Killed', 'Wounded']].shape)
    
    st.write(filtered_df[['Year', 'Month', 'Day', 'Region', 'Country', 'City', 'Latitude', 'Longitude', 'GroupName', 'AttackType',
                            'WeaponType', 'Target', 'TargetType', 'Success', 'Suicide', 'Killed', 'Wounded']])
    
    
@st.cache_data(show_spinner=True)
def terroristPerWeapon_plot(filtered_df):
    weapon_counts = filtered_df['WeaponType'].value_counts()

    # Mengurutkan berdasarkan total aksi teroris secara menurun
    weapon_counts_sorted = weapon_counts.sort_values(ascending=False)

    # Membuat dataframe baru dengan data yang terurut
    df_sorted = pd.DataFrame({'WeaponType': weapon_counts_sorted.index,
                            'Total Attacks': weapon_counts_sorted.values})
    
    
    
    # Membuat histogram menggunakan plotly
    fig = px.histogram(df_sorted, x='WeaponType', y='Total Attacks',
                       title=f'Total Aksi Teroris Berdasarkan Jenis Senjata',
                       labels={'WeaponType': 'Senjata',
                               'Total Attacks': 'Total Aksi'},
                       text_auto='.2s',
                       nbins=len(df_sorted))

    # Mengurutkan histogram dari terbesar
    fig.update_xaxes(categoryorder='total descending')

    # Menampilkan histogram menggunakan Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    
@st.cache_resource()
def wp_plot(filtered_df):
    weapon_counts = filtered_df['WeaponType'].value_counts().reset_index()
    weapon_counts.columns = ['WeaponType', 'Count']

    # Membuat pie chart menggunakan Plotly Express
    fig = px.pie(weapon_counts, values='Count', names='WeaponType', title='Total Weapon Type')

    # Menampilkan pie chart pada Streamlit
    st.plotly_chart(fig, use_container_width=True)