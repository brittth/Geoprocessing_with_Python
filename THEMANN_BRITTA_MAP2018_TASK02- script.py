# ####################################### LOAD REQUIRED LIBRARIES ############################################# #

import time
import os
from osgeo import gdal, ogr, osr
import numpy as np
import struct

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

countries = "ZonalShape_Countries_Europe_NUTS1_multipart.shp"
roads = "gRoads-v1-Europe-sub.shp"
dams = "GRanD_dams_v1_1_Europe-sub.shp"

# ####################################### PROCESSING ########################################################## #

# LOAD DATA FILES
countries = ogr.Open(rootFolder + "ZonalShape_Countries_Europe_NUTS1_multipart.shp", 1)
countries_lyr = countries.GetLayer()
countries_sr = countries_lyr.GetSpatialRef()

roads = ogr.Open(rootFolder + "gRoads-v1-Europe-sub.shp", 1)
roads_lyr = roads.GetLayer()
roads_sr = roads_lyr.GetSpatialRef()

dams = ogr.Open(rootFolder + "GRanD_dams_v1_1_Europe-sub.shp", 1)
dams_lyr = dams.GetLayer()
dams_sr = dams_lyr.GetSpatialRef()

# CHECK SPATIAL REFERENCE
if str(countries_sr) == str(roads_sr) == str(dams_sr):  #only works with str in front
    print("All files share the same spatial reference. No transformation needed!\n")
else:
    print("NOT all files share the same spatial reference. Transformation needed!\n")

# TRANSFORMATION
    # transform point (dams) and line (roads) data since faster than transforming polygon (countries) data
    # set spatial reference of countries layer as target
#roads_new = TransformGeometry(roads, countries_sr)
#print(roads_new.GetSpatialRef())
#dams_new = TransformGeometry(dams, countries_sr)
#print(dams_new.GetSpatialRef())

# PREPARE DATA DICTIONARY FOR SUMMARY DATASET
keys = ['country','area_km2','nr_dams','yr_old','name_old','yr_young','name_young','av_reserv_km2',
        'max_reserv_km2','Name_max_reserv','av_depth_reserv_m','max_depth_reserv_m','Name_max_reserv',
        'max_catch_km2','Name_max_catch','roads_km','roads_dist_km','max_road_dist','nr_roads']
values = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
dataset = dict(zip(keys, values))
#print(dataset)

# PREPARE COUNTRY LIST FOR DATA AGGREGATION
polygons = []
for polygon in countries_lyr:
    polygons.append(polygon.GetField('Name_0'))
print(polygons)
countries = set(polygons)
print(countries)

#for polygon in countries_lyr:
#    print(polygon.GetField('Name_0'))
#    print(polygon.GetField('area_km2'))

#GEOPANDAS EXAMPLE
#world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
#world = world[['country', 'geometry']]
#continents = world.dissolve(by='Name_0')
#continents.plot();
#continents.head()
# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #

print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")