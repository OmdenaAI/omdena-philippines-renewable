from shapely.geometry import shape
import geopandas as gp
import numpy as np
from shapely.geometry import box, Polygon

import helpers.generic as gn


def compute_area(gdf, field="area", crs=None):
    """Compute area in sqkm of geometries in geodataframe"""
    crs = crs if crs else "EPSG:32651"
    gdf[field] = gdf.to_crs(crs).geometry.area / 10 ** 6

    return gdf


def convert_geojson_to_geometry(gjson):
    """Convert geojson to geometry using shapely's shape"""
    geom = None
    try:
        geom = shape(gjson)
    except Exception as err:
        print("err: {}".format(err))
        raise Exception("Cant convert geojson to geometry")

    return geom


def create_geodataframe(data, crs=None):
    """Create a geodataframe"""
    crs = crs if crs else "EPSG:4326"

    return gp.GeoDataFrame(data, geometry=data["geometry"], crs=crs)


def create_shapely_box(geom):
    """Create a box using shapely"""
    minx, miny, maxx, maxy = geom.bounds

    return box(minx, miny, maxx, maxy)


def create_tiles(gdf, crs, width=1, length=1, file=None):
    """Create vector tiles from total bounds of a geodataframe"""
    xmin, ymin, xmax, ymax = geodataframe_bounds(gdf)
    cols = list(np.arange(xmin, xmax + width, width))
    rows = list(np.arange(ymin, ymax + length, length))

    polygons = []
    for x in cols[:-1]:
        for y in rows[:-1]:
            polygons.append(Polygon([(x, y), (x + width, y), (x + width, y + length), (x, y + length)]))

    grid = create_geodataframe({'geometry': polygons}, crs=crs)
    if file:
        grid.to_file(file)
    return grid


def drop_columns_dataframe(gdf, columns):
    """Drop columns in geodataframe or dataframe"""

    available_columns = get_columns_dataframe(gdf)
    remove_columns = [col for col in columns if col in available_columns]
    if not remove_columns:
        return gdf

    return gdf.drop(remove_columns, axis=1)


def get_columns_dataframe(gdf):
    """Get all columns in geodataframe or dataframe"""

    return gdf.columns


def geodataframe_bounds(gdf):
    """Return bounding box of geodataframe"""

    return gdf.total_bounds


def geojson_to_geodataframe(json_data, field="raster_val"):
    """Convert geojson data to geodataframe"""

    geometries = []
    values = []
    data = list(json_data)
    for d in data:
        geometries.append(convert_geojson_to_geometry(d["geometry"]))
        values.append(d["properties"][field])

    data = {
        "geometry": geometries,
        "values": values
    }
    gdf = create_geodataframe(data)
    # print(gdf.head())

    return gdf


def perform_overlay(gdf1, gdf2):
    """Perform geopandas' overlay to intersect two geodataframes"""
    return gp.overlay(
        gdf1,
        gdf2,
        keep_geom_type=False,
        make_valid=True,
        how="intersection"
    )


def reproject_geodataframe(gdf, crs=None):
    """Reproject geodataframe to another crs"""
    if not crs:
        return gdf

    return gdf.to_crs(crs=crs)


def shp_to_geodataframe(file, crs=None):
    """Open shapefile as geodataframe"""
    gn.validate_file(file)
    crs = crs if crs else "EPSG:4326"

    return gp.read_file(file, crs=crs)


def spatial_join(gdf1, gdf2):
    """Spatial join two geodataframes using shapely's intersect"""

    return gp.sjoin(gdf1, gdf2, how="left", op="intersects")
