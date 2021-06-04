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
from marley import *
from marley.tif import getdf
from marley.pandas import set_wcut
import rasterio
import plotly.express as px
os.chdir(c.localpath)


# %%
def basics(df, target, weight=None):
    """ basic analysis """
    d(f"sum={df[target].sum():,.0f} mean={df[target].mean()}")
    df = set_wcut(df, target, weight)
    d(df.groupby(f"{target}_bin")[weight].sum().astype(int))
    return df

def basics_lights(df, target, weight=None):
    df = basics(df, "population", "population")
    
    # proportion with lights
    lit0 = df[df.lights>0].population.sum()
    lit1 = df[df.lights>1].population.sum()
    print(f"lit0={lit0:,} lit1={lit1:,}\npop={df.population.sum():,.0f}%\n"
        f"lit0={lit0/df.population.sum()*100:.0f}%\n"
        f"lit1={lit1/df.population.sum()*100:.0f}%")

    # lights histogram
    df["lights_range"] = pd.cut(df.lights, bins=list(np.arange(0, 2, .05))+[df.lights.max()+1]).values
    weightedhist = df.groupby("lights_range").population.sum().reset_index()
    weightedhist.lights_range = weightedhist.lights_range.astype(str)
    c = px.bar(weightedhist, x="lights_range", y="population", title="number people in lights band")
    d(c)

    # lights by percentile
    df = set_wcut(df, "lights", "population", 100)
    df["percentile"] = (df.population.astype(np.float64).cumsum()/df.population.sum()*100).round(0).values
    c= px.line(df.groupby("percentile").min().reset_index(), x="percentile", y="lights_bin",
                        labels=dict(percentile="population percentile", lights_bin="minimum lights"),
                        title="Lights by percentile of population")
    d(c)
    return df


# %% [markdown]
# # population

# %%
wpop = "wpop/WorldPop_GP_100m_pop_median_population.tif"
df = getdf(wpop=wpop)

# %%
df = basics(df, "wpop", "wpop")

# %%
grid3 = "grid3/GRID3_NGA_PopEst_v1_1_mean_float.tif"
df = getdf(grid3=grid3)

# %%
df = basics(df, "grid3", "grid3")

# %%
rasterio.open(wpop).profile, rasterio.open(grid3).profile

# %%
"""
see above for quartiles to set as map legends
see qgis viirs_aligned to compare distributions of population (overall and abedde area)
    worldpop 100% pixels covered. grid3 settlement focus.
    difference shows worldpop more in non-settlement but also much more in towns and cities.
"""

# %% [markdown]
# # viirs

# %%
popfile = "viirs/GRID3_NGA_PopEst_v1_1_mean_float.tif"
lightsfile = "viirs/NOAA_VIIRS_DNB_MONTHLY_V1_VCMCFG_median_avg_rad.tif"
df = getdf(population=popfile, lights=lightsfile)

# %%
df = basics_lights(df, "lights", "population")

# %% [markdown]
# # dmsp

# %%
popfile = "dmsp/GRID3_NGA_PopEst_v1_1_mean_float.tif"
lightsfile = r"dmsp\NOAA_DMSP-OLS_NIGHTTIME_LIGHTS_median_stable_lights.tif"
df = getdf(population=popfile, lights=lightsfile)

# %%
df = basics_lights(df, "lights", "population")

# %% [markdown]
# # grid3

# %%
popfile = "grid3/GRID3_NGA_PopEst_v1_1_mean_float.tif"
lightsfile = r"grid3\NOAA_DMSP-OLS_NIGHTTIME_LIGHTS_median_stable_lights.tif"
df = getdf(population=popfile, lights=lightsfile)

# %%
# proportion with lights
lit0 = df[df.lights>.1].population.sum()
lit1 = df[df.lights>1].population.sum()
print(f"lit0={lit0:,} lit1={lit1:,}\npop={df.population.sum():,.0f}%\n"
    f"lit0={lit0/df.population.sum()*100:.0f}%\n"
    f"lit1={lit1/df.population.sum()*100:.0f}%")

# %%
lightsfile = r"grid3/NOAA_VIIRS_DNB_MONTHLY_V1_VCMCFG_median_avg_rad.tif"
df = getdf(population=popfile, lights=lightsfile)

# %%
# proportion with lights
lit0 = df[df.lights>.6].population.sum()
lit1 = df[df.lights>1].population.sum()
print(f"lit0={lit0:,} lit1={lit1:,}\npop={df.population.sum():,.0f}%\n"
    f"lit0={lit0/df.population.sum()*100:.0f}%\n"
    f"lit1={lit1/df.population.sum()*100:.0f}%")

# %%
## cannot run basics_lights as memory error
#df = basics_lights(df, "lights", "population")

# %% [markdown]
# # compare dsmp and viirs

# %%
popfile = "grid3/GRID3_NGA_PopEst_v1_1_mean_float.tif"
dmspfile = r"grid3\NOAA_DMSP-OLS_NIGHTTIME_LIGHTS_median_stable_lights.tif"
viirsfile = "grid3/NOAA_VIIRS_DNB_MONTHLY_V1_VCMCFG_median_avg_rad.tif"
df = getdf(population=popfile, dmsp=dmspfile, viirs=viirsfile)

# %%
import rasterio
popfile = "d:/data/grid3/GRID3_NGA_PopEst_v1_1_mean_float.tif"
profile = rasterio.open(popfile).profile
profile

# %%
# create variable to show difference
dmsp = df.dmsp>.1
viirs = df.viirs>.6
df.loc[viirs & dmsp, "lights"] = 3
df.loc[viirs & ~dmsp, "lights"] = 2
df.loc[dmsp & ~viirs, "lights"] = 1
df.lights = df.lights.fillna(0).astype(np.float32)
profile = rasterio.open(popfile).profile
del profile["meta"]
profile["dtype"] = "uint8"
with rasterio.open("grid3/lights.tif", "w", **profile) as f:
    f.write(df.lights.values.reshape(f.shape), 1)

# %%
df[df.lights>0].population.sum()/df.population.sum()

# %%
