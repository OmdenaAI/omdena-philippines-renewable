""" add methods to ee.Image """
import folium
import ee
from . import config as c
from . import creds
import fs
import logging
log = logging.getLogger()

def download(image):
    """ download image to googledrive

    clipped to border with np.nan
    parallel gee to gdrive with progress monitor for tasks at https://code.earthengine.google.com/
    parallel from gdrive to local with progress monitor at chrome://downloads/
    for 452M takes 11 minutes (7+4)
    """
    # collection is already clipped but not single image
    image = image.clip(c.border)

    # todo would use open_fs but bug in googledrive only allows opening root folder
    googlepath = fs.open_fs(f"googledrive://{creds.gdrive()}").makedirs(c.googlepath, recreate=True)
    # todo if path does not exist
    localpath = fs.open_fs(c.localpath)

    # properties overrides meta as latter is incorrect for imagecollection aggregates such as median
    meta = image.getInfo()
    props = meta["properties"]

    # image meta
    image_name = props.get("id") or meta["id"]
    image_name = image_name.replace("/", "_")

    # each band separately as fails if different types e.g. int coverage, float radiance
    allfiles = []
    for i, band in enumerate(meta["bands"]):
        band_image = image.select(i)
        band_name = band["id"]
        taskname = f"{image_name}_{band_name}"
        filename_prefix = taskname
        filename = f"{filename_prefix}.tif"
        crs = band["crs"]
        crs_transform = props.get("crs_transform") or band["crs_transform"]

        # to overwrite then need to delete the original
        if localpath.exists(filename):
            #log.warning(f"File already exists locally: {filename}")
            continue
        if googlepath.exists(filename):
            #log.warning(f"File already exists on google drive: {filename}")
            continue

        # description is task name. cannot contain "."
        # fileNamePrefix is filename without extension. default as description
        # crs and crs_transform better than scale/dimensions/region as includes crs_transform in metadata
        # maxpixels needed else large files raise exception
        # notes:
        #   (if you use region it cannot be multipolygon so border.bounds["coordinates"] not border["coordinates"])
        #   (if you use scale or dimensions then crs_transform is not included in metadata)
        task = ee.batch.Export.image.toDrive(description=taskname,
                                             fileNamePrefix=filename_prefix,
                                             folder=c.googlepath,
                                             image=band_image,
                                             crs = crs,
                                             crs_transform = str(crs_transform),
                                             maxPixels=int(1e10))
        task.start()
        allfiles.append(filename)
    return allfiles
ee.Image.download = download

def add_layer(image, map, visParams, name):
    """
    add Earth Engine image to folium map
    """
    mapID = image.getMapId(visParams)
    folium.raster_layers.TileLayer(
    tiles = "https://earthengine.googleapis.com/map/"+mapID['mapid']+
      "/{z}/{x}/{y}?token="+mapID['token'],
    attr = "Map Data &copy; <a href='https://earthengine.google.com/'>Google Earth Engine</a>",
    name = name,
    overlay = True,
    control = True
    ).add_to(map)
ee.Image.add_layer = add_layer

def add_ee_layer(map, image, visParams, name):
    """ adds ee layer to map. Included for compatibility with ee examples """
    image.add_layer(map, visParams, name)
folium.Map.add_ee_layer = add_ee_layer