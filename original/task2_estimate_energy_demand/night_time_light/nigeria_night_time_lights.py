#https://developers.google.com/earth-engine/python_install
#You 1st need to sign up your Google account here: https://earthengine.google.com/ (it takes a couple of hours to get accepted. The API won't work before.)
import ee
import folium
from IPython.display import Image, display
import os

ee.Authenticate()
ee.Initialize()

# Define a method for displaying Earth Engine image tiles to folium map.
def add_ee_layer(self, eeImageObject, visParams, name):
  mapID = ee.Image(eeImageObject).getMapId(visParams)
  folium.raster_layers.TileLayer(
    tiles = "https://earthengine.googleapis.com/map/"+mapID['mapid']+
      "/{z}/{x}/{y}?token="+mapID['token'],
    attr = "Map Data © Google Earth Engine",
    name = name,
    overlay = True,
    control = True
  ).add_to(self)

# Add EE drawing method to folium.
folium.Map.add_ee_layer = add_ee_layer

# Create a folium map object.
myMap = folium.Map(location=[9.0820, 8.6753], zoom_start=6, height=1000)

# Adds a band containing image date as years since 1991.
def createTimeBand(img):
  year = ee.Date(img.get('system:time_start')).get('year').subtract(1991)
  return ee.Image(year).byte().addBands(img)


# Map the time band creation helper over the night-time lights collection.
# https://developers.google.com/earth-engine/datasets/catalog/NOAA_DMSP-OLS_NIGHTTIME_LIGHTS
collection = ee.ImageCollection('NOAA/DMSP-OLS/NIGHTTIME_LIGHTS').select('stable_lights').map(createTimeBand)

# Compute a linear fit over the series of values at each pixel, visualizing
# the y-intercept in green, and positive/negative slopes as red/blue.
myMap.add_ee_layer(collection.reduce(ee.Reducer.linearFit()),{'bands':['scale', 'offset', 'scale'], 'min': 0, 'max': [0.18, 20, -0.18]},'stable lights trend')

# Add a layer control panel to the map.
myMap.add_child(folium.LayerControl())

# Display the map.
PATH_MAP_FILE = '/home/jeney/Desktop/appdev/renewable/map.html'
myMap.save(PATH_MAP_FILE)