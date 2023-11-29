import streamlit as st
import pandas as pd

from main_buscador import get_estimation


def generate_url(data_inicio, data_fim, origem, destino):
    return f"https://www.decolar.com/shop/flights/results/roundtrip/{origem}/{destino}/{data_inicio}/{data_fim}/1/0/0/NA/NA/NA/NA/NA?from=SB&di=1-0"


st.set_page_config(
    page_title="Estimation",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None,
)

prices = pd.read_csv("data/cheapest/prices.csv")
st.write(prices)

with st.form("Estimation"):
    get_details = st.form_submit_button("Get Details")

if get_details:
    st.write("Under development...")
    # df_prices_resumido = prices.drop_duplicates(subset=["start_date", "end_date"])
    # st.write(df_prices_resumido)
    # for idx_referencia, item_referencia in df_prices_resumido.iterrows():
    #     for idx, item in prices.iterrows():
    #         if idx != idx_referencia:
    #             url = generate_url(
    #                 item["start_date"],
    #                 item["end_date"],
    #                 item["origem"],
    #                 item["destino"],
    #             )
    #             st.write(url)
