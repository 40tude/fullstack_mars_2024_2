# docker run -it --rm -v "$(pwd):/home/app" -e PORT=80 -p 4000:80 jedha/streamlit-sample-app bash
# streamlit run app.py --server.port 80


import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

### Config
st.set_page_config(page_title="Covid Tracker", page_icon="🦠 ", layout="wide")

DATE_COLUMN = "dateRep"
DATA_URL = (
    "https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/ECDC_data.csv"
)

### App
st.title("Zoubida - Covid Tracker")
st.markdown(
    "👋 Hello there! Welcome to this simple covid tracker app. We simply track the evolution of cases accross the world. Data comes from the European Centre for Disease Prevention and Control (ECDC)"
)
st.markdown(
    "Check out data here: [Data on the daily number of new reported COVID-19 cases and deaths by EU/EEA country](https://www.ecdc.europa.eu/en/publications-data/data-daily-new-cases-covid-19-eueea-country)"
)
st.caption("At the moment of this app, data was lastly collected on December 25th 2021")


@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN], dayfirst=True)

    return data


data_load_state = st.text("Loading data...")
data = load_data(None)

if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(data)

### World analysis
st.subheader("World Analysis")
world = data.groupby("dateRep").sum().reset_index()
world_cases = world.loc[:, ["dateRep", "cases"]]

#### cases - cumulated
st.markdown("#### Cumulated cases")
world_cases["cumulated_cases"] = world_cases["cases"].cumsum()

world_fig1 = go.Figure(
    go.Scatter(
        x=world_cases["dateRep"],
        y=world_cases["cumulated_cases"],
        fill="tozeroy",
        name="Cumulated cases",
    )
)

st.plotly_chart(world_fig1, use_container_width=True)

#### cases - new
st.markdown("#### New cases")
### Remove outlier (from Jan 3rd)
world_cases = world_cases.iloc[21:, :]
world_cases["moving_average"] = (
    world_cases["cases"].rolling(window=7, min_periods=1).mean()
)

world_fig2 = go.Figure()
world_fig2.add_trace(
    go.Scatter(x=world_cases["dateRep"], y=world_cases["cases"], name="New cases")
)

world_fig2.add_trace(
    go.Scatter(
        x=world_cases["dateRep"], y=world_cases["moving_average"], name="7-day average"
    )
)

world_fig2.update_xaxes(showgrid=False)
world_fig2.update_yaxes(showgrid=False)

st.plotly_chart(world_fig2, use_container_width=True)

### Country analysis
st.subheader("Country Analysis")
countries = data["countriesAndTerritories"].unique()
country = st.selectbox("Which country would you like to see?", countries)


### Number of cases
cases_per_country = data[data["countriesAndTerritories"] == country].loc[
    :, ["dateRep", "cases"]
]
cases_per_country = cases_per_country.sort_values("dateRep", ascending=True).iloc[1:, :]
# cases_per_country.set_index("dateRep", inplace = True)
# cases_per_country["moving_average"] = cases_per_country.rolling(window=7, min_periods=1).mean()
cases_per_country["moving_average"] = (
    cases_per_country.set_index("dateRep").rolling(window=7, min_periods=1).mean()
)

#### Growth rate
current_growth_rate = (
    cases_per_country["moving_average"].iloc[-1]
    / cases_per_country["moving_average"].iloc[-2]
)
previous_growth_rate = (
    cases_per_country["moving_average"].iloc[-2]
    / cases_per_country["moving_average"].iloc[-3]
)
growth_rate_evolution = current_growth_rate - previous_growth_rate

content, empty_space = st.columns([3, 2])
with empty_space:
    st.empty()

with content:
    st.metric(
        "Current growth rate",
        np.round(current_growth_rate, 3),
        np.round(growth_rate_evolution, 3),
        "inverse",
    )
    st.caption(
        "Growth rate compares the average number of cases of today to the average number of cases of yesterday. If growth rate > 1 - the virus is spreading. If growth rate < 1 - the wave is slowing down"
    )
#####

col1, col2 = st.columns(2)

fig1 = go.Figure()
fig1.add_trace(
    go.Scatter(
        x=cases_per_country["dateRep"],
        y=cases_per_country["cases"],
        name="Number of cases per day",
    )
)

fig1.add_trace(
    go.Scatter(
        x=cases_per_country["dateRep"],
        y=cases_per_country["moving_average"],
        name="7-day average",
    )
)

fig1.update_xaxes(showgrid=False)
fig1.update_yaxes(showgrid=False)

with col1:
    st.markdown("#### Positive cases")
    st.plotly_chart(fig1, use_container_width=True)

### Number of deaths
deaths_per_country = data[data["countriesAndTerritories"] == country].loc[
    :, ["dateRep", "deaths"]
]
deaths_per_country = deaths_per_country.sort_values("dateRep", ascending=True).iloc[
    1:, :
]
deaths_per_country["moving_average"] = (
    deaths_per_country.set_index("dateRep").rolling(window=7, min_periods=1).mean()
)

fig2 = go.Figure()
fig2.add_trace(
    go.Scatter(
        x=deaths_per_country["dateRep"],
        y=deaths_per_country["deaths"],
        name="Number of deaths per day",
    )
)

fig2.add_trace(
    go.Scatter(
        x=deaths_per_country["dateRep"],
        y=deaths_per_country["moving_average"],
        name="7-day average",
    )
)

fig2.update_xaxes(showgrid=False)
fig2.update_yaxes(showgrid=False)

with col2:
    st.markdown("#### Deaths")
    st.plotly_chart(fig2, use_container_width=True)
