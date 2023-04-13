import numpy as np
import pandas as pd

import requests
import streamlit as st

from PIL import Image

def recommendations_array(x):
    import numpy as np
    x = x.replace("[","").replace("]","").replace("Row(product_id=","").replace("rating=","").replace(")","")
    x = x.split(',')
    id=[]
    for i in range(np.size(x)):
        if i%2==0:
            id.append(int(x[i]))
    return id

@st.cache_data
def load_data():
    data = pd.read_csv('data/Products_ThoiTrangNam_raw.csv')
    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)

    recommend = pd.read_csv('data/Products_ThoiTrangNam_rating_recommendForAllItems_ALS.csv', index_col=0, converters={"recommendations":recommendations_array})
    return data, recommend

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

    data, recommend = load_data()
    customer_id = st.number_input('Enter customer id:', min_value=1, max_value=650636, value=1, step=1)
    similar = st.slider('Select maximum number of products similar to the above that you want system to recommend (from 1 to 5)', 1, 5, 3)
    st.write(f'Maximum number of products to recommend: {similar}')
    st.dataframe(recommend)

    if st.button('Recomment'):
        df_filter = data[data.product_id.isin(recommend[recommend.user_id==customer_id]['recommendations'].values[0][:similar])]
        st.write(f'There are {len(df_filter)} products found')
        display_similar_products(df_filter)
