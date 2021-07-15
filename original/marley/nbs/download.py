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
from marley.renewable import *
from marley import gdrive2local

# %% [markdown]
# # download to google drive

# %%
# all from omdena.py
onemonth()
sl_lights()
dmsp_lights()
lights()
population()
gpw_population()
monthly_lights()

# %% [markdown]
# # Download to local

# %%
files = ['NOAA_DMSP-OLS_NIGHTTIME_LIGHTS_median_avg_vis.tif',
 'NOAA_DMSP-OLS_NIGHTTIME_LIGHTS_median_stable_lights.tif',
 'NOAA_DMSP-OLS_NIGHTTIME_LIGHTS_median_cf_cvg.tif',
 'NOAA_DMSP-OLS_NIGHTTIME_LIGHTS_median_avg_lights_x_pct.tif']

# %%
# wait until tasks completed (could be an hour) OR or run several times OR pass list of files to wait for
# if you get any zero sized files then delete them and rerun.
gdrive2local(files)

# %%
