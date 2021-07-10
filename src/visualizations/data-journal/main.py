import streamlit as st
import pages.page1 as p1
import pages.page2 as p2

class HomePage:
    """
    This class serves as the main homepage for the Data Journal project.
    """
    
    def __init__(self):
        self.author = "Neil Ruaro"
        self.PAGES = {
            "Estimating Energy Availability" : p1.Page1,
            "Page 2" : p2.Page2,
        }

    def home_page(self):
        st.sidebar.title('Tasks')
        selection = st.sidebar.radio("Go to", list(self.PAGES.keys()))
        page = self.PAGES[selection]
        page.app()

class Main():
    def __init__(self):
        self.home_page = HomePage()
        self.home_page.home_page()

Main()