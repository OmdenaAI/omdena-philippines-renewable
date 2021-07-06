import streamlit as st

class HomePage():
    """
    This class serves as the main homepage for the Data Journal project.
    """
    def __init__(self):
        self.title = "Data Journal"
        self.subtitle = "A Data-Driven Approach to the Visualization of the World"
        self.author = "Neil Ruaro"

    def home_page(self):
        st.title(self.title)
        st.write(self.subtitle)

class Main():
    def __init__(self):
        self.home_page = HomePage()
        self.home_page.home_page()

Main()