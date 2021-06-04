import os
import numpy as np
import rasterio as rio
from rasterio.enums import Resampling
from tqdm import tqdm
from time import time
from utils import upsample_from_to
from gsa import download_global_solar_atlas_for_nigeria

if not os.path.isdir('data'):
    download_global_solar_atlas_for_nigeria()

directory = 'data/Nigeria_GISdata_LTAy_AvgDailyTotals_GlobalSolarAtlas-v2_GEOTIFF/'

# load the effective irradiance geotiff of nigeria
nigeria_effective_irradiance = rio.open(directory + 'GHI.tif')
meta = nigeria_effective_irradiance.meta
nigeria_irradiance = nigeria_effective_irradiance.read(1)

# load the temperature geotiff of nigeria and upsample to irradiance resolution
nigeria_temp = rio.open(directory + 'TEMP.tif')
upsample_from_to(nigeria_temp, nigeria_effective_irradiance, 'data/nga_temp.tif')
nigeria_temp = rio.open('data/nga_temp.tif').read(1)

# set the temperature coefficient
TEMP_COEF = -0.004 # usually between -0.003 and -0.005 (-0.3 to -0.5%)

M, N = nigeria_irradiance.shape
for m in tqdm(range(M)):
    for n in range(N):
        cur_temp = nigeria_temp[m, n]
        cur_eff_irradiance = nigeria_irradiance[m, n]

        # skip when there is no data
        if np.isnan(cur_temp) or np.isnan(cur_eff_irradiance):
            continue

        # if we don't reach the reference cell temperature, we skip as well
        if cur_temp <= 25:
            continue

        # difference from the reference temperature
        temp_diff = cur_temp - 25

        # calculate how much irradiance is wasted from the temperature
        temp_loss = TEMP_COEF * cur_eff_irradiance * temp_diff
        if temp_loss > 0:
            print(temp_loss)
        # adjust effective irradiance
        nigeria_irradiance[m, n] += temp_loss

# save the new
new_dataset = rio.open(
    'data/nigeria_effective_irradiance.tif',
    'w',
    driver=meta['driver'],
    height=nigeria_irradiance.shape[0],
    width=nigeria_irradiance.shape[1],
    count=meta['count'],
    dtype=np.float32,
    nodata=-99999,
    crs=meta['crs'],
    transform=meta['transform'],
)
new_dataset.write(nigeria_irradiance, 1)
new_dataset.close()

