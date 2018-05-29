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
import ogr
from shapely import geometry
import random

# ####################################### SET TIME-COUNT ###################################################### #

starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")

# ####################################### FOLDER PATHS & global variables ##################################### #

ger_path = 'D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 7 - Vector processing II/Assignment05 - data/gadm36_GERonly.shp'
pas_path = 'D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 7 - Vector processing II/Assignment05 - data/WDPA_May2018_polygons_GER_select10large.shp'
sp_path  = 'D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 7 - Vector processing II/Assignment05 - data/OnePoint.shp'

# ####################################### PROCESSING ########################################################## #

germany        = ogr.Open(ger_path)
protected      = ogr.Open(pas_path)
starting_point  = ogr.Open(sp_path)

ger = germany.GetLayer()
pas = protected.GetLayer()
sp  = starting_point.GetLayer()

# FUNCTION to create random points
'''
def generate_random(number, polygon):
    list_of_points = []
    minx, miny, maxx, maxy = polygon
    counter = 0
    while counter < number:
        pnt = geometry.Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if pnt in polygon: #originally: if polygon.contains(pnt):
            list_of_points.append(pnt)
            counter += 1
    return list_of_points
'''

# loop through PAs
for pa in pas:
    #1) get pa
    print(pa.GetField('NAME')) #works

    #2) TBC transform to EPSG 3035

    #3) get extent of pa
    geom = pa.GetGeometryRef()#works
    pa_ext = geom.GetEnvelope()#works

    #4) create random points a multitude of 30m away from starting point
    # rps = generate_random(1, pa_ext) #takes forever because of if statement, haven't waited for it to finish, but doesn't throw error either
    # print(rps)
        #works, function above only without if-statement, but doesn't check any of the restrictions
    minx, miny, maxx, maxy = pa_ext
    counter = 0
    pnt_list = []
    while counter < 50:
        pnt = geometry.Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        pnt_list.append(pnt)
        counter += 1
    print(len(pnt_list)) #check if the while loop worked
    print(pnt_list[1]) #check first point per PA
        # TBC make sure it's a multitude of 30m

    # The following needs to be included into the function above (generate_random):
    #5) check if point within borders of PA (not extent) #not checked yet
    #if rp in rps:
    #    return True
    #else:
    #    return False

    #6) check if point has min x meters distance to nearest border
        #find min distance to nearest border --> min_dist
        #min_dist < 60 (@Arne: Was it 60m?)

    # 7) Check if x-coord. >= 90m
    #       else check if |y-coord| >= 90m
    #   --> both false, start again
    #   --> one TRUE save list1
    # while loop stopping at 50 entries

# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #

print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")