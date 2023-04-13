import streamlit as st

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self, title, type):
        if type == 'selectbox':
            app = st.sidebar.selectbox(
                    title,
                    self.apps,
                    format_func = lambda app: app['title']
                  )
        elif type == 'radio':
            app = st.sidebar.radio(
                    title,
                    self.apps,
                    format_func = lambda app: app['title']
                  )

        app['function']()
