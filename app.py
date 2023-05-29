
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import folium
from streamlit_folium import st_folium
from streamlit_folium import folium_static
from streamlit_echarts import st_echarts
from pyecharts.charts import Pie
from pyecharts import options as opts
from palettable.colorbrewer.qualitative import Pastel1_5
import plotly.graph_objects as go
import colorlover as cl




# df = urllib2.urlopen(https://drive.google.com/file/d/1DeubD5b4tAckNgLmLnFYtlVaqBo1ncj-/view?usp=drive_link) # it's a file like object and works just like a file


df = pd.read_csv(r"C:\Users\mfthr\anaconda3\envs\streamlit\GlobalTerr\globalterrorism1.csv", encoding="latin-1")



# total events
total_events = df['Year'].count()
# total victims
total_victims = df['Killed'].sum() + df['Wounded'].sum()
# total groupname
total_groupnamex = df['GroupName'].unique()
total_groupname = len(total_groupnamex)




# -------- STREAMLIT PAGE ----------

judul = 'Global Terrorism Analysis'
sub = 'Kelompok Yaudaaaaah'

# filter tahun
# df_dipilih = df.query(
#     'Year == @Year'
# )
st.set_page_config(page_title = judul,
                   page_icon = ":skull:",
                   layout = "wide")
st.title(judul)
st.caption(sub)





# # atas1
# total_events = int(df_dipilih['Year'].count())
# total_victims = int(df_dipilih['Killed'].sum() + df_dipilih['Wounded'].sum())

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


# sidebar
# st.sidebar.header("Silahkan Filter Disini:")
# selected_countries = st.sidebar.multiselect('Select Country(s)', options=[
#     'Lihat Seluruh Negara'] + list(df['Country'].unique())) #, default=['Lihat Seluruh Negara'])

# selected_years = st.sidebar.multiselect('Select Year(s)', options=[
#     'Lihat Seluruh Tahun'] + list(df['Year'].unique())) #, default=['Lihat Seluruh Tahun'])

# # Menerapkan filter pada dataframe berdasarkan pilihan pengguna
# if 'Lihat Seluruh Negara' in selected_countries:
#     filtered_df = df[df['Country'].isin(df['Country'])]
# elif 'Lihat Seluruh Tahun' in selected_years:
#     filtered_df = df[df['Year'].isin(df['Year'])]
# else:
#     filtered_df = df[
#         (df['Year'].isin(selected_years)) &
#         (df['Country'].isin(selected_countries))
#     ]

# ----------SIDEBAR----------
st.sidebar.header("Silahkan Filter Disini:")
selected_countries = st.sidebar.multiselect('Select Country(s)', options=[
    'Lihat Seluruh Negara'] + list(df['Country'].unique()))

# selected_years = st.sidebar.multiselect('Select Year(s)', options=[
#     'Lihat Seluruh Tahun'] + list(df['Year'].unique()))

# selected_weapon = st.sidebar.multiselect('Select Weapon Type', options=[
#     'Lihat Seluruh Senjata'] + list(df['WeaponType'].unique()))


# ----------FILTER UTAMA----------
# Menerapkan filter pada dataframe berdasarkan pilihan pengguna
# if 'Lihat Seluruh Negara' in selected_countries and 'Lihat Seluruh Tahun' in selected_years and 'Lihat Seluruh Senjata' in selected_weapon:
#     filtered_df = df.copy()  # Tampilkan semua data jika kedua opsi dipilih
# else:
#     if 'Lihat Seluruh Negara' in selected_countries:
#         filtered_df = df[df['Year'].isin(selected_years)]
#     elif 'Lihat Seluruh Tahun' in selected_years:
#         filtered_df = df[df['Country'].isin(selected_countries)]
#     else:
#         filtered_df = df[
#             (df['Year'].isin(selected_years)) &
#             (df['Country'].isin(selected_countries)) &
#             (df['WeaponType'].isin(selected_weapon))
#         ]



# #display tabel
# if st.checkbox("Show The Table"):
#     st.write(filtered_df.shape)
#     st.dataframe(filtered_df, use_container_width=True)

# Menerapkan filter pada dataframe berdasarkan pilihan pengguna
# if 'Lihat Seluruh Negara' in selected_countries:
#     filtered_df = df[df['Country'].isin(selected_countries)]
# elif 'Lihat Seluruh Tahun' in selected_years:
#     filtered_df = df[df['Year'].isin(selected_years)]
# else:
#     filtered_df = df[
#         (df['Year'].isin(selected_years)) &
#         (df['Country'].isin(selected_countries))
#     ]
if 'Lihat Seluruh Negara' in selected_countries:
    filtered_df = df
# elif 'Lihat Seluruh Tahun' in selected_years:
#     filtered_df = df
else:
    filtered_df = df[
        # (df['Year'].isin(selected_years)) &
        (df['Country'].isin(selected_countries))
    ]



# ----------MAP PERSEBARAN----------
with st.container():
    'Map Persebaran Aksi Terorisme'
    # Mendapatkan nilai rata-rata latitude dan longitude dari data yang telah difilter
    avg_latitude = filtered_df['Latitude'].mean()
    avg_longitude = filtered_df['Longitude'].mean()

    # Membuat peta dengan zoom awal pada titik latitude dan longitude yang dipilih
    map = folium.Map()#location=[avg_latitude, avg_longitude], zoom_start=3)

    # Menambahkan marker pada peta untuk setiap baris dalam dataframe yang memiliki data koordinat
    for index, row in filtered_df.iterrows():
        if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']):
            location = [row['Latitude'], row['Longitude']]
            total_casualties = int(row['Killed'] + row['Wounded'])
            group_name = row['GroupName']

            tooltip = f"Group: {group_name}<br>Total Casualties: {total_casualties}"

            folium.Marker(location, tooltip=tooltip).add_to(map)

    # Menampilkan peta di Streamlit
    folium_static(map, width=1300, height=450)

# ----------JML AKSI PER NEGARA----------
with st.container():
    
    
    # Menghitung total aksi teroris per negara setelah diterapkan filter
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




# ----------BARCHART KILLED N WOUNDED----------
with st.container():
    # Mengelompokkan data berdasarkan tahun dan menghitung total korban tewas dan terluka
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


# ----------LINECHART TAHUN KE TAHUN----------
with st.container():

    # Buat st.slider untuk memilih rentang tahun
    year_range = st.slider('Filter by Year Range', min_value=int(df['Year'].min()), max_value=int(df['Year'].max()), value=(int(df['Year'].min()), int(df['Year'].max())))

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

    # Tampilkan grafik menggunakan st_echarts
    st_echarts(chart_config, height=600)


# ----------LINERACE NEGARA PERTAHUN----------
with st.container():

    #     # Ambil tahun terkecil dan terbesar dari filtered_data
    # min_year = filtered_data['Year'].min()
    # max_year = filtered_data['Year'].max()

    # # Slider untuk memilih rentang tahun
    # selected_year_range = st.slider(
    #     'Select Year Range', min_value=min_year, max_value=max_year, value=(min_year, max_year))

    # # Menerapkan filter tahun pada filtered_data
    # filtered_data = filtered_data[(filtered_data['Year'] >= selected_year_range[0]) & (
    #     filtered_data['Year'] <= selected_year_range[1])]

    # Buat dataframe baru untuk menghitung jumlah total aksi tahun ke tahun per negara
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

    # Tampilkan grafik menggunakan st_echarts
    st_echarts(chart_config, height=500)





    # # Ambil data yang telah difilter sebelumnya
    # filtered_data = df[df['Country'].isin(selected_countries)]

    # # Buat dataframe baru untuk menghitung jumlah total aksi tahun ke tahun per negara
    # total_actions = filtered_data.groupby(['Year', 'Country']).size().reset_index(name='Total Actions')

    # # Buat list kosong untuk menyimpan series garis per negara
    # series_data = []

    # # Loop melalui setiap negara
    # for country in selected_countries:
    #     country_data = total_actions[total_actions['Country'] == country]
    #     series = {
    #         "name": country,
    #         "type": "line",
    #         "data": country_data['Total Actions'].tolist(),
    #         "emphasis": {
    #             "focus": "series",
    #             "lineStyle": {"opacity": 1, "width": 4},
    #             "label": {"show": False},
    #         },
    #         "itemStyle": {"normal": {"opacity": 0.7, "width": 2}},
    #     }
    #     series_data.append(series)

    # # Konfigurasi grafik line race dengan efek hover
    # chart_config = {
    #     "title": {"text": "Total Actions by Year"},
    #     "xAxis": {"type": "category", "data": total_actions['Year'].astype(str).unique().tolist()},
    #     "yAxis": {"type": "value"},
    #     "series": series_data,
    #     "tooltip": {"trigger": "axis"},
    # }

    # # Tampilkan grafik menggunakan st_echarts
    # st_echarts(chart_config, height=500)



# ----------HIST KILLED N WOUNDED----------
with st.container():
    # Membuat histogram menggunakan Plotly Express
    fig = px.histogram(filtered_df, x=['Killed', 'Wounded'], nbins=50,
                    color_discrete_sequence=['lightsalmon', 'lightblue'],
                    labels={'value': 'Jumlah', 'variable': 'Kategori'})

    # Menambahkan judul dan mengatur sumbu x dan y
    fig.update_layout(title='Histogram Jumlah Korban Tewas dan Terluka',
                    xaxis_title='Jumlah Korban',
                    yaxis_title='Jumlah Kejadian')

    # Menampilkan histogram menggunakan Streamlit
    st.plotly_chart(fig, use_container_width=True)





# ----------DATAFRAME----------
with st.container():
    # Menampilkan dataframe
    if st.checkbox("Show The Table"):
        st.write(filtered_df[['Year', 'Month', 'Day', 'Region', 'Country', 'City', 'Latitude', 'Longitude', 'GroupName', 'AttackType',
                              'WeaponType', 'Target', 'TargetType', 'Success', 'Suicide', 'Killed', 'Wounded']].shape)
        
        st.write(filtered_df[['Year', 'Month', 'Day', 'Region', 'Country', 'City', 'Latitude', 'Longitude', 'GroupName', 'AttackType',
                              'WeaponType', 'Target', 'TargetType', 'Success', 'Suicide', 'Killed', 'Wounded']])


with st.container():
    
    # Menghitung total aksi teroris per jenis senjata setelah diterapkan filter
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


with st.container():
    # Mengambil data WeaponType dan menghitung jumlahnya
    weapon_counts = filtered_df['WeaponType'].value_counts().reset_index()
    weapon_counts.columns = ['WeaponType', 'Count']

    # Membuat pie chart menggunakan Plotly Express
    fig = px.pie(weapon_counts, values='Count', names='WeaponType', title='Total Weapon Type')

    # Menampilkan pie chart pada Streamlit
    st.plotly_chart(fig, use_container_width=True)






# # Menampilkan filter untuk kolom 'Year' dan 'Country'
# selected_years = st.multiselect('Select Year(s)', options=[
#                                 'Lihat Seluruh Tahun'] + list(df['Year'].unique()), default=['Lihat Seluruh Tahun'])
# selected_countries = st.multiselect('Select Country(s)', options=[
#                                     'Lihat Seluruh Negara'] + list(df['Country'].unique()), default=['Lihat Seluruh Negara'])






# with st.container():
#     # Mengelompokkan data berdasarkan tahun dan menghitung total korban tewas dan terluka
#     df_grouped = df.groupby('Year')[['Killed', 'Wounded']].sum().reset_index()

#     # Membuat bar chart menggunakan plotly
#     fig = px.bar(df_grouped, x='Year', y=['Killed', 'Wounded'], barmode='group',
#                 title='Total Korban Tewas dan Terluka per Tahun')
#     fig.update_layout(xaxis_title='Tahun', yaxis_title='Jumlah', legend_title='')

#     # Menampilkan bar chart menggunakan Streamlit
#     st.plotly_chart(fig, use_container_width=True)





# with st.container():
#     # Menghitung banyaknya nilai unik dalam kolom 'GroupName'
#     group_count = df['GroupName'].value_counts()

#     # Mengurutkan berdasarkan jumlah kemunculan secara menurun
#     group_count_sorted = group_count.sort_values(ascending=False)

#     # Membuat dataframe baru dengan data yang terurut
#     df_sorted = pd.DataFrame({'GroupName': group_count_sorted.index, 'Count': group_count_sorted.values})

#     # Membuat bar chart menggunakan plotly
#     fig2 = px.bar(df_sorted, x='GroupName', y='Count', 
#                 title='Banyaknya Nilai Unik dalam Kolom GroupName (Terurut)',
#                 labels={'GroupName': 'GroupName', 'Count': 'Count'})
#     fig2.update_layout(xaxis_tickangle=-45)

#     # Menampilkan bar chart
#     st.plotly_chart(fig2, use_container_width=True)







# with st.container():
#         # Menghitung banyaknya nilai unik dalam kolom 'GroupName'
#     group2_count = df['Country'].value_counts()

#     # Membuat bar chart menggunakan plotly
#     fig3 = px.bar(x=group2_count.index, y=group2_count.values, 
#                 title='Negara Dengan Aksi Teorisme Terbanyak',
#                 labels={'x': 'Country', 'y': 'Total'})
#     fig3.update_layout(xaxis_tickangle=-45)

#     # Menampilkan bar chart
#     st.plotly_chart(fig3, use_container_width=True)



# with st.container():
#     # Menghitung banyaknya nilai unik dalam kolom 'TargetType'
#     target_type_count = df['TargetType'].value_counts()

#     # Mengurutkan berdasarkan jumlah kemunculan secara menurun
#     target_type_count_sorted = target_type_count.sort_values(ascending=False)

#     # Membuat histogram menggunakan Plotly
#     fig4 = px.histogram(df, x='TargetType',
#                     title='Target Terorisme',
#                     labels={'TargetType': 'Target Type', 'count': 'Total'},
#                     category_orders={'TargetType': target_type_count_sorted.index})

#     # Mengurutkan histogram dari terbesar
#     fig4.update_xaxes(categoryorder='total descending')

#     # Menampilkan histogram
#     st.plotly_chart(fig4, use_container_width=True)




# with st.container():
#     st.write("Map")
#     m = folium.Map(location=[39.949610, -75.150282], zoom_start=12)
#     folium.Marker(
#         [39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell"
#     ).add_to(m)

#     # call to render Folium map in Streamlit
#     st_data = st_folium(m, width=725)
