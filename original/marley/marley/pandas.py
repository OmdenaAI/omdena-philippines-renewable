""" functions to manipulate dataframes """

from tqdm import tqdm_notebook as tqdm
import pandas as pd
import numpy as np
from geopy.distance import geodesic
from geopy import Nominatim, Photon
import logging
log = logging.getLogger()

def wcut(df, target, weight=None, bins=4, label_func=min, sort=True, inplace=False, **kwargs):
    """ weighted pd.cut for target bins that have equal sum of weight
    e.g. rainfall, population => lowest bin is labelled 0 and is the 25% of the population who have least rainfall

    :param target: series to divide into bins e.g. rainfall.
    :param weight: series to form percentiles e.g. population.
    :param bins: int, sequence of scalars, or IntervalIndex. see pandas.cut for details.
    :param label_func: function to apply to labels. default=min; None=pd.interval
    :param sort: avoid sort if already sorted by target
    :param inplace: if True then sorts by target and adds column "{target}_bin column". Faster as df only sorted once.
                    and no need to align
    :param kwargs: passed to pd.cut
    :return: if not inplace then labels.values
    """
    if weight is None:
        weight = target
    if not inplace:
        df = pd.concat([df[target], df[weight]], axis=1)
        df = df.reset_index()
    if sort:
        df.sort_values(target, inplace=True)

    # float64 to avoid rounding errors
    cum_weight = df[weight].astype(np.float64).cumsum()
    df["labels_"] = pd.cut(cum_weight, bins=bins, **kwargs)

    # recode labels
    if label_func is not None:
        df.labels_ = df[target].groupby("labels_", sort=False).transform(label_func).values

    if not inplace:
        if sort:
            # sort again to align return values with original df
            df = df.sort_index().set_index("index", drop=True)
        return df.labels_.values

    df.rename(columns=dict(labels_=[f"{target}_bin"]), inplace=True)

def distance(df, a,b):
    """ return distance between 2 dataframe rows representing locations
    :param df: dataframe with lat and lon columns
    :param a: row index of location
    :param b: row index of location
    :return: kms between two points
    """
    a = df.iloc[a]
    b = df.iloc[b]
    return geodesic((a.lat, a.lon), (b.lat, b.lon)).km

def get_rowcol(df, shape, inplace=False):
    """ get rows and cols to fit shape
    :param shape: shape of original tif or image
    :return: rows and cols if inplace=False
    """
    if not inplace:
        df = df.copy()
    rows, cols = shape
    df["row"] = np.concatenate(
            [[row]*cols for row in range(rows)],
            axis=0)
    df["col"] = rows * list(range(cols))
    if not inplace:
        return df.row.values, df.col.values

def get_latlon(df, transform, centred=True, inplace=False):
    """ get longtitude and latitude
    :param df: dataframe including columns for row, col
    :param transform: affine transform to apply. this is in tif.affine
    :param centred: if true then pixel coordinates are centred rather than topleft
    :param inplace: uses less RAM as avoids copying memory
    :return: lat.values, lon.values if inplace=False
    """
    if not inplace:
        df = df.copy()
    lonlat = df.apply(lambda x: (x.col, x.row)*transform, axis=1)
    df["lon"] = lonlat.apply(lambda x: x[0])
    df["lat"] = lonlat.apply(lambda x: x[1])

    if centred:
        # set lonlat to centre of pixel rather than top left
        topleft = (0, 0) * transform
        mid = (.5, .5) * transform
        offset = mid[0]-topleft[0], mid[1]-topleft[1]
        df.lon = df.lon + offset[0]
        df.lat = df.lat + offset[1]
    if not inplace:
        return df.lat.values, df.lon.values

def get_centroids(df, weight):
    """ return weighted cluster centroids for one row
    :param weight: weight such as population
    :return: lat.values, lon.values
    """
    def pop_centroid(row):
        """ return weighted cluster centroid for one row """
        lat = (row.lat*row[weight]).sum()/row[weight].sum()
        lon = (row.lon*row[weight]).sum()/row[weight].sum()
        return lat, lon
    pop_centroids = df[df.label>=0].groupby("label").apply(pop_centroid)
    lat = pop_centroids.apply(lambda x: x[0])
    lon = pop_centroids.apply(lambda x: x[1])
    return lat.values, lon.values

def get_address(df, inplace=False, n=999999):
    """ get the address
    :param df: dataframe
    :param inplace: reduces memory
    :param n: limit to get n addresses for testing as takes long time to run
    :return: if not inplace then values of address, address0, geolocator
    """
    if not inplace:
        df = df.copy()
    # Photon has villages but sometimes returns None. Also server down for last few days?
    # Nominatem returns area only; all others require api keys.
    geolocs = [Photon(), Nominatim(user_agent="renewable")]
    for i, row in tqdm(df.iterrows(), total=len(df)):
        for geoloc in geolocs:
            try:
                address = geoloc.reverse((row.lat, row.lon)).address
            except KeyboardInterrupt:
                break
            except:
                continue
            if address:
                df.loc[i, "address"] = address
                df.loc[i, "address0"] = address.split(",")[0]
                df.loc[i, "geolocator"] = geoloc.__class__.__name__
                break
        if i>n:
            log.warning(f"limited to first {n} addresses")
            break
    if not inplace:
        return df.address.values, df.address0.values, df.geolocator.values

def get_color(df, inplace=False):
    """ assign clusters to 4 colors so no two adjacent clusters have same color
    applies the 4 color theorem
    :param df: dataframe with row, col, label
    :return: Series color

    .. warning:: this takes a long time to run
    """
    if not inplace:
        df = df.copy()
    df["color"] = -9999

    # combined column is 3 times faster
    df["rowcol"] = (df.row*1e6+df.col).astype(int)

    # clusters use 4 colors to show borders
    colors = [1,2,3,4]
    for n, points in tqdm(df[df.label>=0].groupby("label")):
        # get adjacent pixels
        adjacent = []
        for i, p in points.iterrows():
            for offset in [(0,1), (1,0), (0,-1), (-1,0)]:
                adj = p.row+offset[0], p.col+offset[1]
                if all(np.array(adj)>=0):
                    adjacent.append(tuple(adj))

        # remove dupes and same cluster
        cluster = points[["row", "col"]].values.tolist()
        adjacent = set(adjacent) - set([tuple(x) for x in cluster])

        # combine rowcol for adjacent
        adjacent = np.array(list(adjacent))
        adjacent = (adjacent[:,0]*1e6 + adjacent[:,1]).astype(int)

        # set to first unused color
        used = pd.concat([df.loc[df.rowcol==rowcol, "color"] for rowcol in adjacent])
        unused = (set(colors)-set(tuple(used)))
        df.loc[df.label==n, "color"] = list(unused)[0]
    if not inplace:
        return df.color.values