""" add methods to ee.ImageCollection """

import ee
from datetime import datetime
from . import config as c

def formatdate(timestamp):
    """ return d/m/y from timestamp """
    return datetime.fromtimestamp(timestamp/1000).strftime("%d/%m/%y")

def get_dates(coll):
    """ return end dates for each image in collection """
    image_metas = coll.getInfo()["features"]
    dates = [im["properties"]["system:time_end"] for im in image_metas]
    return [formatdate(d) for d in dates]
ee.ImageCollection.get_dates = get_dates

def download(coll, aggfunc="median"):
    """ download single image from aggregating collection
    this is required to fill metadata from collection as not present in aggregated

    :param band: band/variable to download. one at a time as must be same type.
    :param aggfunc: function to convert collection to image
    :return: None. downloads result to "{googlepath}/{imagename}_{aggfunc}_{bandname}.tif"
    """
    # collection metadata
    imagename = coll.getInfo()["id"]
    id = f"{imagename}_{aggfunc}"

    # first image metadata
    meta = coll.first().clip(c.border).getInfo()["bands"][0]
    crs_transform = str(meta["crs_transform"])
    dimensions = meta["dimensions"]

    # check as expected
    print(coll.get_dates())
    print(f"id={id} transform={crs_transform} dimensions={dimensions}")

    # area outside clip set to np.nan for toDrive; zero for getDownloadUrl
    image = getattr(coll, aggfunc)().clip(c.border)
    image = image.set(dict(id=id, crs_transform=crs_transform))
    return image.download()
ee.ImageCollection.download = download

def get_image(coll, n):
    """ return the nth image """
    return ee.Image(coll.toList(coll.size()).get(n))
ee.ImageCollection.get_image = get_image