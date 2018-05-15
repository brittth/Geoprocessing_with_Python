# ####################################### LOAD REQUIRED LIBRARIES ############################################# #

import time
import os
import gdal

# ####################################### SET TIME-COUNT ###################################################### #

starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")

# ####################################### FOLDER PATHS & global variables ##################################### #
root_folder = "D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 5 - Raster processing II/"


# ####################################### PROCESSING ########################################################## #
# Open Raster
ds = gdal.open(root_folder + file)

# Get the basic properties of the raster file
gt = ds.GetGeoTransform()
pr = ds.GetProjection()
cols = ds.RasterXSize
rows = ds.RasterYSize
nbands = ds.RasterCount

# Get the raster values (from the entire raster)
rb = ds.GetRasterBand(1)
dtype = rb.DataType
arr = rb.ReadAsArray(0,0,cols,rows) # (origin_x, origin_y, sliceSize_x, SliceSize_y)


# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #

print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")