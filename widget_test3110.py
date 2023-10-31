import streamlit as st
import pandas as pd
import numpy as np
from owid import catalog
import altair as alt

# Generation Graphing
generation = catalog.find('electricity_generation', version='2023-07-10').load()

pct_to_drop = [col for col in generation.columns if 'pct' in col]
gen_twh = generation.copy()
gen_twh.drop(columns=pct_to_drop, inplace=True)
aus_gen = gen_twh.loc['Australia']
aus_gen_chart = aus_gen[['coal__twh', 'gas__twh', 'solar__twh','hydro__twh',
                         'wind__twh','other_fossil__twh','bioenergy__twh']]

label = aus_gen_chart.columns.tolist()
cleaned_labels = {s.replace("__twh", "") for s in label}

# Altair
stack_alt = aus_gen_chart.stack().reset_index()
stack_alt.columns = ['Year', 'Origin', 'Generation']

chart = alt.Chart(stack_alt).mark_area().encode(
    x='Year:T',
    y='Generation:Q',
    color='Origin:N',)

st.altair_chart(chart,use_container_width=True)