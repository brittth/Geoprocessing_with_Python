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
# NOT NECESSARY BECAUSE ONLY ONE LOOP/FILTER USED
# countries_lyr.ResetReading()  # before each use of loop on country_lyr
# dams_lyr.ResetReading()        # before each use of loop on dams_lyr
# roads_lyr.ResetReading()      # before each use of loop on roads_lyr
# dams_lyr.SetSpatialFilter(None)
# roads_lyr.SetSpatialFilter(None)

# ROUNDING
# km data rounded to m level --> 3rd decimal place
# m data rounded to cm level --> 2nd decimal place

# LOAD DATA FILES
countries = ogr.Open(rootFolder + "ZonalShape_Countries_Europe_NUTS1_multipart.shp", 1)
countries_lyr = countries.GetLayer()
countries_sr = countries_lyr.GetSpatialRef()

dams = ogr.Open(rootFolder + "GRanD_dams_v1_1_Europe-sub.shp", 1)
dams_lyr = dams.GetLayer()
dams_sr = dams_lyr.GetSpatialRef()

roads = ogr.Open(rootFolder + "gRoads-v1-Europe-sub.shp", 1)
roads_lyr = roads.GetLayer()
roads_sr = roads_lyr.GetSpatialRef()


# CHECK SPATIAL REFERENCE
if str(countries_sr) == str(roads_sr) == str(dams_sr):
    print("All files share the same spatial reference. No transformation needed!\n")
else:
    print("NOT all files share the same spatial reference. Transformation needed!\n")


# PREPARE DATA DICTIONARY FOR SUMMARY DATASET
keys = ['country','area_km2','nr_dams','yr_old','name_old','yr_young','name_young','av_reserv_km2',
        'max_reserv_km2','Name_max_reserv','av_depth_reserv_m','max_depth_reserv_m','Name_max_depth',
        'max_catch_km2','Name_max_catch','roads_km','road_dist_km','max_road_dist','nr_roads']
values = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
dataset = dict(zip(keys, values))


# PREPARE COUNTRY LIST FOR DATA AGGREGATION
country_list = sorted(list(set([polygon.GetField('NAME_0') for polygon in countries_lyr]))) #sorted to facilitate testing
print("Country list: \n",country_list,"\n")
country_list = country_list[0:3]    # for testing
print(country_list)                 # for testing


# EXTRACT INFORMATION
print("Extract information:")
for country in country_list:        # Countries-INFO#1
    # Prepare data storage
    polyID = 0                      # for tracking
    area_km2_list = []
    #roads_km_list = []             # ALTERNATIVE roads_km: roads_km for all road features in a country
    keys_dams = ['DAM_NAME', 'YEAR', 'AREA_SKM', 'DEPTH_M', 'CATCH_SKM']
    values_dams = [[], [], [], [], []]
    dataset_dams = dict(zip(keys_dams, values_dams))


    # Extract COUNTRY data
    # Create multipolygon representing country
    multipolygon = ogr.Geometry(ogr.wkbMultiPolygon)                # multipolygon to store all polygons of a country
    countries_lyr.SetAttributeFilter("NAME_0 = '"+str(country)+"'") # filter for country
    polygon = countries_lyr.GetNextFeature()                        # loop through features
    while polygon:
        area_km2_list.append(polygon.GetField('area_km2'))          # Countries-INFO#2: for data aggregation/calculation
        polygon_geom = polygon.GetGeometryRef()                     # get geometry of polygon
        multipolygon.AddGeometry(polygon_geom)                      # add polygon geometry to multipolygon (country)
        polyID += 1                                                 # for tracking
        polygon = countries_lyr.GetNextFeature()                    # loop through features

    print("Country : ", country, "   Number of dissolved polygons: ", polyID,".")


    # Extract DAMS data per country (multipolygon)
    # On-the-fly transformation of multipolygon geometry (country) to match spatial reference of point data (dams)
    #multipolygon = TransformGeometry(multipolygon, dams_sr)            # doesn't work because geometry not attached
    dams_trans = osr.CoordinateTransformation(countries_sr, dams_sr)# transformation rule: countries --> dams
    multipolygon.Transform(dams_trans)                              # apply transformation to multipolygon
    dams_lyr.SetSpatialFilter(multipolygon)                         # reduce dams to country geometry (multipolygon)
    nr_dams = dams_lyr.GetFeatureCount()                            # Dams-INFO#1: count number of dam features
    point = dams_lyr.GetNextFeature()                               # loop through features
    while point:
        # for data aggregation/calculation
        dataset_dams['DAM_NAME'].append(point.GetField('DAM_NAME'))     # Dams-INFO#3,5,8,11,13
        dataset_dams['YEAR'].append(point.GetField('YEAR'))             # Dams-INFO#2,4:
        dataset_dams['AREA_SKM'].append(point.GetField('AREA_SKM'))     # Dams-INFO#6,7
        dataset_dams['DEPTH_M'].append(point.GetField('DEPTH_M'))       # Dams-INFO#9,10,11
        dataset_dams['CATCH_SKM'].append(point.GetField('CATCH_SKM'))   # Dams-INFO#12,13
        point = dams_lyr.GetNextFeature()                               # loop through features

    print("Country : ", country, "   Information extracted from ", nr_dams," dams.")


    # Extract ROADS data per country (multipolygon)
    # On-the-fly transformation of multipolygon geometry (country, now in dams_sr) to match spatial reference of line data (roads)
    multipolygon = TransformGeometry(multipolygon, roads_sr)    # transform geometry to road_sr
    roads_lyr.SetSpatialFilter(multipolygon)                    # reduce dams to country geometry (multipolygon)
    nr_roads = roads_lyr.GetFeatureCount()                      # Roads-INFO#4: count number of road features

    # Create multiline geometry with all roads of a country
    multiline = ogr.Geometry(ogr.wkbMultiLineString)    # multiline to store all roads of a country
    line = roads_lyr.GetNextFeature()                   # loop through features
    while line:                                         # create multiline feature
        #roads_km_list.append(line.GetField('LENGTH_KM'))# ALTERNATIVE roads_km: roads_km for all road features in a country
        line_geom = line.GetGeometryRef()               # get geometry of line
        multiline.AddGeometry(line_geom)                # add line geometry to multiline (roads per country)
        line = roads_lyr.GetNextFeature()               # loop through features

    # Create intersection geometry of all roads in a country and the country border (border-crossing roads are cut off)
    road_intersection_trans = osr.CoordinateTransformation(roads_sr, countries_sr)  # length needs a projected coordinate system obtain units!!! -> countries_sr
    # multipolygon = TransformGeometry(multipolygon, countries_sr)                  # doesn't work because geometry not attached
    # multiline = TransformGeometry(multiline, countries_sr)                        # doesn't work because geometry not attached
    multipolygon.Transform(road_intersection_trans)                                 # apply transformation
    multiline.Transform(road_intersection_trans)                                    # apply transformation
    road_intersection = multiline.Intersection(multipolygon)                        # intersect multiline (roads) with multipolygon (country)
    roads_km = round(road_intersection.Length()/1000,3)                             # Roads-INFO#1: actual length of roads rounded, countries_sr in m -> convert to km

    # Create grid of points across the country to find mean and max distance to nearest road
    country_extent = multipolygon.GetEnvelope()
    x,y,x_stop,y_stop = country_extent[0],country_extent[2],country_extent[1],country_extent[3]
    multipoint = ogr.Geometry(ogr.wkbMultiPoint)  # create point class object MultiPoint -> multipoint grid
    while x <= x_stop or y <= y_stop:
        # create a geometry from coordinates
        point = ogr.Geometry(ogr.wkbPoint)  # create point class object Point
        point.AddPoint(x, y)                # add point coordinate
        multipoint.AddGeometry(point)       # add point to multipoint grid
        x += 100                            # next coordinates 100m east of the previous
        y += 100                            # next coordinates 100m north of the previous
    # Reduce multipoint grid covering country extent to country geometry (border outline)
    grid_intersection = multipoint.Intersection(multipolygon)
    # Get distances from each grid point to the closest road (multiline segment)
    dist_list = []
    for point in grid_intersection:
        dist = point.Distance(multiline)
        dist_list.append(dist)
    road_dist_km = round(mean(dist_list)/1000,3)    # Roads-INFO#2
    max_road_dist = round(max(dist_list)/1000,3)    # Roads-INFO#3

    print("Country : ", country, "   Information extracted from ", nr_roads, " roads.")  # for tracking


    # AGGREGATE/CALCULATE RESULTS (some rounded to decimal places for readability)
    area_km2 = round(sum(area_km2_list),3)                                   # add up area_km2 values for all polygons of one country
    if nr_dams != 0:                                                # if there is dam(s) located in the country
        yr_old = min(dataset_dams['YEAR'])                              # Dams-INFO#2
        i_old = ((dataset_dams['YEAR']).index(yr_old))                  # get index of yr_old
        name_old = dataset_dams['DAM_NAME'][i_old]                      # Dams-INFO#3
        yr_young = max(dataset_dams['YEAR'])                            # Dams-INFO#4
        i_young = ((dataset_dams['YEAR']).index(yr_young))              # get index of yr_young
        name_young = dataset_dams['DAM_NAME'][i_young]                  # Dams-INFO#5
        av_reserv_km2 = mean(dataset_dams['AREA_SKM'])                  # Dams-INFO#6
        max_reserv_km2 = max(dataset_dams['AREA_SKM'])                  # Dams-INFO#7
        i_max = ((dataset_dams['AREA_SKM']).index(max_reserv_km2))      # get index of max_reserv_km2
        Name_max_reserv = dataset_dams['DAM_NAME'][i_max]               # Dams-INFO#8
        av_depth_reserv_m = round(mean(dataset_dams['DEPTH_M']),2)      # Dams-INFO#9
        max_depth_reserv_m = max(dataset_dams['DEPTH_M'])               # Dams-INFO#10
        i_max_d = ((dataset_dams['DEPTH_M']).index(max_depth_reserv_m)) # get index of max_depth_reserv_m
        Name_max_depth = dataset_dams['DAM_NAME'][i_max_d]              # Dams-INFO#11
        max_catch_km2 = max(dataset_dams['CATCH_SKM'])                  # Dams-INFO#12
        i_max_c = ((dataset_dams['CATCH_SKM']).index(max_catch_km2))    # get index of max_catch_km2
        Name_max_catch = dataset_dams['DAM_NAME'][i_max_c]              # Dams-INFO#13
    else:
        yr_old=yr_young=name_young=av_reserv_km2=max_reserv_km2=Name_max_reserv=av_depth_reserv_m=max_depth_reserv_m=Name_max_reserv_m=max_catch_km2=Name_max_catch="--"
    #roads_km = sum(roads_km_list)                                   # ALTERNATIVE roads_km: roads_km for all road features in a country


    # STORE RESULTS
    dataset['country'].append(country)
    dataset['area_km2'].append(area_km2)
    dataset['nr_dams'].append(nr_dams)
    dataset['yr_old'].append(yr_old)
    dataset['name_old'].append(name_old)
    dataset['yr_young'].append(yr_young)
    dataset['name_young'].append(name_young)
    dataset['av_reserv_km2'].append(av_reserv_km2)
    dataset['max_reserv_km2'].append(max_reserv_km2)
    dataset['Name_max_reserv'].append(Name_max_reserv)
    dataset['av_depth_reserv_m'].append(av_depth_reserv_m)
    dataset['max_depth_reserv_m'].append(max_depth_reserv_m)
    dataset['Name_max_depth'].append(Name_max_depth)
    dataset['max_catch_km2'].append(max_catch_km2)
    dataset['Name_max_catch'].append(Name_max_catch)
    dataset['roads_km'].append(roads_km)
    dataset['road_dist_km'].append(road_dist_km)
    dataset['max_road_dist'].append(max_road_dist)
    dataset['nr_roads'].append(nr_roads)

    print("Country : ", country, "   Information storage completed!\n")  # for tracking
print(dataset)

# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #

print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")