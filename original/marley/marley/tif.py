""" functions to manipulate tif files """

import os
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import numpy as np
import pandas as pd
import logging
log = logging.getLogger()

def getdf(**filedict):
    """ return dataframe from dict of colname=filename """
    data = {k:rasterio.open(v).read()[0].reshape(-1) for k,v in filedict.items()}
    df = pd.DataFrame.from_dict(data)
    df = df.fillna(0)
    for col in df.columns:
        df.loc[df[col]<0, col] = 0
    return df

def align(src, tgt, dstfolder, rescale=False):
    """ align src tif to dst dimensions including reproject, mask nans, rescale values
    :param src: source path
    :param tgt: target path to align with. this will not be overwritten.
    :param dstfolder: folder to save aligned output
    :param rescale: if true then scales the total e.g. population.
    :return: None. creates output file f"{src_basename}_aligned.{src_ext}"
    """
    # todo more than 1 band. what happens if unmatched band counts?
    count = 1
    with rasterio.open(src) as src, rasterio.open(tgt) as tgt:
        # set output format
        if (src.meta["width"]*src.meta["height"]) > (tgt.meta["width"]*tgt.meta["height"]):
            # downsize
            resampling = Resampling.bilinear
        else:
            # upsize
            resampling = Resampling.bilinear

        # reproject
        output = np.zeros((count, tgt.height, tgt.width), dtype=tgt.meta["dtype"])
        for i in range(count):
            reproject(
                source=rasterio.band(src, i+1),
                destination=output[i],
                resampling=resampling,

                # need crs and transform to output array rather than tif
                dst_crs=tgt.meta["crs"],
                dst_transform=tgt.meta["transform"],
               )

        # standardise nodata values
        output[output<-3.4e-38] = np.nan
        srcdata = src.read()
        if src.meta["dtype"].startswith("float"):
            srcdata[srcdata==src.meta["nodata"]] = np.nan
            srcdata[srcdata<-3.4e-38] = np.nan

        # mask nans from target. crops to same area.
        tgtdata = tgt.read()
        for i in range(count):
            output[i][np.isnan(tgtdata[i])] = np.nan

        # rescale totals e.g. make population same total for whole grid
        if rescale:
            for i in range(count):
                scale = srcdata[i][~np.isnan(srcdata[i])].sum() / output[i][~np.isnan(output[i])].sum()
                output[i] = output[i] * scale

        # create output file
        meta = tgt.meta.copy()
        name, ext = os.path.splitext(os.path.basename(src.files[0]))
        outfile = f"{dstfolder}/{name}{ext}"
        os.makedirs(dstfolder, exist_ok=True)
        with rasterio.open(outfile, "w", **meta) as f:
            f.write(output)
        log.info(f"created {outfile}")

