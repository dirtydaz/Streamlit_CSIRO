import streamlit as st
import pandas as pd
import numpy as np
from owid import catalog
import altair as alt

st.title("Greenhouse Gas Emissions")

# Co2
@st.cache_data
def fetch_co2():
    co2 = catalog.find('owid_co2', version = '2023-09-28').load()
    co2_table = co2[['co2','co2_per_capita','ghg_per_capita','energy_per_capita','energy_per_gdp','gdp','population']].copy()
    co2_table.columns = ['CO2 Emissions (Mt)', 'CO2 Emissions per Capita (t)', 'GHG Emissions per Capita (CO2 t)', 'Energy use per Capita (kWh)', 'Energy Use per GDP (kWh per $)', 'GDP (2010 US$)', 'Population (M)']
    countries_to_remove = ['Africa (GCP)', 'Asia (GCP)','Central America (GCP)',
 'Europe (GCP)','European Union (27) (GCP)','French Equatorial Africa (GCP)','French West Africa (GCP)','Kuwaiti Oil Fires (GCP)','Leeward Islands (GCP)',
 'Middle East (GCP)','Non-OECD (GCP)','North America (GCP)','OECD (GCP)','Oceania (GCP)','Panama Canal Zone (GCP)','Ryukyu Islands (GCP)',
 'South America (GCP)','St. Kitts-Nevis-Anguilla (GCP)']
    co2_table.drop(countries_to_remove, level='country', inplace=True)
    return co2_table



co2_table = fetch_co2()
all_countries = co2_table.reset_index()['country'].unique().to_list()
countries_list = ['Australia', 'United States', 'United Kingdom', 'China']
data_options = ['CO2 Emissions (Mt)', 'CO2 Emissions per Capita (t)', 'GHG Emissions per Capita (CO2 t)','Energy use per Capita (kWh)' ]

selected_countries = st.multiselect('Countries or Regions:', all_countries, default=countries_list)
selected_data = st.selectbox('Data type:', data_options)

# Create a mask for each selected country and combine them
mask = np.logical_or.reduce([co2_table.index.get_level_values(0) == country for country in selected_countries])
mask &= (co2_table.index.get_level_values(1) >= 1800) & (co2_table.index.get_level_values(1) <= 2022)

sy_df = co2_table.loc[mask][selected_data]
# co2_unstack = sy_df.unstack(level=0).reset_index()
co2_unstack = sy_df.reset_index()
co2_unstack['year'] = pd.to_datetime(co2_unstack['year'], format='%Y')
co2_unstack.columns = ['Country', 'Year', selected_data]
co2_unstack[selected_data] = co2_unstack[selected_data].astype('float').round(3)
co2_unstack = co2_unstack.dropna()


chart = alt.Chart(co2_unstack).mark_line().encode(
    x=alt.X('Year:T', title='Year'),
    y=alt.Y(f'{selected_data}:Q', title=selected_data),
    color=alt.Color('Country:N', scale=alt.Scale(domain=selected_countries))                  
).properties(
    width='container').interactive()


st.altair_chart(chart, use_container_width=True)



# Create three columns
col1, col2 = st.columns(2)

# Add text to each column
with col1:
    st.write("Global emissions have grown significantly since 1800, sitting at around 37,000 Megatonnes of CO2 in 2022.")

with col2:
    st.write("Whilst global emissions continue to rise, emissions per capita have begun falling in some countries.")






