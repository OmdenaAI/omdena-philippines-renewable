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
from ipstartup import *
import geopandas as gpd
from marley import config as c
import rasterio
from rasterio import features
from shapely import wkt
from shapely.geometry import shape, Point
from geopy.distance import distance, geodesic
deg2km = geodesic((5,3), (6,3)).km
km2deg = 1/deg2km
deg2km, km2deg
repo = r"C:\Users\simon\OneDrive\Documents\py\live\renewable"
os.chdir(c.localpath)
os.chdir("clusters_500m")

# %%
with rasterio.open("../grid3/lights.tif") as src:
    lights = src.read(1)
mask = lights>0
shapes = features.shapes(lights, mask=mask)
shapes = [s[0] for s in shapes]

transform = rasterio.open("../grid3/lights.tif").transform
lonlat_shapes = []
for s in shapes:
    coords = [(x,y)*transform for x,y in s["coordinates"][0]]
    lonlat_shapes.append(Polygon(coords))

gdf = gpd.GeoDataFrame.from_dict(dict(geometry=lonlat_shapes))
gdf.to_file("../grid3/lights.geojson", driver="GeoJSON", encoding="utf8")

# %%
get_latlon(unlit, f.transform, inplace=True)

# %%
# read data
df = pd.read_excel("clusters.xlsx")
df.geometry = df.geometry.apply(wkt.loads)
df.centroid = df.centroid.apply(wkt.loads)
gdf = gpd.GeoDataFrame(df)

# %% [markdown]
# # add data

# %%
# ongrid
grid = gpd.read_file(r"../nigeria-electricity-transmission-network\Nigeria Electricity Transmission Network.shp")
ongrid = gpd.GeoSeries(grid.buffer(15*km2deg)).unary_union
df["ongrid"] = gdf.intersects(ongrid)
gpd.GeoSeries(ongrid).to_file("ongrid15.geojson", driver="GeoJSON", encoding="utf8")

# %%
# area
areafile = f"{repo}/task2_estimate_energy_demand/nga_adm_osgof_20190417_SHP/nga_admbnda_adm2_osgof_20190417.shp"
area = gpd.read_file(areafile)[['ADM1_EN','ADM2_EN','geometry']]
adm1s = []
adm2s = []
for point in df.centroid:
    for adm1,adm2,po in area.values:
        if po.contains(point)==True:
            adm1s.append(adm1)
            adm2s.append(adm2)
            break
    else:
        adm1s.append("")
        adm2s.append("")
df["adm1"] = adm1s
df["adm2"] = adm2s

# %% [markdown]
# # score

# %%
# set score
df["score"] = df.density
df.loc[df.ongrid, "score"] = 0
##### add other criteria

# %%
# output
df = df.sort_values("score", ascending=False)
df.to_excel("clusters.xlsx", index=False)
df.head(10)
