import os
import rasterio
from rasterio.features import shapes
import rioxarray as rx
import numpy as np

import helpers.generic as gn


def create_raster_shapes(raster, properties, mask=None):
    """Create geojson shapes from raster"""
    data = None
    with rasterio.Env():
        # image = raster.read(1)
        data = ({
            'properties': {'raster_val': v},
            'geometry': s
        } for i, (s, v) in enumerate(shapes(raster, mask=mask, transform=properties)))
    raster = None

    return data


def open_raster_rio(file, masked=True):
    """Open raster file using rioxarray"""

    gn.validate_file(file)
    return rx.open_rasterio(file, masked=masked)


def open_raster(file):
    """Open raster using rasterio"""

    return rasterio.open(file)


def raster_statistics(raster):
    """Return raster's min, max and average pixel values"""
    min_val = None
    max_val = None
    mean_val = None
    try:
        min_val = raster.min().to_dict()["data"]
        max_val = raster.max().to_dict()["data"]
        mean_val = raster.mean().to_dict()["data"]
    except AttributeError as err:
        print("raster_properties: err: {}".format(err))

    return min_val, max_val, mean_val


def raster_bounds(raster):
    """Return raster's bounding box"""
    return raster.rio.bounds()


def raster_dimensions(raster):
    """Return raster's width and height"""
    return raster.rio.width, raster.rio.height


def raster_crs(raster):
    """Coordinate system of the raster file"""
    return raster.rio.crs


def raster_resolution(raster):
    """Pixel resolution of the raster file"""
    return raster.rio.resolution()


def rasterio_dataset_to_file(data, file, profile, dtype=rasterio.float32, nodata=0, band=1):
    """Create a raster file from rasterio's dataset"""
    with rasterio.Env():
        profile.update(
            dtype=dtype,
            count=band,
            compress='lzw',
            nodata=nodata
        )
        with rasterio.open(file, 'w', **profile) as dst:
            dst.write(data.astype(rasterio.float32), 1)

    return file


def get_dataset_profile(data):
    """Get rasterio's dataset profile"""

    return data.profile


def mask_raster(raster, band=1, op="lte", val=0):
    """Create a masked raster"""
    data = read_raster_band(raster, band=band)
    mask = get_mask_operator(data, val, op)

    return np.ma.masked_array(data, mask=mask)


def get_mask_operator(data, val, op):
    """Get mask operator"""
    operators = {
        "lte": data <= val,
        "lt": data < val,
        "ne": data != val,
        "eq": data == val,
        "gte": data >= val,
        "gt": data > val,
    }

    return operators[op]


def fill_raster_mask(raster, val=0):
    """Fill raster mask"""
    return np.ma.filled(raster.astype(float), val)


def add_two_rasters(raster1, raster2):
    """Add two rasters"""
    try:
        return raster1 + raster2
    except Exception as err:
        print("err: {}".format(err))

    return None


def multiply_two_rasters(raster1, raster2):
    """Multiply two rasters"""
    try:
        return raster1 * raster2
    except Exception as err:
        print("err: {}".format(err))

    return None


def clip_raster_to_geom(raster, geom, crs=None):
    """Clip raster within geometry bounds using rioxarray"""
    crs = crs if crs else "EPSG:4326"

    return raster.rio.clip(geometries=geom, crs=crs, drop=True, invert=False)


def rioxarray_to_file(data, file):
    """Export rioxarray data to file"""
    data.rio.to_raster(file, compress='lzw', tiled=True)

    return file


def read_raster_band(raster, band=1):
    """Read specific band of raster"""
    return raster.read(band)


def get_raster_transform_properties(raster):
    """Get raster properties to use for transformation"""
    return raster.transform


def reproject_match_raster(raster, match):
    """Reproject input raster using a match raster"""
    return raster.rio.reproject_match(match)


def save_to_file(raster, path, filename):
    """Save raster to file using rioxarray"""
    file = os.path.join(path, filename)
    rioxarray_to_file(raster, file)


def get_raster_properties_rio(raster):
    """Wrapper function to get all pertinent properties of raster"""

    return {
        "stats": raster_statistics(raster),
        "bounds": raster_bounds(raster),
        "dimensions": raster_dimensions(raster),
        "crs": raster_crs(raster),
        "pixel_res": raster_resolution(raster)
    }
