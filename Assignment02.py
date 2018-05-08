# ####################################### LOAD REQUIRED LIBRARIES ############################################# #

import time
import gdal
import os
import re

# ####################################### SET TIME-COUNT ###################################################### #

starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")

# ####################################### FOLDER PATHS & global variables ##################################### #

root_folder = "D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 4 - Raster processing I/Assignment02_data/"

# ####################################### PROCESSING ########################################################## #

file_list = os.listdir(root_folder)
#print(file_list)

#(a) calculate the corner coordinates for each of the raster files
print("\nAssignment02 a)\n")

#GetCoordinates --> get coordinates for multiple tif files
    # input: list of input files --> file_list
    # UL --> Upper Left corner
    # LR --> Lower Right corner
def GetCoordinates(file_list):
    for file in file_list:
        ds = gdal.Open(root_folder + file, gdal.GA_ReadOnly)
        gt = ds.GetGeoTransform()  # UL_x, x-coordinate spatial resolution, UL_y, # y-coord. spat.res.
        # Upper left
        UL_x, UL_y = gt[0], gt[3]
        # Lower right
        LR_x = UL_x + (gt[1] * ds.RasterXSize)
        LR_y = UL_y + (gt[5] * ds.RasterYSize)
        print("Coordinates of " + file + ": " + "(" + str(UL_x) + "," + str(UL_y) + ") and (" + str(LR_x) + "," + str(LR_y) + ")")

GetCoordinates(file_list)



#(b) find the overlapping area across all raster files
print("\nAssignment02 b)\n")

#GetIntersectCoordinates --> get coordinates of the largest common extent of multiple tif files
    # input: list of input files --> file_list
    # UL --> Upper Left corner
    # LR --> Lower Right corner
def GetIntersectCoordinates(file_list):
    UL_x_list = []
    UL_y_list = []
    LR_x_list = []
    LR_y_list = []
    for file in file_list:
        ds = gdal.Open(root_folder + file, gdal.GA_ReadOnly)
        gt = ds.GetGeoTransform()  # UL_x, x-coordinate spatial resolution, UL_y, # y-coord. spat.res.
        # Upper left
        UL_x, UL_y = gt[0], gt[3]
        UL_x_list.append(UL_x)
        UL_y_list.append(UL_y)
        # Lower right
        LR_x = UL_x + (gt[1] * ds.RasterXSize)
        LR_y = UL_y + (gt[5] * ds.RasterYSize)
        LR_x_list.append(LR_x)
        LR_y_list.append(LR_y)
    UL_x_ext = max(UL_x_list)
    UL_y_ext = min(UL_y_list)
    LR_x_ext = min(LR_x_list)
    LR_y_ext = max(LR_y_list)
    LL_x_ext = UL_x_ext
    LL_y_ext = LR_y_ext
    UR_x_ext = LR_x_ext
    UR_y_ext = UL_y_ext
    print("The coordinates of the largest common extent are as follows:\n Upper left corner: (" + str(UL_x_ext) + "," + str(
        UL_y_ext) + ")\n Upper right corner: (" + str(UR_x_ext) + "," + str(UR_y_ext) + ")\n Lower left corner: (" + str(
        LL_x_ext) + "," + str(LL_y_ext) + ")\n Lower right corner: (" + str(LR_x_ext) + "," + str(LR_y_ext) + ")")

GetIntersectCoordinates(file_list)

# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #

print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")