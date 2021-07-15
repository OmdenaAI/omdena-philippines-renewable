import os
import numpy as np
import rasterio as rio
from tqdm import tqdm

def get_dists():
    print('Loading tifs..')

    # read in worldpop and find land coordinates
    worldpop_tif = 'nga_ppp_2020.tif'
    worldpop = rio.open(f'../data/{worldpop_tif}')
    worldpop = worldpop.read(1)
    dists = np.full(worldpop.shape, -99999, dtype=np.float32)
    land_idxs = np.argwhere(worldpop != -99999)
    del worldpop
    
    # read in electrical grid and find electrical grid coordinates
    grid_tif = 'nigeria_electrical_grid.tif'
    grid = rio.open(f'data/dev_seed/{grid_tif}')
    grid = grid.read(1)
    grid_idxs = np.argwhere(grid == 1)
    del grid

    # check how far we've come with calculating the distances
    i = 0
    if os.path.isfile('data/current_idx.npy'):
        i = np.load('data/current_idx.npy')
        dists = np.load('data/nigeria_electrical_grid_distances.npy')
        land_idxs = land_idxs[i:]
    
    print('Done!')
    print('Calculating distances..')

    # calculate distances to electrical grid
    dists = calc_min_dists(grid_idxs, land_idxs, dists, i)
    np.save('data/nigeria_electrical_grid_distances.npy', dists)

    print('Done!')

    return dists



def calc_min_dists(grid, land, dists, i):
    surrounding_x = 3000
    surrounding_y = 3000

    for land_point in tqdm(land):
        i += 1
        land_point_y, land_point_x = land_point
        
        x_min = max([0, land_point_x-surrounding_x])
        x_max = land_point_x+surrounding_x
        y_min = max([0, land_point_y-surrounding_y])
        y_max = land_point_y+surrounding_y

        grid_idxs_x = np.logical_and(x_min < grid[:, 1], grid[:, 1] < x_max)
        grid_idxs_y = np.logical_and(y_min < grid[:, 0], grid[:, 0] < y_max)
        grid_idxs = np.flatnonzero(np.logical_and(grid_idxs_x, grid_idxs_y))

        dists_to_grid = np.linalg.norm(grid[grid_idxs]-land_point, axis=1)
        dists[land_point_y, land_point_x] = dists_to_grid.min()

        if i % 100000 == 0:
            np.save('data/current_idx.npy', i)
            np.save('data/nigeria_electrical_grid_distances.npy', dists)
    return dists





