# add functions to ee
import ee
ee.Initialize()
from . import image
from . import imagecollection

# google drive
from . import creds

import fs
from . import config as c
from time import sleep
import fiona

# enable KML support which is disabled by default
fiona.drvsupport.supported_drivers['kml'] = 'rw'
fiona.drvsupport.supported_drivers['KML'] = 'rw'

import logging
log = logging.getLogger()

def gdrive2local(files=None):
    """ download files from google drive to local
    :param files: if provided them will wait for these files. If None then all current files
    """
    gd = fs.open_fs(f"googledrive://{creds.gdrive()}")
    gd = gd.makedirs(c.googlepath, recreate=True)
    local = fs.open_fs(c.localpath)
    if files is None:
        files = gd.listdir("")

    downloaded = set(local.listdir(""))
    while True:
        log.setLevel(logging.WARNING)
        ready = set(files) - downloaded
        log.setLevel(logging.INFO)
        for filename in list(ready):
            with local.open(filename, "wb") as f:
                gd.download(filename, f)
            downloaded.add(filename)
            ready.remove(filename)
            log.info(f"local={len(downloaded)} googledrive={len(files)}")
        if set(files) - set(downloaded):
            continue
        break
        sleep(5)
