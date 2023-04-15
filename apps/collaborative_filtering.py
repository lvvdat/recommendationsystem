import numpy as np
import pandas as pd

import pickle
import requests
import streamlit as st
from PIL import Image

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
    gensim=gensim.drop(['link','text_clean_stopword'],axis=1)
    data=pd.read_csv('data/Products_ThoiTrangNam_resultALS.csv')
    data2=pd.read_csv('data/Products_ThoiTrangNam_rating_raw.csv',sep="\t")
    return data,gensim,data2

@st.cache_resource
def load_model():
    model = pickle.load(open('models/svd.sav', 'rb'))
    return model

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
    st.subheader("Collaborative Filtering")
    data, gensim,data2 = load_data()
    # model = load_model() 
    user_id=data.user_id.sort_values().unique() 
    customer_id = st.number_input('Type User ID',min_value=min(user_id),max_value=max(user_id))
    if not(customer_id in user_id):
        st.warning('User Id is not correct!', icon="⚠️")  
    else:
        st.success(str(data2[data2.user_id==customer_id]['user'].head(1).values[0])+' has successfully logged in') 
    with st.expander("Setting"):
        similar = st.slider('Select the maximum number of products similar to the above that you want the system to recommend (from 1 to 25)', 1, 25, 25)
        rating = st.slider('Select the minimum number of ratings similar to the above that you want the system to recommend (from 1 to 10)', 0, 10, 0)
    
    if st.button('Recomment') and (customer_id in user_id):
        recommend = data[data.user_id==customer_id ]
        recommendlist=pd.DataFrame({'recommend':recommend.recommendations.values[0].replace("[","").replace("]","").split(","),'rating':recommend.rating.values[0].replace("]","").replace("[","").split(",")})
        recommendlist['recommend']=recommendlist['recommend'].astype(int)
        recommendlist['rating']=recommendlist['rating'].astype(float)
        recommendlist=recommendlist[recommendlist.rating>=(0.5*rating)].head(similar)
        recommendlist['index_product']=recommendlist['recommend'].map(lambda x: gensim[gensim.product_id==x].head(1).index[0] if gensim[gensim.product_id==x].shape[0]>0 else np.NaN)
        recommendlist.dropna(inplace=True)
        if recommendlist.shape[0]==0:
            st.warning('No products were found according to the settings!', icon="⚠️")
        else:
            if recommendlist.shape[0]==1:
                st.info('There is 1 product found')
            else:
                st.info('There are ' +str(recommendlist.shape[0]) +' products found')
                df_filter=gensim.iloc[recommendlist.index_product.values,:]
                display_similar_products(df_filter)
