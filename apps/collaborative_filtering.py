import numpy as np
import pandas as pd

import pickle
import requests
import streamlit as st

from PIL import Image

@st.cache_data
def load_data():
    data = pd.read_csv('data/Products_ThoiTrangNam_raw.csv')
    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)
    return data

@st.cache_resource
def load_model():
    model = pickle.load(open('models/svd.mdl', 'rb'))
    return model

def display_similar_products(df_filter):
    similar = len(df_filter)
    with st.container():
        columns = st.columns(similar)
        for column in range(similar):
            cell = columns[column]
            product = df_filter.iloc[column]

            try:
                image_url = product['image']
                if image_url == np.nan:
                    cell.image(Image.open('images/image-not-found-icon.png'))
                else:
                    cell.image(Image.open(requests.get(image_url, stream=True).raw))
            except:
                cell.image(Image.open('images/image-not-found-icon.png'))

            cell.write(product['product_name'])

def app():
    st.subheader("Collaborative Filtering")

    data = load_data()
    model = load_model()
    customer_id = st.number_input('Enter customer id:', min_value=1, max_value=650636, value=1, step=1)
    recommend = pd.DataFrame({'product_id':data.product_id.unique()})

    similar = st.slider('Select maximum number of products similar to the above that you want system to recommend (from 1 to 5)', 1, 5, 3)
    st.write(f'Maximum number of products to recommend: {similar}')

    if st.button('Recomment'):
        filter_str = f'user_id={customer_id}'
        recommend[filter_str] = recommend['product_id'].map(lambda x: model.predict(customer_id, x).est)
        df_filter = data[data.product_id.isin(recommend.sort_values(filter_str,ascending=False).head(similar)['product_id'].values)]
        st.write(f'There are {len(df_filter)} products found')
        display_similar_products(df_filter)
