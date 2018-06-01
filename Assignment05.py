#Group I: Random Sampling
    #1) Get one PA
    #2) transform to EPSG 3035
    #3) Get extent of PA
    #4) Random Point within extent based on starting point (multitude of 30m)
    #5) Check if point within borders of PA (not extent)
    #6) Check if point has min x meters distance to nearest border
    #7) Check if x-coord. >= 90m
    #       else check if |y-coord| >= 90m
    #   --> both false, start again
    #   --> one TRUE save list1
    # while loop stopping at 50 entries

#Group II: Building the pixels
    # 9 Boxes by adding ad subtracting from given center points
    # add ID field for each 9 pixels and for each 9-pixel-box

#Group III: Coordinate system and shapefiles
    # EPSG 3035 because it is in meters


# ####################################### LOAD REQUIRED LIBRARIES ############################################# #

import time
import geopandas as gpd
from osgeo import ogr
from osgeo import osr
from osgeo import gdal
import random
import numpy as np
from shapely import wkt
import pandas as pd

# ####################################### SET TIME-COUNT ###################################################### #

starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")

# ####################################### FOLDER PATHS & global variables ##################################### #

wd = "D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 7 - Vector processing II/Assignment05 - data/"

# ####################################### PROCESSING ########################################################## #

pareas = gpd.read_file(wd+'WDPA_May2018_polygons_GER_select10large.shp')
pareas_lambert = pareas.to_crs({'init': 'EPSG:3035'})
pareas_lambert.to_file(wd+"wdpa_reproj.shp")

expoint = gpd.read_file(wd+'OnePoint.shp')
expoint = expoint.to_crs({'init': 'EPSG:3035'})
expoint.to_file(wd+"onepoint_reproj.shp")

driver = ogr.GetDriverByName('ESRI Shapefile')
dataSourcePoint = driver.Open(wd+"onepoint_reproj.shp", 0)
ExPoint = dataSourcePoint.GetLayer()
ExPointCoord = (ExPoint.GetExtent())
x_ori = ExPointCoord[0]
y_ori = ExPointCoord[2]

# open reprojected PA shp
dataSourcePA = driver.Open(wd+'wdpa_reproj.shp', 0)
pas = dataSourcePA.GetLayer()

# data frame preparation
ID = 0
pnt_df = pd.DataFrame(columns=["ID", "PA_NAME", "X_COORD", "Y_COORD"])

# loop through PAs
for pa in pas:
    # 1) get pa
    pa_name = pa.GetField('NAME')
    print(pa_name)

    # 2) get extent of pa
    geom = pa.GetGeometryRef()
    pa_ext = geom.GetEnvelope()

    # 3) create random points a multitude of 30m away from starting point
    x_min, x_max, y_min, y_max = pa_ext
    pnt_list = []
    while len(pnt_list) < 50: #50, 3 as a test
        # find range of x coords to draw random number
        seq_x_min = x_ori + (int((x_min - x_ori) / 30)) * 30
        seq_x_max = x_ori + (int((x_max - x_ori) / 30)) * 30
        x_random = random.choice(np.arange(seq_x_min, seq_x_max, 30))  # generate random x coordinate

        # find range of y coords to draw random number
        seq_y_min = y_ori + (int((y_min - y_ori) / 30)) * 30
        seq_y_max = y_ori + (int((y_max - y_ori) / 30)) * 30
        y_random = random.choice(np.arange(seq_y_min, seq_y_max, 30))  # generate random y coordinate

        # 4) check if point within borders of PA (not extent) #works
        pnt = ogr.Geometry(ogr.wkbPoint)  # create point class object
        pnt.AddPoint(x_random, y_random)  # add point coordinate
        if geom.Contains(pnt):

            # 5) check if point is at least 64m from nearest boundary
            wkt_pa = wkt.loads(str(geom))
            wkt_pnt = wkt.loads(str(pnt))
            if wkt_pa.boundary.distance(wkt_pnt) >= 64:

                # 6a) check if point is at least 90m from all other points in x direction
                if all(abs(x-x_random) >= 90 for x in pnt_df["X_COORD"].tolist()) == True:
                    pnt_list.append(pnt)
                    pnt_df.loc[len(pnt_df)+1] = [ID, pa_name, x_random, y_random]
                    ID += 1
                    print("point meets all criteria (x)")

                # 6b) if 6a=False, check if point is at least 90m from all other points in y direction
                elif all(abs(y-y_random) >= 90 for y in pnt_df["Y_COORD"].tolist()) == True:
                    pnt_list.append(pnt)
                    pnt_df.loc[len(pnt_df)+1] = [ID, pa_name, x_random, y_random]
                    ID += 1
                    print("point meets all criteria (y)")
                else:
                    print("point overlap")
            else:
                print("point too close to PA boundary:", round(wkt_pa.boundary.distance(wkt_pnt), 2), "m")
        else:
            print("point not contained in PA")

    print(len(pnt_list), "points collected") #check if the while loop worked
    print("")

# write random point sample to txt file in the wd
pnt_df.to_csv(wd+"test.txt", index=None, sep=',', mode='a')


# ####################################### create shapefile and layer ################################## #

# .SHP
# create a shapefile for polygons
shapefile = driver.CreateDataSource(wd+'rnd_sample.shp')
# set spatial reference
spatialreference = ogr.osr.SpatialReference()
spatialreference.ImportFromEPSG(3035)
#create the layer
layer = shapefile.CreateLayer('rnd_sample', spatialreference, ogr.wkbPolygon)
layerDefinition = layer.GetLayerDefn()
# add attributes to layer
point_ID = ogr.FieldDefn('point_ID', ogr.OFTInteger)
polygon_ID = ogr.FieldDefn('polygon_ID', ogr.OFTInteger)
PA_name = ogr.FieldDefn('PA_name', ogr.OFTString)
layer.CreateField(point_ID)
layer.CreateField(polygon_ID)
layer.CreateField(PA_name)

# .KML
kml_driver = ogr.GetDriverByName('KML')
kml_file = kml_driver.CreateDataSource(wd + 'kml_rnd_sample.kml')
sr_kml = ogr.osr.SpatialReference()
sr_kml.ImportFromEPSG(3035)
kml_layer = kml_file.CreateLayer('kml_rnd_sample', sr_kml, ogr.wkbPolygon)
kml_layerDefinitions = kml_layer.GetLayerDefn()
kml_layer.CreateField(point_ID)
kml_layer.CreateField(polygon_ID)
kml_layer.CreateField(PA_name)

# ####################################### define a function ################################## #

def GeometrytoFeature(n, m):
    polygon = ogr.Geometry(ogr.wkbPolygon) # create a polygon
    polygon.AddGeometry(ring) # add geometry to polygon

    # create SHP
    feature = ogr.Feature(layerDefinition) # greate a feature
    feature.SetGeometry(polygon) # put geometry into feature
    feature.SetField("point_ID", str(n)) # add attributes
    feature.SetField("polygon_ID", str((n*10)+m)) # add attributes
    feature.SetField("PA_name", pnt_df.iloc[n][1]) # add attributes
    layer.CreateFeature(feature) # put feature in layer

    # create KML
    kml_feature = ogr.Feature(kml_layerDefinitions)  # greate a feature
    kml_feature.SetGeometry(polygon)  # put geometry into feature
    kml_feature.SetField("point_ID", str(n))  # add attributes
    kml_feature.SetField("polygon_ID", str((n*10)+m))  # add attributes
    kml_feature.SetField("PA_name", pnt_df.iloc[n][1])  # add attributes
    kml_layer.CreateFeature(kml_feature)  # put feature in layer

# ####################################### create polygons ################################## #

for index, row in pnt_df.iterrows():
    pnt_ID = row["ID"]
    x_centre = row["X_COORD"]
    y_centre = row["Y_COORD"]
    # get the x-values and y-values
    x1 = x_centre-45
    x2 = x_centre-15
    x3 = x_centre+15
    x4 = x_centre+45
    y1 = y_centre-45
    y2 = y_centre-15
    y3 = y_centre+15
    y4 = y_centre+45
    # create the middle polygon
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(x2, y3)
    ring.AddPoint(x3, y3)
    ring.AddPoint(x3, y2)
    ring.AddPoint(x2, y2)
    ring.AddPoint(x2, y3)  # repeat first point to close polygon
    GeometrytoFeature(n=pnt_ID, m=1)
    # upper-left
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(x1, y4)
    ring.AddPoint(x2, y4)
    ring.AddPoint(x2, y3)
    ring.AddPoint(x1, y3)
    ring.AddPoint(x1, y4)
    GeometrytoFeature(n=pnt_ID, m=2)
    # upper-middle
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(x2, y4)
    ring.AddPoint(x3, y4)
    ring.AddPoint(x3, y3)
    ring.AddPoint(x2, y3)
    ring.AddPoint(x2, y4)
    GeometrytoFeature(n=pnt_ID, m=3)
    # upper-right
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(x3, y4)
    ring.AddPoint(x4, y4)
    ring.AddPoint(x4, y3)
    ring.AddPoint(x3, y3)
    ring.AddPoint(x3, y4)
    GeometrytoFeature(n=pnt_ID, m=4)
    # middle-left
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(x1, y3)
    ring.AddPoint(x2, y3)
    ring.AddPoint(x2, y2)
    ring.AddPoint(x1, y2)
    ring.AddPoint(x1, y3)
    GeometrytoFeature(n=pnt_ID, m=5)
    # middle-right
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(x3, y3)
    ring.AddPoint(x4, y3)
    ring.AddPoint(x4, y2)
    ring.AddPoint(x3, y2)
    ring.AddPoint(x3, y3)
    GeometrytoFeature(n=pnt_ID, m=6)
    # lower-left
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(x1, y2)
    ring.AddPoint(x2, y2)
    ring.AddPoint(x2, y1)
    ring.AddPoint(x1, y1)
    ring.AddPoint(x1, y2)
    GeometrytoFeature(n=pnt_ID, m=7)
    # lower-middle
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(x2, y2)
    ring.AddPoint(x3, y2)
    ring.AddPoint(x3, y1)
    ring.AddPoint(x2, y1)
    ring.AddPoint(x2, y2)
    GeometrytoFeature(n=pnt_ID, m=8)
    # lower-right
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(x3, y2)
    ring.AddPoint(x4, y2)
    ring.AddPoint(x4, y1)
    ring.AddPoint(x3, y1)
    ring.AddPoint(x3, y2)
    GeometrytoFeature(n=pnt_ID, m=9)

shapefile = None

# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #

print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")