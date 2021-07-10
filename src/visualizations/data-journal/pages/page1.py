import streamlit as st

class Page1:
    def __init__(self):
        self.app()

    def app():
        st.title('Estimating Energy Availability')
        st.title('Task:')
        st.write('Extracting PV Power Potential using Single Diode Formula, KMeans Algorithm, Gaussian Mixture Model, and DBSCAN Algorithm')
        st.write('Solar data from 41,933 barangays in the Philippines were processed and analyzed using zonal statistics and QGIS')
        st.write('From there the data was used to estimate energy availability with the above methods.')
        st.write('KMeans, Gaussian Mixture, and DBSCAN were then used to get the silhouette score to measure which model to used in identifying potential areas that will be optimal for solar power stations in the Philippines')