import os
import numpy as np
import rasterio as rio

def convert_npy_to_tif():
    print('Loading worldpop tif..')
    worldpop_tif = 'nga_ppp_2020.tif'
    worldpop = rio.open(f'../data/{worldpop_tif}')
    meta = worldpop.meta
    del worldpop
    print('Done!')

    print('Loading nigeria electrical grid distances..')
    grid_npy = 'nigeria_electrical_grid_distances.npy'
    grid = np.load(f'data/{grid_npy}')
    print('Done!')

    print('Writing to tif..')
    grid_tif = rio.open(
        'data/nigeria_electrical_grid_distances.tif',
        'w',
        driver=meta['driver'],
        height=grid.shape[0],
        width=grid.shape[1],
        count=meta['count'],
        dtype=meta['dtype'],
        nodata=meta['nodata'],
        crs=meta['crs'],
        transform=meta['transform'],
    )
    grid_tif.write(grid, 1)
    grid_tif.close()
    print('Done!')