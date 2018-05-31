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
from osgeo import gdal
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

wd = "D:/UNI/Python/Assignment05/data/"

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
    while len(pnt_list) < 3: #50, 3 as a test
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


# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #

print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")