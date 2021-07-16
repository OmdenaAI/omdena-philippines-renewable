import os
import numpy as np
import rasterio as rio
from time import time
from datetime import datetime, timedelta, timezone
from solar import dates_in_interval, calc_altitude_azimuth
from shadow import calc_shadow_mask
from srtm import download_srtm_files_for_nigeria

if not os.path.isdir('data'):
    download_srtm_files_for_nigeria()

# load the elevation geotiff of nigeria and get meta data
nigeria_elevation = rio.open('data/srtm/nigeria_elevation.tif')
meta = nigeria_elevation.meta
nigeria_elevation = nigeria_elevation.read(1)

# start start and end dates
start_date = datetime(
    year = 2020,
    month = 1,
    day = 1,
    hour = 0,
    minute = 0,
    tzinfo = timezone(timedelta(hours=0))
)
end_date = datetime(
    year = 2020,
    month = 1,
    day = 2,
    hour = 0,
    minute = 0,
    tzinfo = timezone(timedelta(hours=0))
)
interval = timedelta(hours=0.5)

# calculate aggregated shadow mask between dates with interval
#shadow_mask = np.zeros(nigeria_elevation.shape)
dates = dates_in_interval(start_date, end_date, interval)

for idx, date in enumerate(dates):
    # center of nigeria
    latitude = 9.885581
    longitude = 8.585050
    altitude, azimuth = calc_altitude_azimuth(latitude, longitude, date)

    # if the sun is not above the horizon, we skip
    if altitude <= 0:
        continue
    
    # calculate shadow mask for given solar position
    start = time()
    shadow_mask = calc_shadow_mask(altitude, azimuth, nigeria_elevation, nodata=meta['nodata'])
    print('Finished in:', time()-start)
    print('Dates left:', len(dates) - (idx+1))

    #np.save('data/srtm/nigeria_shadow_mask.npy', shadow_mask)
    new_dataset = rio.open(
        'data/srtm/nigeria_shadow_mask_{}.tif'.format(idx),
        'w',
        driver=meta['driver'],
        height=shadow_mask.shape[0],
        width=shadow_mask.shape[1],
        count=meta['count'],
        dtype=meta['dtype'],
        nodata=meta['nodata'],
        crs=meta['crs'],
        transform=meta['transform'],
    )
    new_dataset.write(shadow_mask, 1)
    new_dataset.close()
