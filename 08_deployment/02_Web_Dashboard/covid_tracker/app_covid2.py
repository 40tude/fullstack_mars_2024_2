# docker run -it --rm -v "$(pwd):/home/app" -e PORT=80 -p 4000:80 jedha/streamlit-sample-app bash
# streamlit run app.py --server.port 80

import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import pathlib 
import datetime
from datetime import timedelta

k_nrows = 10_000
k_file_in = "./assets/data.csv"

@st.cache
def load_data(nrows=k_nrows):
  data_in = pd.read_csv(k_file_in, nrows=k_nrows)
  data_in = data_in[(data_in["cases"]>=0) & (data_in["deaths"]>=0)]
  data_in["date"] = data_in["dateRep"].apply(lambda x: pd.to_datetime(x, format="%d/%m/%Y"))
  # data_in.drop(columns=["dateRep", "day", "month", "year"], inplace=True)
  data_in = data_in[["date", "cases", "deaths", "countriesAndTerritories", "countryterritoryCode"]]
  data_in.sort_values("date", ascending=True, inplace=True)
  data_in.set_index('date', inplace=True)
  data_in["sma_cases"] = data_in["cases"].rolling(7).mean()
  return data_in


## Config
st.set_page_config(
  page_title  = "my_covid_tracker",
  page_icon   = "",
  layout      = "wide"
)


# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------

st.markdown("# My Covid Tracker")
st.markdown("## Worldwide")


st.markdown("### Cumulatives cases")

dataset = load_data()
df  = dataset[["cases", "sma_cases"]].groupby(dataset.index.date).sum()
df["cum_cases"] = df["cases"].cumsum()



fig = px.line(df, x=df.index, y="cum_cases")
fig.update_layout(
  yaxis_title="Cases",
  xaxis_title="Date",
  title="Cumulative cases over time"
)
st.plotly_chart(fig, use_container_width=True)

fig = px.area(df, x=df.index, y="cum_cases")
fig.update_layout(
  yaxis_title="Cases",
  xaxis_title="Date",
  title="Cumulative cases over time"
)
st.plotly_chart(fig, use_container_width=True)


st.markdown("### New cases")

# df["sma_cases"] = df["cases"].rolling(7).mean()
fig = px.line(df, x=df.index, y=["cases", "sma_cases"])
fig.update_layout(
  yaxis_title="Cases",
  xaxis_title="Date",
  title="Cumulative cases over time"
)
st.plotly_chart(fig, use_container_width=True)



# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
# st.subheader("Per country")
st.markdown("## Per country")


@st.cache
def get_country_data(country):
  df_country = dataset[(dataset["countriesAndTerritories"]==country)]
  df_country.sort_values("date", ascending=True, inplace=True)
  df_country["sma_cases"] = df_country["cases"].rolling(7).mean()
  df_country["sma_deaths"] = df_country["deaths"].rolling(7).mean()
  return df_country

country = st.selectbox("Select a country", dataset["countriesAndTerritories"].sort_values().unique())
df_country = get_country_data(country)

date_of_interrest = st.date_input("Select a date : ", datetime.date(2022, 1, 14))
date_of_interrest = pd.to_datetime(date_of_interrest, format="%Y-%m-%d")
date_before       = date_of_interrest - timedelta(days=1)

avg_cases_today       = df_country.loc[date_of_interrest,"sma_cases"]
avg_cases_days_before = df_country.loc[date_before,"sma_cases"]
st.write(f"Rate of growth :  {100*(avg_cases_today/avg_cases_days_before - 1):.2f} %")


col1, col2 = st.columns(2)
if (country):
  with col1:
    st.markdown('### Cases')
    fig = px.line(df_country, x=df_country.index, y=["cases", "sma_cases"])
    fig.update_layout(
      yaxis_title="Cases",
      xaxis_title="Date",
      title="Cases over time"
    )
    st.plotly_chart(fig, use_container_width=True)

  with col2:
    st.markdown('### Deaths')
    fig = px.line(df_country, x=df_country.index, y=["deaths", "sma_deaths"])
    fig.update_layout(
      yaxis_title="Deaths",
      xaxis_title="Date",
      title="Deaths over time"
    )
    st.plotly_chart(fig, use_container_width=True)


# col1, col2 = st.columns(2)
# with col1:
#   fig = px.choropleth(dataset, locations="countryterritoryCode", color="cases", hover_name="countriesAndTerritories", color_continuous_scale="ylgnbu", scope="europe", range_color=(0, 200_000),)
#   fig.update_geos(fitbounds="locations")
#   fig.update_layout(margin={"r":0, "t":0, "l":0, "b":0})
#   st.plotly_chart(fig, use_container_width=True)
  
# with col2:
#   fig = px.choropleth(dataset, locations="countryterritoryCode", color="deaths", hover_name="countriesAndTerritories", color_continuous_scale="ylgnbu",scope="europe", range_color=(0, 2000),)
#   fig.update_geos(fitbounds="locations")
#   fig.update_layout(margin={"r":0, "t":0, "l":0, "b":0})
#   st.plotly_chart(fig, use_container_width=True)




# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
empty_space, footer = st.columns([1, 2])
with empty_space:
  st.write("")

with footer:
  st.markdown("""
© 2024 - All right reserved - 🏍️
  """)