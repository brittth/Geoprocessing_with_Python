# ####################################### LOAD REQUIRED LIBRARIES ############################################# #

import time
from osgeo import gdal, ogr, osr
import pandas as pd
from statistics import mean
import math as m

# https://github.com/brittth/Geoprocessing_with_Python/tree/master/BTheTools
from BTheTools import BTv

# ####################################### SET TIME-COUNT ###################################################### #

starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")

# ####################################### FUNCTIONS ########################################################### #

# see BTheTools package import
# no other functions needed (no repeating processes)

# ####################################### FOLDER PATHS & GLOBAL VARIABLES ##################################### #

rootFolder = "D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/MAP/Geoprocessing-in-python_MAP2018_data/Task02_data/"

# ####################################### PROCESSING ########################################################## #

# REMARKS
# Error handling
    # roads_km can be calculated using 2 approaches:
        #1) for all road features in a country
        #2) for all road segments within country borders, requires cutting off border-crossing roads outside borders
    # for higher accuracy approach 2 was used to calculate roads_km --> round(road_intersection.Length() / 1000, 3)
    # for countries with few/short roads, however, '.Length()' will throw an AttributeError
        # in these cases, approach 1 is used to calculate roads_km --> GetField('LENGTH_KM'),roads_km = sum(roads_km_list)
        #   no effect on accuracy, as it only concerns the Islands 'Guernsey' and 'Malta'
        #   where roads only leave country borders, where there are spatial inconsistencies between the two files
# Rounding
    # km data rounded to m level --> 3rd decimal place
    # m data rounded to cm level --> 2nd decimal place
# Grid
    # To calculate mean and max distance to road a 100x100 grid of 10000 points is calculated per country.
    # The spacing between the points, 99 in each direction, in calculated based on the country's area: sqrt(area)/99
    # This approach keeps the script's running time relatively low while preserving the accuracy of the results.


# LOAD DATA FILES
countries = ogr.Open(rootFolder + "ZonalShape_Countries_Europe_NUTS1_multipart.shp", 1)
countries_lyr = countries.GetLayer()
countries_sr = countries_lyr.GetSpatialRef() # native sr of multipolygon (country) & multipoint (grid per country)

dams = ogr.Open(rootFolder + "GRanD_dams_v1_1_Europe-sub.shp", 1)
dams_lyr = dams.GetLayer()
dams_sr = dams_lyr.GetSpatialRef()

roads = ogr.Open(rootFolder + "gRoads-v1-Europe-sub.shp", 1)
roads_lyr = roads.GetLayer()
roads_sr = roads_lyr.GetSpatialRef() # native sr of multiline (roads per country)

print("All files have been loaded!\n")


# CHECK SPATIAL REFERENCE
if str(countries_sr) == str(roads_sr) == str(dams_sr):
    print("All files share the same spatial reference. No transformation needed!\n")
else:
    print("NOT all files share the same spatial reference. Transformation needed!\n")


# PREPARE DATA FRAME FOR SUMMARY DATASET
dataset = pd.DataFrame(columns=['country','area_km2','nr_dams','yr_old','name_old','yr_young','name_young','av_reserv_km2',
        'max_reserv_km2','Name_max_reserv','av_depth_reserv_m','max_depth_reserv_m','Name_max_depth',
        'max_catch_km2','Name_max_catch','roads_km','road_dist_km','max_road_dist','nr_roads'])


# PREPARE COUNTRY LIST FOR DATA AGGREGATION
country_list = sorted(list(set([polygon.GetField('NAME_0') for polygon in countries_lyr]))) # 'sorted' facilitates testing
print("Country list: \n",country_list,"\n")
#country_list = [country_list[15], country_list[21],country_list[6],  country_list[38]]
country_list = country_list[15:16]
#print(country_list)


# EXTRACT INFORMATION
print("Extract information:")
for country in country_list:    # Countries-INFO#1
    # Prepare data storage
    polyID = 0          # for tracking
    area_km2_list = []
    roads_km_list = []  # for error handling: roads_km
    keys = ['DAM_NAME', 'YEAR', 'AREA_SKM', 'DEPTH_M', 'CATCH_SKM']
    values = [[], [], [], [], []]
    dataset_dams = dict(zip(keys, values))


    # Extract COUNTRY data
    # Create multipolygon representing country
    multipolygon = ogr.Geometry(ogr.wkbMultiPolygon)                # to store all polygons of a country
    countries_lyr.SetAttributeFilter("NAME_0 = '"+str(country)+"'") # filter for country
    polygon = countries_lyr.GetNextFeature()                        # loop through features
    while polygon:
        area_km2_list.append(polygon.GetField('area_km2'))          # Countries-INFO#2
        polygon_geom = polygon.GetGeometryRef()                     # get geometry of polygon
        multipolygon.AddGeometry(polygon_geom)                      # add polygon geometry to multipolygon (country)
        polyID += 1                                                 # for tracking
        polygon = countries_lyr.GetNextFeature()                    # loop through features
    multipolygon.AssignSpatialReference(countries_sr)               # assign native sr (otherwise only sr shadow)

    print("Country : ", country, "   Number of dissolved polygons: ", polyID,".")


    # Extract DAMS data per country (multipolygon)
    multipolygon_d = BTv.TransformGeometry(multipolygon, dams_sr)   # transform multipolygon geometry to sr of dams layer
    dams_lyr.SetSpatialFilter(multipolygon_d)                       # reduce dams to country geometry (multipolygon)
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
    multipolygon_r = BTv.TransformGeometry(multipolygon, roads_sr)  # transform multipolygon geometry to sr of roads layer
    roads_lyr.SetSpatialFilter(multipolygon_r)                      # reduce roads to country geometry (multipolygon)
    nr_roads = roads_lyr.GetFeatureCount()                          # Roads-INFO#4

    # Create multiline geometry representing all roads of the country
    multiline = ogr.Geometry(ogr.wkbMultiLineString)    # to store all line features of a country
    line = roads_lyr.GetNextFeature()                   # loop through features
    while line:
        roads_km_list.append(line.GetField('LENGTH_KM'))    # for error handling: roads_km
        line_geom = line.GetGeometryRef()                   # get geometry of line
        multiline.AddGeometry(line_geom)                    # add line geometry to multiline (roads per country)
        line = roads_lyr.GetNextFeature()                   # loop through features
    multiline.AssignSpatialReference(roads_sr)          # assign native sr (otherwise only sr shadow)

    # Cut off border-crossing roads at the country borders to get actual km of road per country (roads_km, approach 2)
    multiline_c = BTv.TransformGeometry(multiline, countries_sr)    # transform multiline to projected CS with units (here:m)
    road_intersection = multiline_c.Intersection(multipolygon)      # intersect multiline (roads) with multipolygon (country)
    try:
        roads_km = round(road_intersection.Length() / 1000, 3)      # Roads-INFO#1 : approach 2
    except AttributeError:
        roads_km = round(sum(roads_km_list),3)                      # Roads-INFO#1 : approach 1

    # Create grid of points across the country to find mean and max distance to nearest road

    # Find coordinates to start (x/y) and to stop (x/y_stop) building the grid
    country_extent = multipolygon.GetEnvelope()
    x, y, x_stop, y_stop = country_extent[0], country_extent[2], country_extent[1], country_extent[3]

    # Create multipoint grid within country extent
    multipoint = ogr.Geometry(ogr.wkbMultiPoint)    # to store the grid points
    x_list = []
    y_list = []
    area_km2 = round(sum(area_km2_list), 3)  # Countries-INFO#2
    while x <= x_stop:
        x_list.append(x)
        # if area_km2 <= 3000:
        #     x += 200    # next x coordinate 200m east of the previous
        # elif 3000 < area_km2 <= 50000:
        #     x += 4000   # next x coordinate 1km east of the previous
        # elif 50000 < area_km2 <= 200000:
        #     x += 6000   # next x coordinate 2km east of the previous
        # elif 200000 <area_km2 <= 400000:
        #     x += 8000
        # else:
        #     x += 10000
        #formula sqrt(area)/100
        x += ((m.sqrt(area_km2) / 9)*1000) # *1000 to convert from km to m
        #print((m.sqrt(area_km2) / 49)*1000)
    while y <= y_stop:
        y_list.append(y)
        # if area_km2 <= 3000:
        #     y += 200    # next y coordinate 200m north of the previous
        # elif 3000 < area_km2 <= 50000:
        #     y += 4000   # next x coordinate 1km north of the previous
        # elif 50000 < area_km2 <= 200000:
        #     y += 6000   # next x coordinate 2km north of the previous
        # elif 200000 <area_km2 <= 400000:
        #     y += 8000
        # else:
        #     y += 10000
        y += (m.sqrt(area_km2) / 9)
    point = ogr.Geometry(ogr.wkbPoint)              # create point class object Point
    for x_coord in x_list:
        for y_coord in y_list:
            point.AddPoint(x_coord, y_coord)    # add point coordinate
            multipoint.AddGeometry(point)       # add point to multipoint grid

    # Reduce multipoint grid covering country extent to country borders (country geometry)
    grid_intersection = multipoint.Intersection(multipolygon)

    # Get distances from each grid point to the closest road (multiline segment)
    dist_list = []
    for point in grid_intersection:
        dist = point.Distance(multiline_c)          # get shortest distance from point to roads
        dist_list.append(dist)                      # store distance in list
    road_dist_km = round(mean(dist_list) / 1000, 3) # Roads-INFO#2
    max_road_dist = round(max(dist_list) / 1000, 3) # Roads-INFO#3

    print("Country : ", country, "   Information extracted from ", nr_roads, " roads.")


    # AGGREGATE/CALCULATE RESULTS
    #area_km2 = round(sum(area_km2_list),3)  # Countries-INFO#2
    if nr_dams != 0:                        # if there is/are dam(s) located in the country
        yr_old = min(dataset_dams['YEAR'])                              # Dams-INFO#2
        i_old = ((dataset_dams['YEAR']).index(yr_old))                  # get index of yr_old
        name_old = dataset_dams['DAM_NAME'][i_old]                      # Dams-INFO#3
        yr_young = max(dataset_dams['YEAR'])                            # Dams-INFO#4
        i_young = ((dataset_dams['YEAR']).index(yr_young))              # get index of yr_young
        name_young = dataset_dams['DAM_NAME'][i_young]                  # Dams-INFO#5
        av_reserv_km2 = round(mean(dataset_dams['AREA_SKM']),3)         # Dams-INFO#6
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
        yr_old=name_old=yr_young=name_young=av_reserv_km2=max_reserv_km2=Name_max_reserv=av_depth_reserv_m=max_depth_reserv_m=Name_max_depth=max_catch_km2=Name_max_catch="-"


    # STORE RESULTS
    dataset.loc[len(dataset) + 1] = [country,area_km2,nr_dams,yr_old,name_old,yr_young,name_young,av_reserv_km2,max_reserv_km2,
                           Name_max_reserv,av_depth_reserv_m,max_depth_reserv_m,Name_max_depth,max_catch_km2,
                           Name_max_catch,roads_km,road_dist_km,max_road_dist,nr_roads]

    print("Country : ", country, "   Information storage completed!\n")

print("Summary dataset:\n",dataset)

# WRITE SUMMARY DATA FRAME TO CSV FILE
dataset.to_csv("THEMANN_BRITTA_MAP-task02_dataset.csv", index=None, sep=',')
print("\nThe summary dataset has been written to disc!\n")

# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #

print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")