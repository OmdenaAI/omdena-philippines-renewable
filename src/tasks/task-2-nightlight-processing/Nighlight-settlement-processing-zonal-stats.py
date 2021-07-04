"""
## What this notebook is about

- This notebook aims to compute the mean, max, and min nighlight values in settlement areas at municipal level.

### Data
1. [Regional administrative boundaries]
(https://github.com/faeldon/philippines-json-maps/tree/master/topojson/regions/hires)
2. [Municipal administrative boundaries (ph_municities.geojson)]
(https://drive.google.com/drive/u/0/folders/1eiAlQB058M5F-aGEnS9YtQv44gV08-yi)
3. [Nighlight raster file (clipped_ph_nl_median_masked_2020.tif)]
(https://drive.google.com/drive/u/0/folders/1eiAlQB058M5F-aGEnS9YtQv44gV08-yi)
4. [Settlement raster file ("hrsl_phl_settlement.tif" from hrsl_phl_v1.zip)]
(https://drive.google.com/drive/u/0/folders/1xWZiuBcf7PqKpmBgL5NFDVAjhgdP87wD)

### Steps

1. Open Region and Municipal administrative shapefiles in geopandas
2. Open nightlight and settlement rasters and clip per region
3. Upsample and match bounds of nighlight to settlement (to enable raster calculation later)
4. Perform raster calculation to settlement and nightlight (multiply the two rasters to filter out nightlight
values in settlements)
5. Converted output of step 4 to polygons (per specific value) using Rasterio. Only included values greater than zero
5. Filter municipalities per region
6. Perform spatial overlay of municipalities and converted nightlight-settlement polygons
7. Perform aggregation to compute mean, max and min
8. Merge output of aggregation with municipal geodataframe
9. Concat all municipalities and output to shape file / geojson
"""

import argparse
import os
import pandas as pd
import geopandas as gp
import rasterio

from helpers import \
    raster as rh, \
    generic as gh, \
    vector as vh

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def clip_settlement_and_nightlight(slr, nlr, bounds, path, slfile, nlfile, crs=None):
    """Clip settlement and nighlight to input bounds, reproject nightlight to match settlement and save to file"""
    # TODO do clipping using rasterio instead of rioxarray or find method to convert DataArray to rasterio's
    #  DataSetReader to (this is to remove additional step of saving clip and opening again in rasterio)

    func = "clip_settlement_and_nightlight"
    start = gh.print_start_time(func)

    slc = rh.clip_raster_to_geom(slr, [bounds], crs=crs)
    nlc = rh.clip_raster_to_geom(nlr, [bounds], crs=crs)
    nlcr = rh.reproject_match_raster(nlc, slc)
    rh.save_to_file(slc, path, slfile)
    rh.save_to_file(nlcr, path, nlfile)

    gh.print_end_time(func, start)


def compute_statistics(gdf, field, index=0):
    '''Compute the settlement/nightlight areas per polygon'''

    gdf = vh.compute_area(gdf)
    gdf["val1"] = (gdf["values"] * gdf["area"])
    # gdf.to_file(os.path.join(temp_path, "muni_overlay_{}.shp".format(index)))

    '''8. Perform aggregation to compute mean, max and min'''
    gdf_g = gdf.groupby([field]).agg(
        sum=("val1", "sum"),
        max=("values", "max"),
        min=("values", "min"),
        lit_area=("area", "sum")
    ).reset_index()
    gdf_g["mean"] = gdf_g["sum"] / gdf_g["lit_area"]
    # print(gdf_g.head(2))

    return gdf_g


def merge_settlement_and_nightlight(slfile, nlfile, path):
    """
    Open clipped settlement and nightlight, get raster properties of settlement, mask settlement to remove nodata
    values, mask nightlight to only get values greater than zero, multiply masked rasters to get intersection
    """

    func = "merge_settlement_and_nightlight"
    start = gh.print_start_time(func)

    sl = rh.open_raster(os.path.join(path, slfile))
    transform_prop = rh.get_raster_transform_properties(sl)
    sl_band_m = rh.mask_raster(sl, band=1, op="eq", val=sl.nodata)
    sl_band_mf = rh.fill_raster_mask(sl_band_m, 0)

    '''nightlight with values'''
    nl = rh.open_raster(os.path.join(path, nlfile))
    nl_band_m = rh.mask_raster(nl, band=1, op="lte", val=0)
    nl_band_mf = rh.fill_raster_mask(nl_band_m, 0)

    '''nightlight with 0 values'''
    nl_band_0v = rh.mask_raster(nl, band=1, op="ne", val=0)
    nl_band_0v[nl_band_0v == 0] = 1
    nl_band_0v_mf = rh.fill_raster_mask(nl_band_0v, 0)

    sl_with_nl = sl_band_mf * nl_band_mf
    sl_without_nl = sl_band_mf * nl_band_0v_mf

    gh.print_end_time(func, start)

    return sl_with_nl, sl_without_nl, transform_prop


def process_no_nightlight_areas(raster, admin_boundary, properties, field, index=0):
    '''process areas with no nightlight'''

    raster = raster.astype(rasterio.float32)
    results = rh.create_raster_shapes(raster, properties, mask=raster > 0)
    no_nightlight = vh.geojson_to_geodataframe(results)
    # no_nightlight.to_file(os.path.join(temp_path, "no_nightlight_{}.shp".format(index)))

    admin_overlay = vh.perform_overlay(admin_boundary, no_nightlight)
    admin_overlay = vh.compute_area(admin_overlay)
    admin_overlay_g = admin_overlay.groupby([field]).agg(nolit_area=("area", "sum")).reset_index()

    return admin_overlay_g


def process_nightlight_settlement_data(path, nightlight, settlement, regions, municipalities):
    """Process nightlight and settlement data"""

    function = "process_nightlight_settlement_data"
    start = gh.print_start_time(function)

    '''WGS 84 coordinate system used by all data'''
    wgs_crs = "EPSG:4326"

    '''Create a temporary output directory, disregard warning message if folder has already been created'''
    temp_path = gh.create_directory(os.path.join(os.getcwd(), "temp"))

    '''
    Open municipal administrative boundaries using geopandas
    Print first two rows in geodataframe to check the data
    Look for column that is the same with regions to use for filtering later (e.g. ADM1_PCODE)
    Also check which column to use later for aggregation (e.g. ADM3_EN)
    '''
    munis_gdf = vh.shp_to_geodataframe(os.path.join(path, municipalities))
    # print(munis_gdf.head(2))

    '''
    Open regional administrative boundaries using geopandas
    # Print first two rows in geodataframe to check the data
    # Look for column that is the same with municipalities to use for filtering later (e.g. ADM1_PCODE)
    '''
    regions_gdf = vh.shp_to_geodataframe(os.path.join(path, regions))
    # print(regions_gdf.head(2))

    '''fields to use in filtering'''
    muni_field = "ADM3_EN"
    region_field = "ADM1_PCODE"

    '''Open nighlight raster using rioxarray'''
    nl_raster = rh.open_raster_rio(os.path.join(path, nightlight))
    '''To check raster properties (optional)'''
    # nl_raster_prop = rh.get_raster_properties_rio(nl_raster)
    # print(nl_raster_prop)

    '''Open settlement raster using rioxarray'''
    sl_raster = rh.open_raster_rio(os.path.join(path, settlement), masked=False)

    '''Running the process per region is not necessary but to speed processing time, this is opted'''
    gdfs = []
    for i, region in regions_gdf.iterrows():
        print("{}: running region: {}".format(i + 1, region[region_field]))

        '''Get total bounds of region'''
        region_bound = vh.create_shapely_box(region.geometry)
        # print("bounds: {}".format(region_bound))

        '''2-3. Clip settlement and nightlight and match latter with former'''
        slfile = os.path.splitext(settlement)[0] + "_{}.tif".format(i)
        nlfile = os.path.splitext(nightlight)[0] + "_{}.tif".format(i)
        clip_settlement_and_nightlight(
            sl_raster,
            nl_raster,
            region_bound,
            temp_path,
            slfile,
            nlfile,
            crs=wgs_crs
        )

        '''4. If you want to merge settlement and nightlight to only get nightlight in settlement areas'''
        sl_with_nl, sl_without_nl, sl_properties = merge_settlement_and_nightlight(slfile, nlfile, temp_path)

        '''5. Nightlight to polygon (only include values greater than zero)'''
        sl_with_nl2 = sl_with_nl.astype(rasterio.float32)  # transforms float64 to float32
        results = rh.create_raster_shapes(sl_with_nl2, sl_properties, mask=sl_with_nl2 > 0)
        nightlight_gdf = vh.geojson_to_geodataframe(results)
        '''Write to file if you want to check the output in another program such as QGIS'''
        # nightlight_gdf.to_file(os.path.join(temp_path, "nightlight_{}.shp".format(i)))

        '''6. Filter municipalities based on region'''
        muni_region_gdf = munis_gdf[munis_gdf[region_field] == region[region_field]]
        if not len(muni_region_gdf):
            continue

        '''If you want to check the filtered municipalities'''
        # print(muni_region_gdf.head(2))

        '''7. Perform spatial overlay of municipalities and converted nightlight-settlement polygons
        and Compute the settlement/nightlight areas per polygon
        '''
        with_light = vh.perform_overlay(muni_region_gdf, nightlight_gdf)
        with_light_g = compute_statistics(with_light, muni_field, index=i)
        no_light_g = process_no_nightlight_areas(sl_without_nl, muni_region_gdf, sl_properties, muni_field, index=i)

        merged_dfs = pd.merge(no_light_g, with_light_g, on=muni_field)
        merged_dfs["total_area"] = merged_dfs["nolit_area"] + merged_dfs["lit_area"]
        merged_dfs["nolit_per"] = (merged_dfs["nolit_area"] / merged_dfs["total_area"]) * 100
        merged_dfs["lit_per"] = (merged_dfs["lit_area"] / merged_dfs["total_area"]) * 100
        merged_dfs = vh.drop_columns_dataframe(merged_dfs, ["sum", "nolit_area", "lit_area"])
        # print(merged_dfs.head(3))

        '''Since the output of aggregation did not retain the geometry, merge the statistics
        to original muicipalities'''
        muni_overlay_gm = vh.create_geodataframe(
            muni_region_gdf.merge(
                merged_dfs,
                on=muni_field,
                how='left')
        )
        # print(muni_overlay_gm.head(3))
        gdfs.append(muni_overlay_gm)

    print("Done with processing regions")
    gdf = vh.create_geodataframe(pd.concat(gdfs))
    output_path = gh.create_directory(os.path.join(os.getcwd(), "final_output"))
    output = os.path.join(output_path, "Nightlight_muni_stats.shp")
    gdf.to_file(output, crs=wgs_crs)

    # TODO remove temporary files created during clipping
    # TODO split this function to smaller functions for better readability
    gh.print_end_time(function, start)

    return output, temp_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script to process nightlight and settlement and compute zonal '
                                                 'statistics.')
    required = parser.add_argument_group('required arguments')
    arguments = [
        ('--path', 'folder where all the inputs are saved'),
        ('--region', 'region geojson / shapefile (including extension) to use for processing'),
        ('--muni', 'municipal geojson / shapefile (including extension) to use for processing'),
        ('--nightlight', 'nightlight raster (including extension)'),
        ('--settlement', 'settlement raster (including extension)')
    ]
    for arg in arguments:
        required.add_argument(arg[0], type=str, help=arg[1], required=True)

    parser.add_argument('--del_temp', type=str, help='delete temporary files created during processing?')
    args = parser.parse_args()

    try:
        output, temp_path = process_nightlight_settlement_data(
            args.path,
            args.nightlight,
            args.settlement,
            args.region,
            args.muni)

        if args.del_temp and str(args.del_temp) == "true":
            print("removing temporary folder: {}".format(temp_path))
            gh.remove_directory(temp_path)

        print("Additional columns were added in shapefile: max, min, mean, total_area, nolit_per, lit_per")
        print("Results in: {}".format(output))
    except Exception as err:
        print("Error encountered: {}".format(err))
