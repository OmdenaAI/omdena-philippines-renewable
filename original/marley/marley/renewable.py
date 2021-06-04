""" functions unique to renewable project """
import ee
import json
from marley import config as c

def lights():
    coll = ee.ImageCollection("NOAA/VIIRS/DNB/MONTHLY_V1/VCMCFG")\
                                    .sort('system:time_end', False)\
                                    .limit(12)
    return coll.download()

def sl_lights():
    coll = ee.ImageCollection("NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG")\
                                    .sort('system:time_end', False)\
                                    .limit(12)
    return coll.download()

def dmsp_lights():
    coll = ee.ImageCollection('NOAA/DMSP-OLS/NIGHTTIME_LIGHTS')\
                                .sort('system:time_end', False) \
                                .limit(12)
    return coll.download()

def onemonth():
    image = ee.Image("NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG/20171001")
    return image.download()

def population():
    coll = ee.ImageCollection("WorldPop/GP/100m/pop")\
                        .filterMetadata("country", "equals", "NGA")\
                        .filterMetadata("year", "equals", 2019)
    return coll.download()

def gpw_population():
    coll = ee.ImageCollection("CIESIN/GPWv411/GPW_Population_Count")
    return coll.download()

###########################################################################

def monthly_lights():
    lights = ee.ImageCollection("NOAA/VIIRS/DNB/MONTHLY_V1/VCMCFG") \
                        .sort('system:time_end', False) \
                        .limit(36)
    files = []
    for month in range(36):
        image = lights.get_image(month)
        file = image.download()
        files.append(file)
    return files

def border():
    """ download exact border direct to local """
    coordinates = c.border.coordinates().getInfo()
    with open(f"{c.localpath}/nigeria.json", "w") as f:
        json.dump(coordinates, f)

