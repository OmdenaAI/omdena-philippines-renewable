import os
import numpy as np
import rasterio as rio
from shapely.geometry import Polygon, LineString
from shapely.ops import cascaded_union
from rasterio import features, mask
from tqdm import tqdm
from time import time
from utils import upsample_from_to

# load the shadow mask of nigeria
nigeria_shadow_mask = rio.open('shadow_mask/data/nigeria_shadow_mask.tif')
nga_shadow_meta = nigeria_shadow_mask.meta

# load the effective irradiance geotiff of nigeria
directory = 'temp_impact/data/Nigeria_GISdata_LTAy_AvgDailyTotals_GlobalSolarAtlas-v2_GEOTIFF/'
nigeria_irradiance = rio.open(directory + 'GHI.tif')

# crop shadow mask to effective irradiance
shapes = features.shapes(nigeria_irradiance.dataset_mask().astype(np.int16), transform=nigeria_irradiance.transform)
out_image, out_transform = mask.mask(nigeria_shadow_mask, [Polygon(geom['coordinates'][0]) for geom, val in shapes], crop=True)
del nigeria_shadow_mask

new_dataset = rio.open(
    'data/cropped_shadow_mask.tif',
    'w',
    driver=nga_shadow_meta['driver'],
    height=out_image.shape[1],
    width=out_image.shape[2],
    count=nga_shadow_meta['count'],
    dtype=nga_shadow_meta['dtype'],
    nodata=nga_shadow_meta['nodata'],
    crs=nga_shadow_meta['crs'],
    transform=out_transform,
)
new_dataset.write(out_image.squeeze(), 1)
new_dataset.close()

# load cropped shadow mask
nigeria_shadow_mask = rio.open('data/cropped_shadow_mask.tif')

# upsample effective irradiance to shadow mask resolution
upsample_from_to(nigeria_irradiance, nigeria_shadow_mask, 'data/nga_irr_upsampled.tif')
nigeria_irradiance = rio.open('data/nga_irr_upsampled.tif')
nga_irr_meta = nigeria_irradiance.meta
nigeria_irradiance = nigeria_irradiance.read(1)

# upsample temperature to shadow mask resolution
nigeria_temp = rio.open(directory + 'TEMP.tif')
upsample_from_to(nigeria_temp, nigeria_shadow_mask, 'data/nga_temp_upsampled.tif')
nigeria_temp = rio.open('data/nga_temp_upsampled.tif').read(1)
nigeria_shadow_mask = nigeria_shadow_mask.read(1)

print(nigeria_irradiance.shape)
print(nigeria_temp.shape)
print(nigeria_shadow_mask.shape)

# set the temperature coefficient
TEMP_COEF = -0.004 # usually between -0.003 and -0.005 (-0.3 to -0.5%)

M, N = nigeria_shadow_mask.shape
for m in tqdm(range(M)):
    for n in range(N):
        cur_eff_irradiance = nigeria_irradiance[m, n]
        cur_shadow_perc = nigeria_shadow_mask[m, n]
        cur_temp = nigeria_temp[m, n]

        # skip when there is no data
        if np.isnan(cur_temp) or np.isnan(cur_eff_irradiance) or np.isnan(cur_shadow_perc):
            continue
        
        # the effect of irradiance is lowered by the amount of shadows
        cur_eff_irradiance *= (1-cur_shadow_perc)

        # if we don't reach the reference cell temperature, we don't factor temperature in
        if cur_temp > 25:
            # difference from the reference temperature
            temp_diff = cur_temp - 25

            # calculate how much irradiance is wasted from the temperature
            temp_loss = TEMP_COEF * cur_eff_irradiance * temp_diff

            # adjust effective irradiance
            cur_eff_irradiance += temp_loss
        
        nigeria_irradiance[m, n] = cur_eff_irradiance

# save the new irradiance tif
new_dataset = rio.open(
    'data/nigeria_effective_irradiance.tif',
    'w',
    driver=nga_irr_meta['driver'],
    height=nigeria_irradiance.shape[0],
    width=nigeria_irradiance.shape[1],
    count=nga_irr_meta['count'],
    dtype=nga_irr_meta['dtype'],
    nodata=-99999,
    crs=nga_irr_meta['crs'],
    transform=nga_irr_meta['transform'],
)
new_dataset.write(nigeria_irradiance, 1)
new_dataset.close()

