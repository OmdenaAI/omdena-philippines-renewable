import os
import zipfile
from urllib.request import urlretrieve

def download_global_solar_atlas_for_nigeria():
    download_gsa()
    unzip_gsa()



def download_gsa():
    if not os.path.isdir('data'):
        os.makedirs('data')
    
    print('Downloading (this can take a while depending on your connection)..')

    # Global Solar Atlas for Nigeria
    url = 'https://solargis.com/file?url=download/Nigeria/Nigeria_GISdata_LTAym_AvgDailyTotals_GlobalSolarAtlas-v2_GEOTIFF.zip&bucket=globalsolaratlas.info'
    urlretrieve(url, 'data/Nigeria_GISdata_LTAym_AvgDailyTotals_GlobalSolarAtlas-v2_GEOTIFF.zip')
    
    print('Done!')



def unzip_gsa():
    assert os.path.isdir('data')

    print('Unzipping..')

    zip_name = 'Nigeria_GISdata_LTAym_AvgDailyTotals_GlobalSolarAtlas-v2_GEOTIFF.zip'

    # unzip the zip file
    with zipfile.ZipFile(f'data/{zip_name}', 'r') as zip_file:
        zip_file.extractall('data')

    # remove zip file after unzipping
    os.remove(f'data/{zip_name}')
    
    print('Done!')
