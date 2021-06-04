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
from marley import config as c
from marley.renewable import *
import rasterio
from glob import glob
import re
import plotly.express as px
os,chdir(c.localpath)

# %% [markdown]
# # Aggregate the monthly

# %%
dfs = []
for f in glob("viirs/monthly/*avg_rad.tif"):
    month = re.findall("\d{8}", f)
    if month and not month[0].startswith("2012"):
        month = month[0]
        light = rasterio.open(f).read().reshape(-1)
        dfs.append(pd.DataFrame(light, columns=[month]))
df = pd.concat(dfs, axis=1).sort_index(axis=1)

# %%
s = pd.DataFrame(df.sum()).reset_index()
s.columns = ["Date", "Radiance"]
fig = px.line(s, x=s.Date.values.tolist(), y="Radiance", title="monthly lighting")
fig.layout.update(dict(xaxis=dict(type="category", dtick=6)))
fig.show()
