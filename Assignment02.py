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

root_folder = "D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 4 - Raster processing I/"

# ####################################### PROCESSING ########################################################## #

ds = gdal.Open(root_folder + "LT05_L1TP_117056_20000717_20161214_01_T1_sr_evi.tif", gdal.GA_ReadOnly)

gt = ds.GetGeoTransform()
#pr = ds.GetProjection()
#cols = ds.RasterXSize
#rows = ds.RasterYSize
#print(cols,rows)

print(gt)
UL_x, UL_y = gt[0], gt[3]
# Upper left
print(UL_x, UL_y)
#Lower right
LR_x = UL_x + (gt[1]*ds.RasterXSize)
LR_y = UL_y + (gt[5]*ds.RasterYSize)
print(LR_x)
print(LR_y)
# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #

print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")