import os
import numpy as np
import rasterio as rio
from rasterio.enums import Resampling
from tqdm import tqdm
from time import time

def upsample_from_to(raster_in, raster_out, new_raster):
    """
    Upsamples and adjusts the resolution and transformation of raster_in
    to raster_out.

    Accustomed from: https://gis.stackexchange.com/questions/329434/creating-an-in-memory-rasterio-dataset-from-numpy-array/329439#329439
    """
    # calculate resize scale
    in_shape = raster_in.read(1).shape
    out_shape = raster_out.read(1).shape
    scale = out_shape[0] / in_shape[0]

    t = raster_in.transform

    # rescale the metadata
    transform = rio.Affine(t.a / scale, t.b, t.c, t.d, t.e / scale, t.f)
    height = round(raster_in.height * scale)
    width = round(raster_in.width * scale)

    profile = raster_in.profile
    profile.update(transform=transform, driver='GTiff', height=height, width=width)

    # note changed order of indexes, arrays are band, row, col order not row, col, band
    data = raster_in.read(
        out_shape=(raster_in.count, height, width),
        resampling=Resampling.bilinear,
    )
    new_dataset = rio.open(
        new_raster,
        'w',
        driver=raster_in.meta['driver'],
        height=height,
        width=width,
        count=raster_in.meta['count'],
        dtype=raster_in.meta['dtype'],
        nodata=raster_in.meta['nodata'],
        crs=raster_in.meta['crs'],
        transform=transform,
    )
    new_dataset.write(data)
    new_dataset.close()

