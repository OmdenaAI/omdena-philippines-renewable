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
from marley.pandas import *
import rasterio
import plotly.express as px
import geopandas as gpd
from shapely.geometry import MultiPoint
from geopy.distance import EARTH_RADIUS, geodesic
from sklearn.cluster import DBSCAN
os.chdir(c.localpath)
popfile = "grid3/GRID3_NGA_PopEst_v1_1_mean_float.tif"
lightsfile = "grid3/lights.tif"
f = rasterio.open(popfile)

# %% [markdown]
# # get data

# %%
# get data
df = getdf(population=popfile, lights=lightsfile)
df.population = df.population.fillna(0).astype(int)
df["row"], df["col"] = get_rowcol(df, f.shape)

# %%
# REMINDER OF ORIENTATION row, col => height, width => y,x => lat,lon  => NS, WE
# row, col => google maps/earth, numpy, pandas, tif.shape, geopy, image
# x,y = openstreetmap, rasterio transform input and output.
(0,0)*f.transform, (f.width,0)*f.transform, (0,f.height)*f.transform

# %%
# pixelwidth at top and bottom of map
top = geodesic((0,0)*f.transform, (0,1)*f.transform).km
bottom = geodesic((f.height,0)*f.transform, (f.height,1)*f.transform).km
d(f"top={top*1000:.1f}m bottom={bottom*1000:.1f}m diff={(top-bottom)/top*100:.1f}%")

# %%
# %%s
# 3m to be clustered
pd.crosstab(df.lights==0, df.population>0)

# %% [markdown]
# # model

# %%
# rowcol model faster than latlon. 16, 10, 5 pixels is roughly 1.5km.1km, 500m
# unlit is DSMB<.1 and viirs<.6
eps = 5
unlit = df[(df.population>0) & (df.lights==0)]
weights = unlit.population.values
x = unlit[["row", "col"]].values
m = DBSCAN(eps=eps, min_samples=4000, algorithm='ball_tree', n_jobs=-1)
unlit["label"] = m.fit_predict(x, sample_weight=weights)

# %% [markdown]
# # add features

# %%
get_latlon(unlit, f.transform, inplace=True)

# %%
# aggregate to clusters => population, area, density
# dfp = points, dfc=clusters
dfp = unlit[unlit.label>=0]
dfc = dfp.groupby("label").agg(dict(population=np.sum, 
                                    row=np.mean, col=np.mean,
                                    lat=np.mean, lon=np.mean))
def get_area(x):
    hull = MultiPoint(list(zip(x.row, x.col))).convex_hull
    area = hull.area*top**2
    return area
dfc["area"] = dfp.groupby("label").apply(get_area).values
dfc["density"] = dfc.population/dfc.area

dfc[["area", "population", "density"]] = dfc[["area", "population", "density"]].astype(int)
f"clusters={len(dfc):,}, mean={dfc.population.mean():,.0f} median={dfc.population.median():,.0f}"\
            f" clustered={dfp.population.sum():,}"\
            f" unclustered={unlit[unlit.label==-1].population.sum():,}"\
            f" median_density={dfc.density.median():,.0f}"

# %% [markdown] {"heading_collapsed": true}
# # check

# %% {"hidden": true}
# first clusters look perfect
dfc.head()

# %% {"hidden": true}
# largest clusters
dfc.sort_values("population", ascending=False).head()

# %% {"hidden": true}
# single cluster
n = 1
d(dfc[dfc.index==n])
cluster = dfp[dfp.label==n]
pd.crosstab(cluster.row, cluster.col, cluster.population, aggfunc=sum).fillna(-1).astype(int).replace(-1, "")

# %% {"hidden": true}
for x in np.arange(1,4, .5):
    area = np.pi*x**2
    print(x, area, 4000/area)

# %% {"hidden": true}
px.histogram(dfc[dfc.population.between(1, 100000)], "population")

# %% {"hidden": true}
px.box(dfc, y="density")

# %% {"hidden": true}
subpop = dfc[dfc.population.between(0,8000)]
px.scatter(subpop, x="population", y="density")

# %% [markdown]
# # output - address, geoshapes

# %%
# set the job folder
os.chdir(f"{c.localpath}/clusters_500m")

# %%
# #%%s
# save
dfp.to_pickle("points.pkl", index=False)
dfc.to_excel("clusters.xlsx", index=False)

# %%
# load
dfp = pd.read_pickle("points.pkl")
dfc = pd.read_excel("clusters.xlsx", index=False)

# %%
# address - 15 MINUTES
get_address(dfc, inplace=True)

# %%
dfc.to_excel("clusters.xlsx", index=False)


# %%
# shapes
def get_shape(x):
    hull = MultiPoint(list(zip(x.lon, x.lat))).convex_hull
    return hull
dfc.address0 = dfc.address0.fillna("")
dfc["label_out"] = dfc.apply(lambda x: f"{str(x.name)}-{x.address0}={x.population:,.0f}", axis=1)
dfc["geometry"] = dfp.groupby("label").apply(get_shape).values
gdf = gpd.GeoDataFrame(dfc[["label_out", "geometry"]])
try:
    os.remove("popshapes.geojson")
except FileNotFoundError:
    pass
gdf.to_file("popshapes.geojson", driver="GeoJSON", encoding="utf8")

# %%
# cleanup
dfc["centroid"] = dfc.apply(lambda x: Point(x.lon, x.lat), axis=1)
dfc = dfc.drop(columns=["lat", "lon", "row", "col"])

# %%
dfc.to_excel("clusters.xlsx", index=False)

# %%
# create pop_web for display on web. WARNING clip to 255 is OK for map if largest band is <255
src = r"grid3\GRID3_NGA_PopEst_v1_1_mean_float.tif"
dst = r"grid3\pop_web.tif"
profile = rasterio.open(src).profile
profile["dtype"] = "uint8"
del profile["nodata"]
data = rasterio.open(src).read(1)
data = np.clip(data, 0, 255).astype(np.uint8)
with rasterio.open(dst, "w", **profile) as f:
    f.write(data, 1)

# %% [markdown]
# # test for bug geopandas

# %%
gpd.show_versions()

# %%
df = gpd.read_file("popshapes.geojson")
df.to_file("popshapes2.geojson", driver="GeoJSON") 
df2 = gpd.read_file("popshapes2.geojson") 
