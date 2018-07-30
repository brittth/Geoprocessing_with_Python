# ####################################### LOAD REQUIRED LIBRARIES ############################################# #

import time
import os
from osgeo import gdal, ogr, osr
import numpy as np
import struct
import geopandas as gpd
import pandas as pd

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
#countries = ogr.Open(rootFolder + "ZonalShape_Countries_Europe_NUTS1_multipart.shp", 1)
#countries_lyr = countries.GetLayer()
#countries_sr = countries_lyr.GetSpatialRef()

#ALTERNATIVE, both work
countries = rootFolder + "ZonalShape_Countries_Europe_NUTS1_multipart.shp"
driver = ogr.GetDriverByName("ESRI Shapefile")
countries = driver.Open(countries, 0)
countries_lyr = countries.GetLayer()
countries_sr = countries_lyr.GetSpatialRef()

dams = ogr.Open(rootFolder + "GRanD_dams_v1_1_Europe-sub.shp", 1)
dams_lyr = dams.GetLayer()
dams_sr = dams_lyr.GetSpatialRef()

roads = ogr.Open(rootFolder + "gRoads-v1-Europe-sub.shp", 1)
roads_lyr = roads.GetLayer()
roads_sr = roads_lyr.GetSpatialRef()


# CHECK SPATIAL REFERENCE AND CREATE TRANSFORMATION RULES
if str(countries_sr) == str(roads_sr) == str(dams_sr):  #only works with str in front
    print("All files share the same spatial reference. No transformation needed!\n")
else:
    print("NOT all files share the same spatial reference. Transformation needed!\n")
#dams_trans = osr.CoordinateTransformation(dams_sr, countries_sr)    # transformation rule: dams --> countries
#roads_trans = osr.CoordinateTransformation(roads_sr, countries_sr)  # transformation rule: roads --> countries


# PREPARE DATA DICTIONARY FOR SUMMARY DATASET
keys = ['country','area_km2','nr_dams','yr_old','name_old','yr_young','name_young','av_reserv_km2',
        'max_reserv_km2','Name_max_reserv','av_depth_reserv_m','max_depth_reserv_m','Name_max_reserv',
        'max_catch_km2','Name_max_catch','roads_km','roads_dist_km','max_road_dist','nr_roads']
values = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
dataset = dict(zip(keys, values))
#print(dataset)


# PREPARE COUNTRY LIST FOR DATA AGGREGATION
country_list = list(set([polygon.GetField('NAME_0') for polygon in countries_lyr]))
print("Country list: \n",country_list,"\n")


# EXTRACT INFORMATION
# Go through each country
for country in country_list:
    polyID = 0                                                      # for tracking
    dataset['country'].append(country)                              # store country name in dataset INFO#1
    area_km2_list = []                                              # prepare for area_km2 data aggregation
    countries_lyr.ResetReading()                                    # before each use of loop on country_lyr

    # Check each polygon for the designated country
    polygon = countries_lyr.GetNextFeature()                        # loop through features
    nr_dams = 0
    while polygon:
        # If designated country is found, extract information
        if polygon.GetField('NAME_0')== country:
            #print("Country : ", country, "   Polygon #", polyID)    # for tracking
            area_km2_list.append(polygon.GetField('area_km2'))      # store area_km2 for data aggregation INFO#2
            #print("Data extraction from polygon shapefile (countries) complete!")

            polygon_geom = polygon.GetGeometryRef()                 # get geometry of polygon
            #polygon_geom = polygon.geometry().Clone()

            dams_lyr.ResetReading()                                 # before each use of loop on dams_lyr
            pointID = 0                                             # for tracking
            point = dams_lyr.GetNextFeature()                        # loop through features
            while point:
                #print("pointID: ", pointID)                         # for tracking
                # On-the-fly transformation of point data (dams) to match spatial reference of polygon data (countries)
                point_geom = point.GetGeometryRef()
                point_geom_trans = TransformGeometry(point_geom, countries_sr)
                #print(point_geom)
                #print(point_geom_trans)

                if polygon_geom.Contains(point_geom_trans):
                    nr_dams += 1
                    print("Country : ", country, "   Polygon #",polyID, "   Dams #", nr_dams)  # for tracking



                #point_geom_trans.SetSpatialFilter(polygon_geom)
                #nr_dams_poly = point_geom_trans.GetFeatureCount()
                #print(nr_dams_poly)

                #if polygon_geom.Contains(point_geom_trans):
                #    print("Point #",pointID," lies within polygon!")

                pointID += 1
                point = dams_lyr.GetNextFeature()

                #if polygon.Contains(point_geom_cl):
                #polygon.SetSpatialFilter(point_geom_cl)
                #count = polygon.GetFeatureCount()
                #print("nr_dams: ", count)
                    #print("contains")


            # On-the-fly transformation of line data (roads)to match spatial reference of polygon data (countries)
            #line_geom = line.GetGeometryRef()
            #line_geom_trans = TransformGeometry(line_geom, countries_sr)
            polyID += 1                                             # for tracking
        #print(nr_dams)
        polygon = countries_lyr.GetNextFeature()


    # Aggregate and store area_km2 per country
    area_km2 = sum(area_km2_list)                                   # add up area_km2 values for all polygons of one country
    dataset['area_km2'].append(area_km2)                            # store the area_km2 result in dataset
    # Aggregate and store nr_dams per country
    dataset['nr_dams'].append(nr_dams)  # store number of dams in dataset INFO#3
print(dataset)


# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #

print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")