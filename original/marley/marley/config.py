"""
global variables for the project or task
these can be reset at any time
"""
import ee
import os

# exact border for clipping. this keeps the size down and cuts out unnecessary data.
border = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017')\
                    .filterMetadata("country_na", "equals", "Nigeria").geometry()

# data path on local drive for large files
localpath = "d:/data"

# data path on google drive
googlepath = "eedata"

# these are required for GDAL and not automatically set at install
os.environ.setdefault("PROJ_LIB", r"C:\Users\simon\Anaconda3\Library\share\proj")
os.environ.setdefault("GDAL_DATA", r"C:\Users\simon\Anaconda3\Library\share\gdal")