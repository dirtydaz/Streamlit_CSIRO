import streamlit as st
import pandas as pd
import numpy as np
from owid import catalog
import altair as alt

# Calculate the year-on-year percentage change for each 'Gen' column.
@st.cache_data
def get_generation():
    generation = catalog.find('electricity_generation', version='2023-07-10').load()

    pct_to_drop = [col for col in generation.columns if 'pct' in col]
    gen_twh = generation.copy()
    gen_twh.drop(columns=pct_to_drop, inplace=True)
    aus_gen = gen_twh.loc['Australia']
    aus_gen_chart = aus_gen[['coal__twh', 'gas__twh', 'solar__twh','hydro__twh',
                            'wind__twh','other_fossil__twh','bioenergy__twh']]
    aus_gen_chart.columns = ['Coal', 'Gas', 'Solar', 'Hydro', 'Wind', 'Other Fossil', 'Bioenergy']

    change_df = pd.DataFrame( columns=aus_gen_chart.columns)
    for column in aus_gen_chart.columns:

        change_df[column] = aus_gen_chart[column].pct_change()

    pct_df = change_df.stack().reset_index()
    pct_df.columns = ['Year', 'Source', 'YoY % Change']
    return pct_df

df = get_generation()

chart = alt.Chart(df).mark_line().encode(
    x='Year:O',  
    y=alt.Y('YoY % Change:Q', axis=alt.Axis(format='%')),  
    color='Source:N',  
    tooltip=['Year', 'YoY % Change', 'Source']
).interactive()

st.altair_chart(chart, use_container_width=True)
