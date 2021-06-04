""" functions that depend on qgis

easiest to run inside the qgis console
alternatively can run in a qgis environment but this is not easy to configure
"""
from qgis.analysis import QgsAlignRaster as AR
from os.path import splitext

def align(src, tgt):
    """
    align files to same long/lat/crs/shape and save to f"{filename}_aligned.tif"
    run from qgis console (or in own qgis environment which is not easy to create)

    :param src: localpath to tiff file or list of paths
    :param tgt: localpath to tiff file with format for alignment

    .. note:: copies np.nan values but not "nodata" metadata so this has to be set manually in qgis if required
    """
    ar = AR()

    # sources
    if isinstance(src, str):
        src = [src]
    sources = []
    for f in src:
        name, ext = splitext(f)
        src_item = ar.Item(f, f"{name}_rescaled{ext}")
        src_item.resampleMethod = ar.RA_Bilinear
        sources.append(src_item)

    # target
    name, ext = splitext(tgt)
    tgt_item = ar.Item(tgt, f"{name}_rescaled{ext}")

    # run
    ar.setRasters([src_item])
    ar.setParametersFromRaster(ar.RasterInfo(tgt_item))
    #ar.setProgressHandler(ProgressHandler())
    ar.run()

    # todo - TO BE TESTED
    # class ProgressHandler(AR.ProgressHandler):
    # 	def progress(complete):
    # 		if complete*100 % 10 == 0:
    # 			print(f"{int(complete)}% completed")
    # 		return True

def test():
    lights = r"D:\omdena\lights\NOAA_VIIRS_DNB_MONTHLY_V1_VCMCFG.avg_rad.tif"
    population = r"D:\omdena\population\WorldPop_GP_100m_pop.population.tif"
    align(lights, population)