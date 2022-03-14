#!/usr/bin/env python3

"""
Script for the preparation of raster lesson Sentinel 2 data
-- not part of the course, data prepared with this is provided: https://a3s.fi/gis-courses/pythongis_2022/S2B_RGBNIR_20210926_Helsinki.tif ---
"""


import os
import rasterio
from rasterio.mask import mask
import fiona
from fiona.transform import transform_geom
import numpy as np
import glob


def find_bands(S2SAFEfile, pixelsize):
    """
    find bands from Sentinel-2 SAFE "file" with given pixelsize
    """
    
    bandlocation =  [S2SAFEfile,'*','*','IMG_DATA']
    
    bandpaths = {}
    # we want r,g,b and nir at 10 m spatial resolution
    for band in [2,3,4,8]:
        pathbuildinglist =  bandlocation + ['R' + str(pixelsize) + 'm','*' + str(band)+ '_' + str(pixelsize) +'m.jp2'] 
        bandpathpattern = os.path.join(*pathbuildinglist)
        bandpath = glob.glob(bandpathpattern)[0]
    
        bandpaths[band] = bandpath

    #type: dict[bandnumber] - bandpath
    return bandpaths


def create_multiband_tif(bandpaths):
    """
    create multiband geotif file from given bandpathdict
    """

    outfilename = "./data/S2B_RGBNIR_20210926.tif"
    with rasterio.open(bandpaths[4]) as src:
        meta = src.meta
        crs = src.crs
        out_meta = meta.copy()
        out_meta.update({"driver": "GTiff","count":4})
    with rasterio.open(outfilename, "w", **out_meta) as dest:
        for i,band in enumerate(bandpaths.keys()):
            with rasterio.open(bandpaths[band]) as src:
                banddata = src.read(1)
                dest.write(banddata, i+1)

    return outfilename, crs


def read_shapefile():
    """
    reads in shapefile of Finland municipalities and returns geometry of Helsinki polygon
    """

    with fiona.open("../L2/data/finland_municipalities.shp", "r") as shapefile:
        polygons = [feature["geometry"] for feature in shapefile] if feature['properties']['name'] == 'Helsinki'])
        #polycrs = str(shapefile.crs['init']).upper()
    return polygons#, polycrs


def clip_area(mytif, polygons, outname):
    """
    clip area of polygons from input raster file
    """
    
    with rasterio.open(mytif) as src:
        out_image, out_transform = mask(src, polygons, crop=True)
        out_meta = src.meta
        out_meta.update({"driver": "GTiff",
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": out_transform})

   
    with rasterio.open(outname, "w", **out_meta) as dest:
        dest.write(out_image)

# Process for getting Sentinel2 4 band raster of Helsinki
bandpaths = find_bands("./data/S2B_MSIL2A_20210926T094029_N0301_R036_T35VLG_20210926T110446.SAFE",10)
mytif,crs= create_multiband_tif(bandpaths)
polygon = read_shapefile()
clip_area(mytif, polygon, "./data/S2B_RGBNIR_20210926_Helsinki.tif")
