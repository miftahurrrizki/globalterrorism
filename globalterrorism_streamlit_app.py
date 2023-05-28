import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import random
import folium
from streamlit_folium import st_folium
from streamlit_folium import folium_static






df = pd.read_csv(r"C:\Users\mfthr\anaconda3\envs\streamlit\Belajar Miftah\globalterrorism.csv", encoding="latin-1")

#pre-processing

df.rename(columns={'iyear': 'Year', 'imonth': 'Month', 'iday': 'Day', 'country_txt': 'Country', 'region_txt': 'Region', 'city': 'City', 'latitude': 'Latitude', 'longitude': 'Longitude', 'success': 'Success', 'suicide': 'Suicide',
          'attacktype1_txt': 'AttackType', 'target1': 'Target', 'nkill': 'Killed', 'nwound': 'Wounded', 'summary': 'Summary', 'gname': 'GroupName', 'targtype1_txt': 'TargetType', 'weaptype1_txt': 'WeaponType', 'motive': 'Motive'}, inplace=True)
df = df[['Year', 'Month', 'Day', 'Region', 'Country', 'City', 'Latitude', 'Longitude', 'GroupName', 'AttackType',
         'WeaponType', 'Target', 'TargetType', 'Success', 'Suicide', 'Killed', 'Wounded','Motive','Summary']]

df.dropna(subset=['Longitude'], inplace=True)
df.dropna(subset=['City'], inplace=True)
df['Target'].fillna('Unknown', inplace=True)
df['Killed'].fillna(0, inplace=True)
df['Wounded'].fillna(0, inplace=True)
df = df.drop('Motive',axis=1)
df = df.drop('Summary',axis=1)


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
    st.subheader('Total Victims:')
    st.subheader(int(total_victims))

with column3:
    st.subheader('Total Terrorist Group:')
    st.subheader(len(total_groupnamex))



# sidebar
st.sidebar.header("Silahkan Filter Disini:")
selected_countries = st.sidebar.multiselect('Select Country(s)', options=[
    'Lihat Seluruh Negara'] + list(df['Country'].unique())) #, default=['Lihat Seluruh Negara'])

selected_years = st.sidebar.multiselect('Select Year(s)', options=[
    'Lihat Seluruh Tahun'] + list(df['Year'].unique())) #, default=['Lihat Seluruh Tahun'])

# Menerapkan filter pada dataframe berdasarkan pilihan pengguna
if 'Lihat Seluruh Negara' in selected_countries:
    filtered_df = df[df['Country'].isin(df['Country'])]
elif 'Lihat Seluruh Tahun' in selected_years:
    filtered_df = df[df['Year'].isin(df['Year'])]
else:
    filtered_df = df[
        (df['Year'].isin(selected_years)) &
        (df['Country'].isin(selected_countries))
    ]



# #display tabel
# if st.checkbox("Show The Table"):
#     st.write(filtered_df.shape)
#     st.dataframe(filtered_df, use_container_width=True)

# # Menerapkan filter pada dataframe berdasarkan pilihan pengguna
# if 'Lihat Seluruh Negara' in selected_countries:
#     filtered_df = df[df['Country'].isin(selected_countries)]
# elif 'Lihat Seluruh Tahun' in selected_years:
#     filtered_df = df[df['Year'].isin(selected_years)]
# else:
#     filtered_df = df[
#         (df['Year'].isin(selected_years)) &
#         (df['Country'].isin(selected_countries))
#     ]


# Menghitung total aksi teroris per negara setelah diterapkan filter
country_counts = filtered_df['Country'].value_counts()

# Mengurutkan berdasarkan total aksi teroris secara menurun
country_counts_sorted = country_counts.sort_values(ascending=False)

# Membuat dataframe baru dengan data yang terurut
df_sorted = pd.DataFrame({'Country': country_counts_sorted.index,
                         'Total Attacks': country_counts_sorted.values})

# Membuat histogram menggunakan plotly
fig = px.histogram(df_sorted, x='Country', y='Total Attacks',
                   title=f'Total Aksi Teroris per Negara - Years: {", ".join(str(year) for year in selected_years)}, Countries: {", ".join(selected_countries)}',
                   labels={'Country': 'Negara',
                           'Total Attacks': 'Total Aksi Teroris'},
                   nbins=len(df_sorted))

# Mengurutkan histogram dari terbesar
fig.update_xaxes(categoryorder='total descending')

# Menampilkan histogram menggunakan Streamlit
st.plotly_chart(fig, use_container_width=True)


with st.container():
    # Menghitung jumlah aksi terorisme dari tahun ke tahun
    terrorism_count = filtered_df.groupby('Year').size()

    # Membuat line chart menggunakan matplotlib
    plt.figure(figsize=(12, 6))
    plt.plot(terrorism_count.index, terrorism_count.values, marker='o')
    plt.title('Perkembangan Jumlah Aksi Terorisme dari Tahun ke Tahun')
    plt.xlabel('Tahun')
    plt.ylabel('Jumlah Aksi Terorisme')
    plt.grid(True)

    # Menampilkan line chart menggunakan Streamlit
    st.pyplot(plt)


# # Menerapkan filter pada dataframe berdasarkan pilihan pengguna
# if 'Lihat Seluruh Negara' in selected_countries:
#     filtered_df = df[df['Country'].isin(selected_countries)]
# elif 'Lihat Seluruh Tahun' in selected_years:
#     filtered_df = df[df['Year'].isin(selected_years)]
# else:
#     filtered_df = df[
#         (df['Year'].isin(selected_years)) &
#         (df['Country'].isin(selected_countries))
#     ]


# Menampilkan dataframe
st.write(filtered_df[['Year', 'Month', 'Day', 'Region', 'Country', 'City', 'Latitude', 'Longitude', 'GroupName', 'AttackType',
                          'WeaponType', 'Target', 'TargetType', 'Success', 'Suicide', 'Killed', 'Wounded']])



with st.container():
    'Map Persebaran Aksi Terorisme'
    # Mendapatkan nilai rata-rata latitude dan longitude dari data yang telah difilter
    avg_latitude = filtered_df['Latitude'].mean()
    avg_longitude = filtered_df['Longitude'].mean()

    # Membuat peta dengan zoom awal pada titik latitude dan longitude yang dipilih
    map = folium.Map(location=[avg_latitude, avg_longitude], zoom_start=3)

    # Menambahkan marker pada peta untuk setiap baris dalam dataframe yang memiliki data koordinat
    for index, row in filtered_df.iterrows():
        if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']):
            location = [row['Latitude'], row['Longitude']]
            total_casualties = row['Killed'] + row['Wounded']
            group_name = row['GroupName']

            tooltip = f"Group: {group_name}<br>Total Casualties: {total_casualties}"

            folium.Marker(location, tooltip=tooltip).add_to(map)

    # Menampilkan peta di Streamlit
    folium_static(map)






# if st.container():
#     # Mengelompokkan data berdasarkan tahun dan menghitung total korban tewas dan terluka
#     df_dipilih_grouped = df_dipilih.groupby('Year')[['Killed', 'Wounded']].sum().reset_index()

#     # Membuat bar chart menggunakan plotly
#     fig = px.bar(df_dipilih_grouped, x='Year', y=['Killed', 'Wounded'], barmode='group',
#                 title='Total Korban Tewas dan Terluka per Tahun')
#     fig.update_layout(xaxis_title='Tahun', yaxis_title='Jumlah', legend_title='')

#     # Menampilkan bar chart menggunakan Streamlit
#     st.plotly_chart(fig, use_container_width=True)


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
