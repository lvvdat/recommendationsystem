import streamlit as st


def app():
    st.subheader('Product Overview')
    st.image('images/about_banner.jpg')
    st.write('#### Business Understanding')
    st.write('Shopee is a top 1 e-commerce website in Vietnam and Southeast Asia and an "all in one" commerce ecosystem.')
    st.write('Shopee has implemented many utilities to enhance user experience and they want to build more.')
    st.write('**Objective/problem**: Build a Recommendation System for one or several groups of goods on shopee.vn to help suggest and recommend relevant products to users/customers:')
    st.markdown('''
        * Content-based filtering
        * Collaborative filtering
    ''')
    st.write('#### Collaborative Filtering')
    st.write('Collaborative filtering is a method of making automatic predictions (filtering) about the interests of a user by collecting preferences or taste information from many users (collaborating).')
    st.write("The underlying assumption of the collaborative filtering approach is that if a person A has the same opinion as a person B on an issue, A is more likely to have B's opinion on a different issue x than to have the opinion on x of a person chosen randomly.")
    st.write('Collaborative filtering is commonly used for recommender systems. These techniques aim to fill in the missing entries of a user-item association matrix.')
    st.write('Two general approaches to collaborative filtering are:')
    st.markdown('''
        * Memory-based: approaches that calculate similarity between users or items directly.
        * Model-based: approaches that build a model (e.g. matrix factorization) of user, item and their associations.
    ''')
    st.write('#### Content-based Filtering')
    st.write('Content-based filtering is a technique used to recommend products to users based on their previous purchases or viewed items.')
    st.write("Content-based filtering is based on a description of the item and a profile of the user's preferences.")
    st.write('These descriptions are created by the item creator and the user.')
    st.write('The recommender system will try to recommend items that are similar to those that the user liked in the past (or is examining in the present).')


