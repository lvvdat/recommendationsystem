import numpy as np
import pandas as pd

import requests 
import streamlit as st

import pickle
from text_cleaner import clean_text, process_emoji, remove_stopword

from PIL import Image
from underthesea import word_tokenize
from gensim.corpora import Dictionary
from gensim import similarities

@st.cache_data
def load_data():
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
    gensim=gensim.drop(['link', 'text_clean_stopword'], axis=1)
    gensim.reset_index(drop=True, inplace=True)

    return gensim

@st.cache_resource
def load_model():
    with open('files/vietnamese-stopwords.txt', 'r', encoding="utf8") as file:
        stopwords = file.read().split('\n')
    tfidf = pickle.load(open("models/tfidf.p", "rb"))
    dictionary = Dictionary.load('models/dictionary')
    indexes = similarities.SparseMatrixSimilarity.load('models/SparseMatrixSimilarity.index')
    return tfidf, dictionary, indexes, stopwords

def display_similar_products(df_filter):
    similar = len(df_filter)
    with st.container():
        k=0
        for i in range(int(round(similar/5+0.5,0))):
            columns = st.columns(5)
            for column in range(5):
                k=k+1
                product = df_filter.iloc[column+5*i]
                cell = columns[column]                
                try:
                    image_url = product['image']
                    if image_url == np.nan:
                        cell.image(Image.open('images/image-not-found-icon.png').resize((150,150)))
                    else:
                        cell.image(Image.open(requests.get(image_url, stream=True).raw).resize((150,150)))
                except:
                    cell.image(Image.open('images/image-not-found-icon.png').resize((150,150)))
                col1,col2=cell.columns([6,4])
                with col1:
                    try:
                        st.write("{:,}₫".format(int(product['price'])))
                    except:
                        st.write(" ")
                with col2:
                    st.write(str(product['rating'])+"★")
                cell.write(product['product_name'])
                cell.write(" ")
                if k==similar:
                    break
            if k==similar:
                break
            

def app():
    st.subheader("Content Based Filtering")
    gensim = load_data()
    tfidf, dictionary, indexes, stopwords = load_model()
    filters = st.radio('Please choose a method:', options=('Select product from the list', 'Enter the product description to search'), index=0)
    if filters == 'Select product from the list':
        col1, col2 = st.columns(2)
        with col1:
            option1 = st.selectbox("Select category",options=gensim['sub_category'].unique())
        with col2:
            option2 = st.selectbox("Select product",options=gensim[gensim.sub_category==option1]['product_name'])
        product = gensim[(gensim['product_name'] == option2) &(gensim['sub_category'] == option1)]    
        selected_id = product['product_id'].values[0]
        col1,col2=st.columns([1,3])
        with col1:
            try:
                image_url = product['image'].values[0]
                st.image(Image.open(requests.get(image_url, stream=True).raw).resize((150,150)))
            except:
                st.image(Image.open('images/image-not-found-icon.png').resize((150,150)))
        with col2:
            st.success(product['product_name'].values[0])
            col3,col4=st.columns(2)
            with col3:
                try:
                    st.code("Price: " + "{:,}₫".format(int(product['price'])))
                except:
                    st.code("Price: ")
            with col4:
                st.code("Rating: "+str(product['rating'].values[0])+" ★")
        with st.expander("Description: "):
            st.write(product['description'].values[0])
        with st.expander("Setting"):
            similar = st.slider('Select the maximum number of products similar to the above that you want the system to recommend (from 1 to 50)', 1, 50, 20)
            rating = st.slider('Select the minimum number of ratings similar to the above that you want the system to recommend (from 1 to 10)', 0, 10, 0)
        if st.button('Recomment'):
            df_filter = gensim.iloc[gensim[gensim.product_id==selected_id]['suggestion'].values[0][:similar]]
            df_filter['rate_suggestion']=gensim[gensim.product_id==selected_id]['rate_suggestion'].values[0][:similar]
            df_filter=df_filter[df_filter['rate_suggestion']>=(0.1*rating)]
            if df_filter.shape[0]==0:
                st.warning('No products were found according to the settings!', icon="⚠️")
            else:
                if df_filter.shape[0]==1:
                    st.info('There is 1 product found')
                else:
                    st.info('There are ' +str(df_filter.shape[0]) +' products found')
                display_similar_products(df_filter)
    else:
        with st.expander("Setting"):
            similar2 = st.slider('Select the maximum number of products similar to the above that you want the system to recommend', 1, 50, 20)
            rating2 = st.slider('Select the minimum number of ratings similar to the above that you want the system to recommend (from 1 to 10)', 0, 10, 0)
        text = st.text_input('Enter a product name to search:', value='', max_chars=None, key=None, type='default')
        if text != '':
            text = clean_text(text)
            text = process_emoji(text)
            text = word_tokenize(text, format="text")
            text = remove_stopword(text, stopwords)
            kw_vector = dictionary.doc2bow(text.split()) 
            df_sim = pd.DataFrame(indexes[tfidf[kw_vector]])
            df_sim=df_sim[df_sim.iloc[:,0]>=(0.1*rating2)]
            df_sim=df_sim.sort_values(0, ascending=False)           
            df_filter = gensim.iloc[df_sim.head(similar2).index]
            if df_filter.shape[0]==0:
                st.warning('No products were found according to the settings!', icon="⚠️")
            else:
                if df_filter.shape[0]==1:
                    st.info('There is 1 product found')
                else:
                    st.info('There are ' +str(df_filter.shape[0]) +' products found')
                display_similar_products(df_filter)
