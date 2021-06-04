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
from marley.utils.ipstartup import *
from marley import tif, config as c
import rasterio
from rasterstats import zonal_stats
import geopandas as gpd
os.chdir(c.localpath)

# %% [markdown]
# # other cropped areas

# %%
lightsfile = r"grid3\NOAA_VIIRS_DNB_MONTHLY_V1_VCMCFG_median_avg_rad.tif"
d("**** with lights **********")
d(zonal_stats("vectors/examples/ajaokuta.gpkg", lightsfile))

d("**** without lights **********")
d(zonal_stats("vectors/examples/omuo.gpkg", lightsfile))
d(zonal_stats("vectors/examples/agbaja.gpkg", lightsfile))
d(zonal_stats("vectors/examples/agbede all.kml", lightsfile))

# %%
popfile = r"grid3/GRID3_NGA_PopEst_v1_1_mean_float.tif"
data = rasterio.open(popfile).read()[0]
data[data<0] = 0
data[np.isnan(data)] = 0
d(zonal_stats("vectors/examples/agbede all.kml", data, affine=rasterio.open(popfile).transform, stats=["sum"]))
zonal_stats("vectors/examples/richifa.kml", data, affine=rasterio.open(popfile).transform, stats=["sum"])

# %%
popfile = r"dmsp/GRID3_NGA_PopEst_v1_1_mean_float.tif"
data = rasterio.open(popfile).read()[0]
d(zonal_stats("vectors/examples/agbede all.kml", data, affine=rasterio.open(popfile).transform, stats=["sum"]))
zonal_stats("vectors/examples/richifa.kml", data, affine=rasterio.open(popfile).transform, stats=["sum"])

# %% [markdown]
# # village agbede - apply KML vector to raster

# %% [markdown]
# * cut the shape files in google maps pro for 4 areas around agbede; one super-area around the whole settlement; and one round remote village south west
# * rasterstats to get data for those areas from the population raster
# * manually estimated number of houses
# * calculated area km2 and density pop/km2
#
# check:
# * scale is 1 pixel = 100m
# * agbede north is about 200m*50m = .2 * .05=.01km2 => looks OK
#
# results:
# * at high resolution it is not accurate e.g. the forest has more people than the village
# * that is only 2 pixels for agbede north with 30 houses
# * as you zoom out then you get 163 people in 100 houses. still a bit low.
# * looks like it could be improved by increasing the weight given to settlements

# %%
# compare count of houses to worldpop
shapes = ["vectors/examples/agbede north.kml",\
          "vectors/examples/agbede north east.kml",\
          "vectors/examples/agbede south.kml",\
          "vectors/examples/agbede south east.kml",
          "vectors/examples/agbede all.kml",
          "vectors/examples/unnamed swest agbedde.kml"]


# %%
def getstats(shapes, tifname):
    # get as array to allow replacement of -3.4e-34
    data = rasterio.open(tifname).read()[0]
    data[data<0] = 0
    data[np.isnan(data)] = 0
    d(f"total population={data.sum()}")
    
    # create df of shapes
    allstats = []
    for shape in shapes:
        row = zonal_stats(shape, data, affine=rasterio.open(tifname).meta["transform"])
        # list of 1 polygon
        row[0].update(geometry = gpd.read_file(shape).geometry.values)
        allstats.extend(row)
    df = pd.DataFrame.from_records(allstats)
    
    # format df
    df["filename"] = shapes
    df["sum"] = df["mean"]*df["count"]
    df["houses"] = [30,0,0,70, 100, 70]
    df["area"] = df.geometry.apply(lambda x: x.area.sum())*10000
    df["density"] = df["sum"]/df.area
    return df.round(3).drop(columns=["geometry"])


# %%
getstats(shapes, "wpop/WorldPop_GP_100m_pop_median_population.tif")

# %%
getstats(shapes, r"grid3/GRID3_NGA_PopEst_v1_1_mean_float.tif")
