# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import ee
from IPython.display import Image
import folium
ee.Initialize()
# Define a method for displaying Earth Engine image tiles to folium map.
def add_ee_layer(self, eeImageObject, visParams, name):
  mapID = ee.Image(eeImageObject).getMapId(visParams)
  folium.raster_layers.TileLayer(
    tiles = "https://earthengine.googleapis.com/map/"+mapID['mapid']+
      "/{z}/{x}/{y}?token="+mapID['token'],
    attr = "Map Data &copy; <a href='https://earthengine.google.com/'>Google Earth Engine</a>",
    name = name,
    overlay = True,
    control = True
  ).add_to(self)
folium.Map.add_ee_layer = add_ee_layer

# %% [markdown]
# # population

# %%
collection = ee.ImageCollection("WorldPop/GP/100m/pop")

# %%
collection.size().getInfo()

# %%
sample = collection.filterMetadata("country", "equals", "NGA")\
                   .filterMetadata("year", "equals", 2019)
sample.size().getInfo()

# %%
m = folium.Map(location=[6.4, 3.4], zoom_start=9)
m.add_ee_layer(sample.first(), {}, 'pop')
m.add_child(folium.LayerControl())
display(m)

# %%
