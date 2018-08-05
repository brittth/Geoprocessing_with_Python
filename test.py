# ####################################### LOAD REQUIRED LIBRARIES ############################################# #

import time
import os
from osgeo import gdal, ogr, osr
import numpy as np
import struct
import geopandas as gpd
import pandas as pd
from statistics import mean

# ####################################### SET TIME-COUNT ###################################################### #

starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")

# ####################################### FUNCTIONS ########################################################### #

# TO BE PUT IN PACKAGE
def TransformGeometry(geometry, target_sref):
    #Returns cloned geometry, which is transformed to target spatial reference
    geom_sref= geometry.GetSpatialReference()
    transform = osr.CoordinateTransformation(geom_sref, target_sref)
    geom_trans = geometry.Clone()
    geom_trans.Transform(transform)
    return geom_trans

# ####################################### FOLDER PATHS & GLOBAL VARIABLES ##################################### #

rootFolder = "D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/MAP/Geoprocessing-in-python_MAP2018_data/Task02_data/"

# ####################################### PROCESSING ########################################################## #

# LOAD DATA FILES
countries = ogr.Open(rootFolder + "ZonalShape_Countries_Europe_NUTS1_multipart.shp", 1)
countries_lyr = countries.GetLayer()
countries_sr = countries_lyr.GetSpatialRef()

#ALTERNATIVE, both work
# countries = rootFolder + "ZonalShape_Countries_Europe_NUTS1_multipart.shp"
# driver = ogr.GetDriverByName("ESRI Shapefile")
# countries = driver.Open(countries, 0)
# countries_lyr = countries.GetLayer()
# countries_sr = countries_lyr.GetSpatialRef()

dams = ogr.Open(rootFolder + "GRanD_dams_v1_1_Europe-sub.shp", 1)
dams_lyr = dams.GetLayer()
dams_sr = dams_lyr.GetSpatialRef()

#ALTERNATIVE, both work
# dams = rootFolder + "GRanD_dams_v1_1_Europe-sub.shp"
# driver = ogr.GetDriverByName("ESRI Shapefile")
# dams = driver.Open(dams, 0)
# dams_lyr = dams.GetLayer()
# dams_sr = dams_lyr.GetSpatialRef()

roads = ogr.Open(rootFolder + "gRoads-v1-Europe-sub.shp", 1)
roads_lyr = roads.GetLayer()
roads_sr = roads_lyr.GetSpatialRef()

#ALTERNATIVE, both work
# roads = rootFolder + "gRoads-v1-Europe-sub.shp"
# driver = ogr.GetDriverByName("ESRI Shapefile")
# roads = driver.Open(roads, 0)
# roads_lyr = roads.GetLayer()
# roads_sr = roads_lyr.GetSpatialRef()


# CHECK SPATIAL REFERENCE AND CREATE TRANSFORMATION RULES
if str(countries_sr) == str(roads_sr) == str(dams_sr):  #only works with str in front
    print("All files share the same spatial reference. No transformation needed!\n")
else:
    print("NOT all files share the same spatial reference. Transformation needed!\n")
dams_trans = osr.CoordinateTransformation(countries_sr, dams_sr)    # transformation rule: dams --> countries
#roads_trans = osr.CoordinateTransformation(countries_sr, roads_sr)  # transformation rule: roads --> countries


# PREPARE DATA DICTIONARY FOR SUMMARY DATASET
keys = ['country','area_km2','nr_dams','yr_old','name_old','yr_young','name_young','av_reserv_km2',
        'max_reserv_km2','Name_max_reserv','av_depth_reserv_m','max_depth_reserv_m','Name_max_reserv_m',
        'max_catch_km2','Name_max_catch','roads_km','roads_dist_km','max_road_dist','nr_roads']
values = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
dataset = dict(zip(keys, values))
#print(dataset)


# PREPARE COUNTRY LIST FOR DATA AGGREGATION
country_list = sorted(list(set([polygon.GetField('NAME_0') for polygon in countries_lyr])))
print("Country list: \n",country_list,"\n")

country_list = country_list[0:3]    # for testing
print(country_list)                 # for testing


# EXTRACT INFORMATION
print("Extract information:")
# Extract country data
for country in country_list:
    # Prepare data storage
    polyID = 0                                                      # for tracking
    area_km2_list = []

    # Extract country data
    # Build multipolygon representing country
    multipolygon = ogr.Geometry(ogr.wkbMultiPolygon)                # multipolygon to store all polygons of a country
    countries_lyr.SetAttributeFilter("NAME_0 = '"+str(country)+"'")
    countries_lyr.ResetReading()                                    # before each use of loop on country_lyr
    polygon = countries_lyr.GetNextFeature()                        # loop through features
    while polygon:
        # If designated country is found, extract information and build country multipolygon
        #if polygon.GetField('NAME_0')== country:
        polygon_geom = polygon.GetGeometryRef()                 # get geometry of polygon
        multipolygon.AddGeometry(polygon_geom)                  # add polygon to multipolygon (country)
        polyID += 1                                             # for tracking
        polygon = countries_lyr.GetNextFeature()

    print("Country : ", country, "   Number of dissolved polygons : ", polyID)

        # Damns
    multipolygon.Transform(dams_trans)  # apply coordinate transformation
    dams_lyr.SetSpatialFilter(multipolygon)
    count = dams_lyr.GetFeatureCount()
    print(count)
