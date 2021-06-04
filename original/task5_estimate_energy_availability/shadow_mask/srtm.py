import os
import zipfile
import rasterio as rio
from rasterio.merge import merge
from urllib.request import urlretrieve

def download_srtm_files_for_nigeria():
    download_srtm()
    unzip_srtm()
    merge_srtm()



def download_srtm():
    if not os.path.isdir('data/srtm'):
        os.makedirs('data/srtm')

    print('Downloading (this can take a while depending on your connection)..')
    
    # version 4 of srtm data from http://srtm.csi.cgiar.org/ over nigeria
    urls = [
        'http://srtm.csi.cgiar.org/wp-content/uploads/files/srtm_5x5/TIFF/srtm_39_11.zip',
        'http://srtm.csi.cgiar.org/wp-content/uploads/files/srtm_5x5/TIFF/srtm_39_10.zip',
        'http://srtm.csi.cgiar.org/wp-content/uploads/files/srtm_5x5/TIFF/srtm_38_12.zip',
        'http://srtm.csi.cgiar.org/wp-content/uploads/files/srtm_5x5/TIFF/srtm_38_11.zip',
        'http://srtm.csi.cgiar.org/wp-content/uploads/files/srtm_5x5/TIFF/srtm_38_10.zip',
        'http://srtm.csi.cgiar.org/wp-content/uploads/files/srtm_5x5/TIFF/srtm_37_11.zip',
        'http://srtm.csi.cgiar.org/wp-content/uploads/files/srtm_5x5/TIFF/srtm_37_10.zip'
    ]

    # save the zip files
    for url in urls:
        file_name = url.split('/')[-1]
        urlretrieve(url, f'data/srtm/{file_name}')
    
    print('Done!')



def unzip_srtm():
    assert os.path.isdir('data/srtm')

    print('Unzipping..')

    # unzip all the download zip files
    for srtm_zip in os.listdir('data/srtm'):
        if '.zip' in srtm_zip:
            with zipfile.ZipFile(f'data/srtm/{srtm_zip}', 'r') as zip_file:
                zip_file.extractall('data/srtm')

            # remove zip file after unzipping
            os.remove(f'data/srtm/{srtm_zip}')
    
    print('Done!')



def merge_srtm():
    print('Merging..')

    srtm_tifs = list()
    # load all tifs into a list
    for i, srtm_tif in enumerate(os.listdir('data/srtm')):
        if '.tif' in srtm_tif:
            tif = rio.open(f'data/srtm/{srtm_tif}')
            srtm_tifs.append(tif)

    # merge all the tifs
    merged_array, transform = rio.merge.merge(srtm_tifs)
    merged_array = merged_array.squeeze()

    # save the merged tif
    merged_tif = rio.open(
        'data/srtm/nigeria_elevation.tif',
        'w',
        driver = tif.meta['driver'],
        count = tif.meta['count'],
        dtype = tif.meta['dtype'],
        nodata = tif.meta['nodata'],
        crs = tif.meta['crs'],
        transform = transform,
        height = merged_array.shape[0],
        width = merged_array.shape[1]
    )
    merged_tif.write(merged_array, 1)

    print('Done!')

    # clean up
    for any_file in os.listdir('data/srtm'):
        if any_file != 'nigeria_elevation.tif' and any_file != 'readme.txt':
            os.remove(f'data/srtm/{any_file}')

