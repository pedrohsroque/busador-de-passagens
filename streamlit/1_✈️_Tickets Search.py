import streamlit as st
import pandas as pd

from streamlit_forms import origin_form, destination_form
from main_buscador import listar_menores_precos

def load_city_airport_mapping():
    df = pd.read_csv(
        "data/cities_airports.csv"
    )
    df.set_index("City", inplace=True)
    return df


st.set_page_config(
    page_title="Tickets Search",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None,
)

if "origin_city_list" not in st.session_state:
    st.session_state.origin_city_list = []
if "destination_city_list" not in st.session_state:
    st.session_state.destination_city_list = []

st.title("✈️Tickets Search")
st.title("Origins")
city_airport_mapping = load_city_airport_mapping()

origins = city_airport_mapping[city_airport_mapping["Type"]=="Origin"]
origin_form(
    form_id="Origins",
    form_title="Add the origin cities:",
    options=origins,
    data_object=st.session_state.origin_city_list,
)
if len(st.session_state.origin_city_list) > 0:
    origin_df = pd.DataFrame(st.session_state.origin_city_list)
    origin_df = origin_df.set_index('city').join(city_airport_mapping)
    st.write(origin_df)

st.title("Selected Destinations")
with st.sidebar:
    destinations = city_airport_mapping[city_airport_mapping["Type"]=="Destination"]
    st.session_state.destination_city_list = st.multiselect("Destinations", options=destinations.index)

if len(st.session_state.destination_city_list) > 0:
    destination_df = pd.DataFrame(st.session_state.destination_city_list)
    destination_df = destination_df.rename({0:"city"},axis='columns')
    destination_df = destination_df.set_index('city').join(city_airport_mapping.reset_index().set_index("City"))
    st.dataframe(destination_df, height=36 + 36 * destination_df.shape[0], width=400)

with st.form("Search"):
    search = st.form_submit_button("Buscar")

if search:
    prices = listar_menores_precos(
        lista_origens=list(origin_df["Airport"]),
        lista_destinos=list(destination_df["Airport"]),
        force_refresh=True
    )
    cam = city_airport_mapping.reset_index().set_index('Airport')
    cam = cam.drop(['Type'],axis='columns')
    prices = prices.set_index('origem').join(cam)
    prices = prices.rename(columns={"City": "Origin_City"})
    prices = prices.set_index('destino').join(cam)
    prices = prices.rename(columns={"City": "Destination_City"})
    st.title("Results")
    st.write(prices)
    st.title("Aggregated")
    st.write(prices.groupby("Destination_City")["price"].sum())
