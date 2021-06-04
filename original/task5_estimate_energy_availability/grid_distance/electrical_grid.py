import os
import zipfile
import geopandas as gpd
import rasterio as rio
from rasterio import features
from urllib.request import urlretrieve

def download_electrical_grid_for_nigeria():
    download_grid()
    unzip_grid()
    rasterize_grid()



def download_grid():
    if not os.path.isdir('data/dev_seed'):
        os.makedirs('data/dev_seed')

    print('Downloading..')
    
    #url = 'https://development-data-hub-s3-public.s3.amazonaws.com/ddhfiles/99888/geospatial/AICD/Power%20Transmission/nigeria-electricity-transmission-network.zip'
    url = 'https://development-data-hub-s3-public.s3.amazonaws.com/ddhfiles/148149/nigeria_at_03-08-2018.geojson.zip'

    # save the zip
    file_name = url.split('/')[-1]
    urlretrieve(url, f'data/dev_seed/{file_name}')
    
    print('Done!')



def unzip_grid():
    assert os.path.isdir('data/dev_seed')

    print('Unzipping..')

    # unzip the transmission grid zip
    #grid_zip = 'nigeria-electricity-transmission-network.zip'
    grid_zip = 'nigeria_at_03-08-2018.geojson.zip'
    with zipfile.ZipFile(f'data/dev_seed/{grid_zip}', 'r') as zip_file:
        zip_file.extractall('data/dev_seed')
    
    # remove zip file after unzipping
    os.remove(f'data/dev_seed/{grid_zip}')

    print('Done!')



def rasterize_grid():
    """
    Converts shapefile of electrical grid to tif.
    Requires the worldpop tif as template in directory: task5_estimate_energy_availability/data/nga_ppp_2020.tif.

    Accustomed from: https://gis.stackexchange.com/questions/151339/rasterize-a-shapefile-with-geopandas-or-fiona-python
    """

    print('Rasterizing..')

    #grid_file = 'Nigeria Electricity Transmission Network.shp'
    grid_file = 'nigeria_at_03-08-2018.geojson'
    worldpop_file = '../data/nga_ppp_2020.tif'
    output_file = 'nigeria_electrical_grid.tif'

    grid = gpd.read_file(f'data/dev_seed/{grid_file}/{grid_file}')
    raster = rio.open(worldpop_file)
    meta = raster.meta.copy()

    with rio.open(f'data/dev_seed/{output_file}', 'w+', **meta) as out:
        grid_array = out.read(1)

        shapes = [geom for geom in grid["geometry"]]

        grid_array = features.rasterize(shapes=shapes, out=grid_array, transform=out.transform)
        out.write_band(1, grid_array)
    
    print('Done!')

