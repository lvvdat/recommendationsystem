import numpy as np
import pandas as pd

import requests
import streamlit as st

import pickle
from text_cleaner import clean_text, process_emoji, remove_stopword

from PIL import Image
from underthesea import word_tokenize
from gensim.corpora import Dictionary
from gensim import corpora, models, similarities

@st.cache_data
def load_data():
    data = pd.read_csv('data/Products_ThoiTrangNam_raw.csv')
    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)

    def convert_array_int(x):
        x=x[x.index("[")+1:]
        x=x[:x.index("]")]
        x=x.split(',') 
        x=[int(item) for item in x]
        return x

    def convert_array_float(x):
        import regex
        x=x[x.index("[")+1:]
        x=x[:x.index("]")]
        if x.find(',')>-1:
            x=x.split(',')
            x=[float(item) for item in x]
        else:
            x=x.replace("\n"," ")
            x=regex.sub(r'\s+', ' ', x).strip()
            x=x.split(' ')
            x=[float(item) for item in x]
        return x

    gensim = pd.read_csv('data/Products_ThoiTrangNam_resultGensim.csv', index_col=0, converters={"suggestion": convert_array_int,"rate_suggestion":convert_array_float})
    gensim.dropna(inplace=True)
    gensim.reset_index(drop=True, inplace=True)

    return data, gensim

@st.cache_resource
def load_model():
    with open('files/vietnamese-stopwords.txt', 'r', encoding="utf8") as file:
        stopwords = file.read().split('\n')
    tfidf = pickle.load(open("models/tfidf.mdl", "rb"))
    dictionary = Dictionary.load('models/dictionary.mdl')
    indexes = similarities.SparseMatrixSimilarity.load('models/SparseMatrixSimilarity.mdl')
    return tfidf, dictionary, indexes, stopwords

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
    st.subheader("Content Based Filtering")

    data, gensim = load_data()
    tfidf, dictionary, indexes, stopwords = load_model()

    filters = st.radio('Please choose a method:', options=('Select product from the list', 'Enter the product description to search'), index=0)

    if filters == 'Select product from the list':
        option = st.selectbox(
            "Select product to view:",
            options=data['product_name']
        )

        product = data[data['product_name'] == option]    
        selected_id = product['product_id'].values[0]

        try:
            image_url = product['image'].values[0]
            st.image(Image.open(requests.get(image_url, stream=True).raw))
        except:
            st.image(Image.open('images/image-not-found-icon.png'))

        similar = st.slider('Select maximum number of products similar to the above that you want system to recommend (from 1 to 5)', 1, 5, 3)
        st.write(f'Maximum number of products to recommend: {similar}')

        if st.button('Recomment'):
            df_filter = gensim.iloc[gensim[gensim.product_id==selected_id]['suggestion'].values[0][:similar]]
            display_similar_products(df_filter)
    else:
        text = st.text_input('Enter a product name to search:', value='', max_chars=None, key=None, type='default')

        if text != '':
            text = clean_text(text)
            text = process_emoji(text)
            text = word_tokenize(text, format="text")
            text = remove_stopword(text, stopwords)

            kw_vector = dictionary.doc2bow(text.split())
            df_sim = pd.DataFrame(indexes[tfidf[kw_vector]])
            df_filter = data.iloc[df_sim.sort_values(0, ascending=False).head(5).index]

            display_similar_products(df_filter)
