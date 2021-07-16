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
import plotly.express as px
os.chdir(c.localpath)

# %% [markdown] {"heading_collapsed": true}
# # align rasters

# %% {"hidden": true}
# grid3
dstfolder = "grid3"
tgt = "grid3/GRID3_NGA_PopEst_v1_1_mean_float.tif"
tif.align("dmsp/NOAA_DMSP-OLS_NIGHTTIME_LIGHTS_median_stable_lights.tif", tgt, dstfolder)
tif.align("viirs/NOAA_VIIRS_DNB_MONTHLY_V1_VCMCFG_median_avg_rad.tif", tgt, dstfolder)

# %% {"hidden": true}
# wpop
dstfolder = "wpop"
tgt = "wpop/WorldPop_GP_100m_pop_median_population.tif"
tif.align("GRID3_NGA_PopEst_v1_1_mean_float.tif", tgt, dstfolder, True)

# %% {"hidden": true}
# VIIRS
dstfolder = "viirs"
tgt = "viirs/NOAA_VIIRS_DNB_MONTHLY_V1_VCMCFG_median_avg_rad.tif"
tif.align("grid3/GRID3_NGA_PopEst_v1_1_mean_float.tif", tgt, dstfolder, True)
tif.align("wpop/WorldPop_GP_100m_pop_median_population.tif", tgt, dstfolder, True)
tif.align("dmsp/NOAA_DMSP-OLS_NIGHTTIME_LIGHTS_median_stable_lights.tif", tgt, dstfolder)

# %% {"hidden": true}
# DMSP
dstfolder = "dmsp"
tgt = "dmsp/NOAA_DMSP-OLS_NIGHTTIME_LIGHTS_median_stable_lights.tif"

tif.align("grid3/GRID3_NGA_PopEst_v1_1_mean_float.tif", tgt, dstfolder, True)
tif.align("wpop/WorldPop_GP_100m_pop_median_population.tif", tgt, dstfolder, True)
tif.align("viirs/NOAA_VIIRS_DNB_MONTHLY_V1_VCMCFG_median_avg_rad.tif", tgt, dstfolder)

# %% [markdown]
# # align vector and raster

# %%
# read vector
areas = gpd.read_file("vectors/gadm36_NGA.gpkg")
areas.head(2)

# %%
# read raster
popfile = "wpop/WorldPop_GP_100m_pop_median_population.tif"
population = rasterio.open(popfile).read()
population[population>0].sum(), population.shape

# %%
# get raster data using vector areas
stats = zonal_stats("vectors/gadm36_NGA.gpkg", popfile)
len(stats), stats[0]

# %%
# reformat areas and combine with stats
df = areas.rename(columns=dict(GID_2="code", NAME_2="area"))[["area", "code"]]
df = pd.concat([df, pd.DataFrame.from_records(stats)], axis=1)
df["population"] = df["mean"]*df["count"]
df.population= df.population.astype(int)
d(len(df))
df.head()

# %% [markdown]
# # compare raster and census population

# %%
# format census
census = pd.read_excel(r"tables/nga_admpop_2016.xlsx", sheet_name="NGA Admin2 2016 Pop")
census = census.rename(columns={"admin2RefName": "area", "Population2016":"population", "admin2Pcode":"code"})
census["code2"] = census.code.apply(lambda x: f"NGA.{int(x[2:5])}.{int(x[5:8])}_1")
census = census[["code", "code2", "area", "population"]]
d(len(census))
census.head()

# %%
# THE AREAS DONT MATCH!!!!!!
both = df.merge(census, left_on="code", right_on="code2", how="outer",
                indicator=True, suffixes=["_pop", "_cen"])\
                .sort_values("area_pop")
both.to_excel("temp.xlsx")
both[both._merge!="both"]

# %%
# check %diff after adjusting to same scale as different years
both["cen2"] = both.population_cen*both.population_pop.sum()/both.population_cen.sum()
both.cen2 = both.cen2.fillna(0).astype(int)
both["diffpc"] = (both.cen2/both.population_pop-1)*100
both.drop(columns=["count", "max", "mean", "min"])
