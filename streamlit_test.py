import streamlit as st
import pandas as pd
import numpy as np
from owid import catalog
from bokeh.plotting import figure
import matplotlib.pyplot as plt
import altair as alt

# Generation Graphing
generation_capacity = catalog.find('renewable_electricity_capacity', version='2023-06-26').load()
aus_generation_capacity = generation_capacity.loc['Australia']
aus_generation_capacity['Biofuels'] = aus_generation_capacity[['bagasse', 'biogas', 'bioenergy','liquid_biofuels','solid_biofuels_and_renewable_waste']].sum(axis=1)
# aus_generation_capacity['Wind'] = aus_generation_capacity[['offshore_wind', 'onshore_wind']].sum(axis=1)
# st.area_chart(aus_generation_capacity)

generation = catalog.find('electricity_generation', version='2023-07-10').load()
# aus_generation = generation.loc['Australia']


pct_to_drop = [col for col in generation.columns if 'pct' in col]
gen_twh = generation.copy()
gen_twh.drop(columns=pct_to_drop, inplace=True)
aus_gen = gen_twh.loc['Australia']
aus_gen_chart = aus_gen[['coal__twh', 'gas__twh', 'solar__twh','hydro__twh',
                         'wind__twh','other_fossil__twh','bioenergy__twh']]

label = aus_gen_chart.columns.tolist()
cleaned_labels = {s.replace("__twh", "") for s in label}

# Bokeh
# gen_fig = figure(
#     title='Electricity Generation by Source',
#     x_axis_label='Year',
#     y_axis_label='TWh',
# )
# gen_fig.varea_stack(stackers=labels, legend_label=labels, source=aus_gen_chart)
# st.bokeh_chart(gen_fig, use_container_width=True)

# Matplotlib
fig, ax = plt.subplots()
ax.stackplot(aus_gen_chart.index, aus_gen_chart.T, labels=aus_gen_chart.columns)
ax.legend(loc='upper left')
st.pyplot(fig)

# Streamlit
# st_stack = aus_gen[['bioene']]
stacked_df = aus_gen_chart.cumsum(axis=1)
st.area_chart(stacked_df)

# Altair
stack_alt = aus_gen_chart.stack().reset_index()
stack_alt.columns = ['Year', 'Origin', 'Generation']

chart = alt.Chart(stack_alt).mark_area().encode(
    x='Year:T',
    y='Generation:Q',
    color='Origin:N',)

st.altair_chart(chart,use_container_width=True)



# Co2
co2 = catalog.find('owid_co2', version = '2023-09-28').load()
co2_table = co2[['co2','co2_per_capita','energy_per_capita','energy_per_gdp','gdp','population']]
co2_countries = co2_table.loc[['Australia','United States', 'United Kingdom', 'China', 'Canada']]
mask = (co2_countries.index.get_level_values(1) >= 1800) & (co2_countries.index.get_level_values(1) <= 2022)
sy_df = co2_countries.loc[mask]
co2_unstack = sy_df.unstack(level=0)


st.line_chart(co2_unstack['co2_per_capita'])

# Energy Use
st.line_chart(co2_unstack['energy_per_capita'])

# Generation Emissions
gen_emissions = catalog.find('emissions', dataset = 'yearly_electricity', version = '2023-07-10').load()
gen_emissions_aus = gen_emissions.loc['Australia']
gen_emissions_aus_chart = gen_emissions_aus[['coal__mtco2', 'gas__mtco2', 'solar__mtco2','hydro__mtco2',
                         'wind__mtco2','other_fossil__mtco2','bioenergy__mtco2']]

# Streamlit
gen_emissions_stacked_df = gen_emissions_aus_chart.cumsum(axis=1)
st.area_chart(gen_emissions_stacked_df)



