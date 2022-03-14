"""

Functions for use in Seurasaari trees notebook (Raster lesson of Introduction to Python GIS at CSC 2022)

last updated: 10.03.2022

"""
#################################
#download_from_url (adjusted from AutoGIS course material)

import os
import urllib

def get_filename(url):
    """
    Parses filename from given url
    """
    if url.find('/'):
        return url.rsplit('/', 1)[1]

def download_data(url):
    """
    Downloads data from given url
    """
    
    # Filepaths
    outdir = r"data"

    # Create folder if it does not exist
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    # Parse filename
    fname = get_filename(url)
    outfp = os.path.join(outdir, fname)
    # Download the file if it does not exist already
    if not os.path.exists(outfp):
        print("Downloading", fname)
        r = urllib.request.urlretrieve(url, outfp)


#################################

# histogram stretch

import numpy as np

def stretch(array):
    """
    remove lowest and highest 2 percentile and perform histogram stretch on array
    """
    
    min_percent = 2   
    max_percent = 98  
    lowp, highp = np.nanpercentile(array, (min_percent, max_percent))

    # Apply linear "stretch" from lowp to highp 
    outar = (array.astype(float) - lowp) / (highp-lowp)

    #fix range to (0 to 1) 
    outar = np.maximum(np.minimum(outar*1, 1), 0)

    return outar

#################################

# get corine legend from excel file

import pandas as pd

def excel_to_df(catxls):
    # read excel file into dataframe
    catdf = pd.read_excel(catxls, index_col=None)
    # limit dataframe from excel to only contain class value and its english name (level4)
    catdf_lim = catdf[["Value","Level4Eng"]].set_index("Value")
    return catdf_lim


def get_corine_dict(catxls):
    """
    transform limited dataframe from excel to dictionary
    """
    catdf_lim = excel_to_df(catxls)
    # transform to dictionary
    catdict = catdf_lim.to_dict()["Level4Eng"]

    return catdict

#################################

#get_json_feature

import json

def getFeatures(gdf):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    
    return [json.loads(gdf.to_json())["features"][0]["geometry"]]


#################################

#for false color image

import rasterio

def read_band(s2, bandnumber):
    """
    reads band, rescales and removes artifacts from array
    """
    
    # read band into array
    band = s2.read(bandnumber)
    # rescale
    band = band / 10000
    # remove all artifacts
    band[ band>1 ] = 1

    return band

import numpy as np

def make_false_color_stack(raster):
    """
    read nir,red,green, stretch and create stack of arrays for false color composite
    """

    nir = read_band(raster,4)
    red = read_band(raster,3)
    green = read_band(raster,2)

    nirs = stretch(nir)
    reds = stretch(red)
    greens = stretch(green)

    # Create RGB false color composite stack
    rgb = np.dstack((nirs, reds, greens))

    return rgb

#################################

#zonal_stats_percentage

def get_zonal_stats_percentage(zstats):
    """
    transforms the result of categorical zonal stats from number of pixels into rounded percentages of the whole polygon
    """

    zstat_perc = {}
    # total amount of pixels is stored as 'count'
    total = zstats[0]["count"]
    # loop through classes
    for key in zstats[0].keys():
        if not key == "count":
            # calcualate percentage of total and store in dictionary
            amount = zstats[0][key]
            perc=  round(amount/total *100)
            zstat_perc[key] = perc

    return zstat_perc


#################################

def get_forest_codes():
    """
    gets codes for all forest classes from corine dataframe
    """
    
    # Lets consider only forest (that is present on Seurasaari)
    forest = ["Broad-leaved forest on mineral soil",
    "Coniferous forest on mineral soil",
    "Coniferous forest on rocky soil",
    "Mixed forest on mineral soil",
    "Mixed forest on rocky soil"]

    # we only need to look at value and english description
    catdf_lim = excel_to_df("https://geoportal.ymparisto.fi/meta/julkinen/dokumentit/CorineMaanpeite2018Luokat.xls")
    # and we only want those classes that include forest
    forestdf = catdf_lim[catdf_lim["Level4Eng"].isin(forest)]
    # as list
    forestcodelist = forestdf.index.to_list()

    return forestcodelist

#################################

# forestmask

def create_forest_mask(corinearray,forestcodes):
    """
    create mask from corine with 1 for forest, 0 other
    """
    # mask places where corine values are those of the forest classes
    mask = (corinearray == int(forestcodes[0])) |  (corinearray == int(forestcodes[1])) | (corinearray == int(forestcodes[2])) | (corinearray == int(forestcodes[3])) | (corinearray == int(forestcodes[4]))
    
    # store as integers
    mask = mask.astype("uint8")
    
    return mask

#################################

#reproject shapefile

import geopandas as gpd

def get_reprojected_shapefilename(rastercrs, shapefilename):
    """
    reproject shapefile to given rastercrs, store it and return its name
    """
    
    # read shapefile into dataframe
    df = gpd.read_file(shapefilename)
    # reproject to rasters CRS
    df = df.to_crs(rastercrs)
    # build the outputname from the inputname
    outname = os.path.join("data",os.path.splitext(os.path.basename(shapefilename))[0] + "_repr_32635.shp")
    # write to disk
    df.to_file(driver = "ESRI Shapefile", filename= outname)
    # return the name of the reprojected shapefile
    return outname
