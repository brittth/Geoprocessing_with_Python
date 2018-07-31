'''
import sys
try:
    from osgeo import ogr, osr, gdal
except:
    sys.exit('ERROR: cannot find GDAL/OGR modules')

# example GDAL error handler function
def gdal_error_handler(err_class, err_num, err_msg):
    errtype = {
            gdal.CE_None:'None',
            gdal.CE_Debug:'Debug',
            gdal.CE_Warning:'Warning',
            gdal.CE_Failure:'Failure',
            gdal.CE_Fatal:'Fatal'
    }
    err_msg = err_msg.replace('\n',' ')
    err_class = errtype.get(err_class, 'None')
    print ('Error Number: %s' % (err_num))
    print ('Error Type: %s' % (err_class))
    print ('Error Message: %s' % (err_msg))

if __name__=='__main__':

    # install error handler
    gdal.PushErrorHandler(gdal_error_handler)

    # Raise a dummy error
    gdal.Error(1, 2, 'test error')

    #uninstall error handler
    gdal.PopErrorHandler()
'''
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
#countries = ogr.Open(rootFolder + "ZonalShape_Countries_Europe_NUTS1_multipart.shp", 1)
#countries_lyr = countries.GetLayer()
#countries_sr = countries_lyr.GetSpatialRef()

#ALTERNATIVE, both work
countries = rootFolder + "ZonalShape_Countries_Europe_NUTS1_multipart.shp"
driver = ogr.GetDriverByName("ESRI Shapefile")
countries = driver.Open(countries, 0)
countries_lyr = countries.GetLayer()
countries_sr = countries_lyr.GetSpatialRef()

#dams = ogr.Open(rootFolder + "GRanD_dams_v1_1_Europe-sub.shp", 1)
#dams_lyr = dams.GetLayer()
#dams_sr = dams_lyr.GetSpatialRef()

#ALTERNATIVE, both work
dams = rootFolder + "GRanD_dams_v1_1_Europe-sub.shp"
driver = ogr.GetDriverByName("ESRI Shapefile")
dams = driver.Open(dams, 0)
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
'''
# Go through each country
multipolygon = ogr.Geometry(ogr.wkbMultiPolygon)
#multipolygon.AssignSpatialReference(countries_sr)

for country in country_list:
    polyID = 0                                                      # for tracking
    dataset['country'].append(country)                              # store country name in dataset INFO#1
    area_km2_list = []                                              # prepare for area_km2 data aggregation
    countries_lyr.ResetReading()                                    # before each use of loop on country_lyr

    # Check each polygon for the designated country
    multipolygon = ogr.Geometry(ogr.wkbMultiPolygon)
    polygon = countries_lyr.GetNextFeature()                        # loop through features
    while polygon:
        # If designated country is found, extract information
        if polygon.GetField('NAME_0')== country:
            print("Country : ", country, "   Polygon #", polyID)    # for tracking
            area_km2_list.append(polygon.GetField('area_km2'))      # store area_km2 for data aggregation INFO#2
            polygon_geom = polygon.GetGeometryRef()                 # get geometry of polygon
            multipolygon.AddGeometry(polygon_geom)
            polyID += 1
        polygon = countries_lyr.GetNextFeature()

    print("Country : ", country, " dissolved!")

    #transformation
    # On-the-fly transformation of multipolygon geometry (country) to match spatial reference of point data (dams)
    #multipolygon_trans = TransformGeometry(multipolygon, dams_sr)

    geom_sref= multipolygon.GetSpatialReference()
    transform = osr.CoordinateTransformation(geom_sref, dams_sr)
    geom_trans = multipolygon.Clone()
    geom_trans.Transform(transform)

    #dams_lyr.SetSpatialFilter(multipolygon_trans)
    #nr_dams = dams_lyr.GetFeatureCount()
    #print("Country : ", country, "   Polygon #", polyID, "   DamsPOLY #", nr_dams)  # for tracking


    # Aggregate and store area_km2 per country
    area_km2 = sum(area_km2_list)  # add up area_km2 values for all polygons of one country
    dataset['area_km2'].append(area_km2)  # store the area_km2 result in dataset
print(dataset)
'''

# EXTRACT INFORMATION
print("Extract information:")
# Go through each country
for country in country_list:
    polyID = 1                                                      # for tracking
    area_km2_list = []                                              # prepare for area_km2 data aggregation

    # Check each polygon for the designated country
    # initialize dam information storage
    nr_dams = 0
    keys_dams = ['DAM_NAME', 'YEAR', 'AREA_SKM', 'DEPTH_M', 'CATCH_SKM']
    values_dams = [[], [], [], [], []]
    dataset_dams = dict(zip(keys_dams, values_dams))

    multipolygon = ogr.Geometry(ogr.wkbMultiPolygon)                # multipolygon to store all polygons of a country
    countries_lyr.ResetReading()                                    # before each use of loop on country_lyr
    polygon = countries_lyr.GetNextFeature()                        # loop through features
    while polygon:
        # If designated country is found, extract information
        if polygon.GetField('NAME_0')== country:
            #print("Country : ", country, "   Polygon #", polyID)    # for tracking
            area_km2_list.append(polygon.GetField('area_km2'))      # store area_km2 for data aggregation INFO#2
            polygon_geom = polygon.GetGeometryRef()                 # get geometry of polygon
            multipolygon.AddGeometry(polygon_geom)                  # add polygon to multipolygon (country)
            polyID += 1                                             # for tracking
        polygon = countries_lyr.GetNextFeature()

    print("Country : ", country, "   Number of dissolved polygons : ", polyID)

    # extract dams data per country (multipolygon)
    dams_lyr.ResetReading()                                         # before each use of loop on dams_lyr
    point = dams_lyr.GetNextFeature()                               # loop through features
    while point:
        # On-the-fly transformation of point geometry (dams) to match spatial reference of polygon data (countries)
        point_geom = point.GetGeometryRef()
        point_geom_trans = TransformGeometry(point_geom, countries_sr)
        if multipolygon.Contains(point_geom_trans):
            nr_dams += 1                                                # count number of dams INFO#3
            dataset_dams['DAM_NAME'].append(point.GetField('DAM_NAME')) # INFO#5,7,10,13,15
            dataset_dams['YEAR'].append(point.GetField('YEAR'))         # INFO#4,6
            dataset_dams['AREA_SKM'].append(point.GetField('AREA_SKM')) # INFO#8,9
            dataset_dams['DEPTH_M'].append(point.GetField('DEPTH_M'))   # INFO#11,12
            dataset_dams['CATCH_SKM'].append(point.GetField('CATCH_SKM'))# INFO#13,14
        point = dams_lyr.GetNextFeature()

    print("Country : ", country, "   Number of damns", nr_dams,"\n")  # for tracking

    # AGGREGATE/CALCULATE RESULTS
    area_km2 = sum(area_km2_list)                                   # add up area_km2 values for all polygons of one country
    if nr_dams != 0:
        yr_old = min(dataset_dams['YEAR'])                          # yr_old: year of establishment of oldest dam INFO#4
        i_old = ((dataset_dams['YEAR']).index(yr_old))              # get index of yr_old
        name_old = dataset_dams['DAM_NAME'][i_old]                  # name_old: name of oldest dam INFO#5
        yr_young = max(dataset_dams['YEAR'])                        # yr_young: year of establishment of youngest dam INFO#6
        i_young = ((dataset_dams['YEAR']).index(yr_young))          # get index of yr_young
        name_young = dataset_dams['DAM_NAME'][i_young]              # name_young: name of youngest dam INFO#7
        av_reserv_km2 = mean(dataset_dams['AREA_SKM'])              # av_reserv_km2: average reservoir size in km2 INFO#8
        max_reserv_km2 = max(dataset_dams['AREA_SKM'])              # max_reserv_km2: maximum size of reservoir in km2 INFO#9
        i_max = ((dataset_dams['AREA_SKM']).index(max_reserv_km2))  # get index of max_reserv_km2
        Name_max_reserv = dataset_dams['DAM_NAME'][i_max]           # Name_max_reserv: name of the dam with largest reservoir INFO#10
        av_depth_reserv_m = mean(dataset_dams['DEPTH_M'])           # av_depth_reserv_m: average depth of reservoirs in m INFO#11
        max_depth_reserv_m = max(dataset_dams['DEPTH_M'])           # max_depth_reserv_m: maximum depth of reservoirs in m INFO#12
        i_max_d = ((dataset_dams['DEPTH_M']).index(max_depth_reserv_m))  # get index of max_depth_reserv_m
        Name_max_reserv_m = dataset_dams['DAM_NAME'][i_max_d]         # Name_max_reserv: name of dam with deepest reservoir INFO#13
        max_catch_km2 = max(dataset_dams['CATCH_SKM'])              # max_catch_km2: largest catchment in km2 INFO#14
        i_max_c = ((dataset_dams['CATCH_SKM']).index(max_catch_km2))  # get index of max_catch_km2
        Name_max_catch = dataset_dams['DAM_NAME'][i_max_c]         # Name_max_catch: name of the dam with the largest catchment INFO#15
    else:
        yr_old = "--"
        yr_young = "--"
        name_young = "--"
        av_reserv_km2 = "--"
        max_reserv_km2 = "--"
        Name_max_reserv = "--"
        av_depth_reserv_m = "--"
        max_depth_reserv_m = "--"
        Name_max_reserv_m = "--"
        max_catch_km2 = "--"
        Name_max_catch = "--"

    print("Country : ", country, "   Dam info:\n", nr_dams, dataset_dams,"\n")  # for tracking


    # STORE RESULTS
    dataset['country'].append(country)                              # store country name in dataset INFO#1
    dataset['area_km2'].append(area_km2)                            # store the area_km2 result in dataset INFO#2
    dataset['nr_dams'].append(nr_dams)                              # store number of dams in dataset INFO#3
    dataset['yr_old'].append(yr_old)# yr_old: year of establishment of oldest dam INFO#4
    dataset['name_old'].append(name_old)# name_old: name of oldest dam INFO#5
    dataset['yr_young'].append(yr_young)# yr_young: year of establishment of youngest dam INFO#6
    dataset['name_young'].append(name_young)# name_young: name of youngest dam INFO#7
    dataset['av_reserv_km2'].append(av_reserv_km2)# av_reserv_km2: average reservoir size in km2 INFO#8
    dataset['max_reserv_km2'].append(max_reserv_km2)# max_reserv_km2: maximum size of reservoir in km2 INFO#9
    dataset['Name_max_reserv'].append(Name_max_reserv)# Name_max_reserv: name of the dam with largest reservoir INFO#10
    dataset['av_depth_reserv_m'].append(av_depth_reserv_m)# av_depth_reserv_m: average depth of reservoirs in m INFO#11
    dataset['max_depth_reserv_m'].append(max_depth_reserv_m)# max_depth_reserv_m: maximum depth of reservoirs in m INFO#12
    dataset['Name_max_reserv_m'].append(Name_max_reserv_m)# Name_max_reserv: name of dam with deepest reservoir INFO#13
    dataset['max_catch_km2'].append(max_catch_km2)# max_catch_km2: largest catchment in km2 INFO#14
    dataset['Name_max_catch'].append(Name_max_catch)# Name_max_catch: name of the dam with the largest catchment INFO#15

print(dataset)


# point_geom_trans.SetSpatialFilter(polygon_geom)
# nr_dams_poly = point_geom_trans.GetFeatureCount()
# print("Country : ", country, "   Polygon #", polyID, "   DamsPOLY #", nr_dams_poly)  # for tracking

# On-the-fly transformation of line data (roads)to match spatial reference of polygon data (countries)
# line_geom = line.GetGeometryRef()
# line_geom_trans = TransformGeometry(line_geom, countries_sr)
# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #

print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")