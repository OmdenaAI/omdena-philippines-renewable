import os
from electrical_grid import download_electrical_grid_for_nigeria
from dist import get_dists
from convert import convert_npy_to_tif

if not os.path.isdir('data'):
    download_electrical_grid_for_nigeria()

dists = get_dists()
convert_npy_to_tif()
