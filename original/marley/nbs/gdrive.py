import requests
from google_drive_downloader import GoogleDriveDownloader as gdd

"""
module will download data from gdrive. 
"""
def download_drive(file_id='1K8meQ_vkxD6Eat0YiSZ6NNpkvtPE7y7YLnRMbNpPmNw',
                   dest_path = 'data/clusters.xlsx',
                  unzip=False):
    """
file_id can be retrieve by go to shareable link of a specific file. The last part before '/view'of link will be file_id
"""
    return gdd.download_file_from_google_drive(file_id=file_id,
                                    dest_path=dest_path,
                                    unzip=unzip)