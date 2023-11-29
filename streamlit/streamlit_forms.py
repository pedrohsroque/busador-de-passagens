from pandas import DataFrame
import streamlit as st

DEFAULT_LIST = [
    {"city":"Belo Horizonte","qty":2},
    {"city":"Brasília","qty":1},
    {"city":"Florianópolis","qty":1},
    {"city":"Memphis","qty":1},
    {"city":"São Paulo","qty":1},
    {"city":"Houston","qty":1},
    {"city":"Caracas","qty":1},
]

def add_city(city: str, cities_list: list, qty: int = None) -> None:
    if not any(city_dict["city"] == city for city_dict in cities_list):
        data = {"city": city}
        if qty:
            data["qty"] = qty
        cities_list.append(data)

def remove_city(city: str, cities_list: list) -> None:
    for city_dict in cities_list:
        if city_dict["city"] == city:
            cities_list.remove(city_dict)

def update_city(city: str, cities_list: list, qty: int = None) -> None:
    if any(city_dict["city"] == city for city_dict in cities_list):
        remove_city(city, cities_list)
    add_city(city, cities_list, qty)

def origin_form(form_id: str, form_title: str, options: DataFrame, data_object: list):
    with st.form(form_id):
        st.write(form_title)
        col1, col2 = st.columns([3,1])
        city = col1.selectbox("Add a city:", options.index)
        qty = col2.selectbox("How many tickets?",range(1,3))
        col1, col2, col3, col4 = st.columns(4)
        add_or_update = col1.form_submit_button("Add/Update")
        remove = col2.form_submit_button("Remove")
        clear = col3.form_submit_button("Clear")
        default = col4.form_submit_button("Default")

    if add_or_update:
        update_city(city, data_object, qty)
    if remove:
        remove_city(city, data_object)
    if clear:
        data_object.clear()
    if default:
        data_object.clear()
        data_object.extend(DEFAULT_LIST)

def destination_form(form_id: str, form_title: str, options: DataFrame, data_object: list):
    with st.form(form_id):
        st.write(form_title)
        city = st.selectbox("Add a city:", options.index)
        col1, col2, col3, col4 = st.columns(4)
        add_or_update = col1.form_submit_button("Add/Update")
        remove = col2.form_submit_button("Remove")
        clear = col3.form_submit_button("Clear")
        select_all = col4.form_submit_button("Select All")

    if add_or_update:
        update_city(city, data_object)
    if remove:
        remove_city(city, data_object)
    if clear:
        data_object.clear()
    if select_all:
        data_object.clear()
        new = options.reset_index()[["City"]].rename({"City":"city"},axis='columns').to_dict('records')
        data_object.extend(new)
