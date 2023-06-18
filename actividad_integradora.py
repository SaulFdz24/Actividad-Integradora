import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

st.title('Police Incidents Reports from 2018 to 2020 in San Francisco')
st.markdown('Migue Saúl Fernández Avalos')
df = pd.read_csv('Police_Department_Incident_Reports__2018_to_Present.csv')
st.markdown('The data shown below belongs to incident reports in the city of San Francisco, from the year 2018 to 2020, with details from each case such as date, day of the week, police district, neighborhood in which it happened, type of incident in category and subcategory, exact location, and resolution.')

mapa = pd.DataFrame()
mapa['Date'] = df['Incident Date']
mapa['Day'] = df['Incident Day of Week']
mapa['Police District'] = df['Police District']
mapa['Neighborhood'] = df['Analysis Neighborhood']
mapa['Incident Category'] = df['Incident Subcategory']
mapa['Resolution'] = df['Resolution']
mapa['lat'] = df['Latitude']
mapa['lon'] = df['Longitude']
mapa = mapa.dropna()
st.map(mapa.astype({'lat': 'float32', 'lon': 'float32'}))

subset_data2 = mapa
police_district_input = st.sidebar.multiselect(
    'Police District',
    mapa.groupby('Police District').count().reset_index()['Police District'].tolist()
)
if len(police_district_input) > 0:
    subset_data2 = mapa[mapa['Police District'].isin(police_district_input)]

subset_data1 = subset_data2
neighborhood_input = st.sidebar.multiselect(
    'Neighborhood',
    subset_data2.groupby('Neighborhood').count().reset_index()['Neighborhood'].tolist()
)
if len(neighborhood_input) > 0:
    subset_data1 = subset_data2[subset_data2['Neighborhood'].isin(neighborhood_input)]

subset_data = subset_data1
incident_input = st.sidebar.multiselect(
    'Incident Category',
    subset_data1.groupby('Incident Category').count().reset_index()['Incident Category'].tolist()
)
if len(incident_input) > 0:
    subset_data = subset_data1[subset_data1['Incident Category'].isin(incident_input)]

st.markdown('It is important to mention that any police district can respond to any incident, the neighborhood in which it happened is not related to the police district.')
st.markdown('Crime locations in San Francisco')
st.map(subset_data)

st.markdown('Crimes occurred per day of the week')
colors = ['purple', 'blue', 'green', 'yellow', 'orange', 'red', 'pink']
fig = px.bar(subset_data['Day'].value_counts(), labels={'value': 'Count'},
             title='Crimes occurred per day of the week', color=subset_data['Day'].unique(),
             color_discrete_sequence=colors)
st.plotly_chart(fig)

st.markdown('Crimes occurred per date')
fig2 = px.line(subset_data['Date'].value_counts(), labels={'value': 'Count'},
              title='Crimes occurred per date',color_discrete_sequence=['red'])
st.plotly_chart(fig2)

st.markdown('Type of crimes committed')
fig3 = px.bar(subset_data['Incident Category'].value_counts(), labels={'value': 'Count'},
             title='Type of crimes committed',color_discrete_sequence=px.colors.qualitative.Set2)
fig3.update_layout(height=800)
st.plotly_chart(fig3) 

agree = st.button('Click to see Incident Subcategories')
if agree:
    st.markdown('Subtype of crimes committed')
    st.bar_chart(subset_data['Incident Subcategory'].value_counts())

# Gráfico de barras - Neighborhood distribution
st.markdown('Neighborhood distribution')
neighborhood_counts = subset_data['Neighborhood'].value_counts()
fig5 = px.bar(neighborhood_counts, x=neighborhood_counts.index, y=neighborhood_counts.values,
              color=neighborhood_counts.index, color_discrete_sequence=px.colors.qualitative.Set3)
fig5.update_layout(xaxis={'categoryorder':'total descending'})
st.plotly_chart(fig5)

# Gráfico de barras - Incidents by Police District
st.markdown('Incidents by Police District')
police_district_counts = subset_data['Police District'].value_counts()
fig6 = px.bar(police_district_counts, x=police_district_counts.index, y=police_district_counts.values,
              color=police_district_counts.index, color_discrete_sequence=px.colors.qualitative.Set1)
fig6.update_layout(xaxis={'categoryorder':'total descending'})
st.plotly_chart(fig6)