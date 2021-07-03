import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import folium
from streamlit_folium import folium_static 
import warnings
warnings.filterwarnings('ignore')

import streamlit.components.v1 as components

import random


## Modeling imports
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier 
from sklearn.metrics import accuracy_score,roc_curve, auc, confusion_matrix, classification_report
from sklearn.metrics.pairwise import euclidean_distances, manhattan_distances, cosine_similarity

from sklearn.preprocessing import MinMaxScaler


## import external


## API
import time

import requests

## Extra configs
st.set_page_config(page_title="Geo", page_icon="🌎", layout="wide", initial_sidebar_state="expanded")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
## End of Extra configs

## Modular pages
#import page_test
#page_test.hello()


# Example how to load Images
# pip install pillow
from PIL import Image
#image = Image.open('./images/sunrise.jpg.jpg')
#st.image(image, caption='Sunrise by the mountains', use_column_width=False, width=350)
# end of Image load example

###### DATA and Modeling Functions
scalerMinmax = MinMaxScaler()
scaler = MinMaxScaler()

###### DATA Loading
# Create the 6 data frames per csv file (Upload the CSV files first!)
# df_file = pd.read_csv("./data/file.csv")

## DATA





###### END OF DATA Laoding

###### Variables
## 
            
## Data Processing


feature_cols = []

###### End of Variables

## Pages as def functions

## Anyone wants a loadable setup? multiple pages?
## Modular pages
#import page_test
#page_test.hello()


## Site Wide Contents
### Main
#Oops Let's Do it Again")

### Side bars
st.sidebar.title("Sprint 04")

#image = Image.open('./images/logo.jpg')
#st.sidebar.image(image, caption='', use_column_width=False, width=290)

## Radio
nav = st.sidebar.radio("Navigation ", 
               (
                    'Presentation',
                    'App'
               ))


## Functions

          
### Pages
def page_home():
    st.title("Home")
    st.markdown("""
## Our Client
""")
    image = Image.open('')
    st.image(image, caption='', use_column_width=False, width=350)
    st.markdown("""
## Objectives

- a
    """)

def page_prezi():
    components.html(
        '<frame></iframe>' 
            ,height=640, width=1630)

    st.markdown("""
## Objectives

- a
    """)
    
def page_app():
    components.html(
        '<frame></iframe>' 
            ,height=640, width=1630)

    st.markdown("""
## Objectives

- a
    """)
        
 
        
    
### Page switching
#data = load_data_pred()

if (nav == 'Presentation'):
    page_prezi()
elif (nav == 'App'):
    page_app()


## Credits if you like
st.sidebar.markdown("""
## The Team

""")
