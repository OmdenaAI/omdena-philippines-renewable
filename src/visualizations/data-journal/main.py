import streamlit as st
import pages.page1 as p1
import pages.page2 as p2

class HomePage:
    """
    This class serves as the main homepage for the Data Journal project.
    """
    
    def __init__(self):
        self.title = "Data Journal"
        self.subtitle = "Documenting everything from Data Processing to Data Modeling"
        self.author = "Neil Ruaro"
        self.PAGES = {
            "Page 1" : p1.Page1,
            "Page 2" : p2.Page2,
        }

    def home_page(self):
        st.title(self.title)
        st.write(self.subtitle)
        st.sidebar.title('Pages')
        selection = st.sidebar.radio("Go to", list(self.PAGES.keys()))
        page = self.PAGES[selection]
        page.app()

class Main():
    def __init__(self):
        self.home_page = HomePage()
        self.home_page.home_page()

Main()