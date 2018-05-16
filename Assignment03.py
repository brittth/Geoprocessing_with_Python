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
root_folder = "D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 5 - Raster processing II/Assignment03 - data/"

DEM = "DEM_Humboldt_sub.tif"
SLOPE = "SLOPE_Humboldt_sub.tif"
THP = "THP_Humboldt_sub.tif"

# ####################################### FUNCTIONS ########################################################## #

# ####################################### PROCESSING ########################################################## #

#list files for whom the common extent is needed
file_list = os.listdir(root_folder)
#print(file_list)

#get the coordinates of the common extent (same as GetIntersectCoordinates, but not as a function as it needs to be tweaked)
gt_list = []
inv_gt_list = []
UL_x_list = []
UL_y_list = []
LR_x_list = []
LR_y_list = []

for file in file_list:
    ds = gdal.Open(root_folder + file, gdal.GA_ReadOnly)
    gt = ds.GetGeoTransform()  # UL_x, x-coordinate spatial resolution, UL_y, # y-coord. spat.res.
    gt_list.append(gt) #list of geotransform objects in lat/lon coordinates
    inv_gt = gdal.InvGeoTransform(gt) #transform geographic coordinates into array coordinates
    inv_gt_list.append(inv_gt)#list of geotransform objects in x/y cell coordinates
    print(file)
    #print(gt)
    print(inv_gt)
    # Upper left
    UL_x, UL_y = gt[0], gt[3] #calculate corner x/y cell coordinates (for lat/lon coordinates use gt)
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
#print("The coordinates of the largest common extent are as follows:\n Upper left corner: (" + str(UL_x_ext) + "," + str(
#    UL_y_ext) + ")\n Upper right corner: (" + str(UR_x_ext) + "," + str(UR_y_ext) + ")\n Lower left corner: (" + str(
#    LL_x_ext) + "," + str(LL_y_ext) + ")\n Lower right corner: (" + str(LR_x_ext) + "," + str(LR_y_ext) + ")")

overlap = [UL_x_ext, UL_y_ext, LR_x_ext, LR_y_ext] #only upper left and lower right coordinates
print(overlap)
# calculating extent with lat/lon/gt: [1399618.9749825108, 705060.6257949192, 1565979.932774514, 360674.0019850965]
# calculating extent with x/y/inv_gt: [1399618.9749825108, 2538.6444058538473, -5037.317506083792, 360674.0019850965]

#convert real-world coordinates (lat/lon) to image coordinates (x,y)
x1,y1 = gdal.ApplyGeoTransform(inv_gt, 1399619, 705061) #in die Funktion schreiben... ich check die zusammenhänge noch nicht!
x2,y2 = gdal.ApplyGeoTransform(inv_gt, 1565980, 360674)
minX = int(min(x1,x2))
maxX = int(max(x1,x2))
minY = int(min(y1,y2))
maxY = int(max(y1,y2))
x1off, y1off = map(int, x1,y1)
x1off, y1off = map(int, x2,y2)
#value_UL = band.ReadAsArray(x1off, y1off, 1, 1)[0,0] #what's band?
#value_LR = band.ReadAsArray(x2off, y2off, 1, 1)[0,0]

# calculate overlap extent - raster data has its origin on the lower left corner
extent_x = UR_x_ext - UL_x_ext
extent_y = UL_y_ext - LL_y_ext

print(extent_x)
print(extent_y)
'''
# Open Raster
ds = gdal.Open(root_folder + file)

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

# 0. Formulate an outputName
outfile = root_folder + "DEM_Humboldt_sub_copy.tif"
# 1. Create a driver with which we write the output
drvR = gdal.GetDriverByName ("GTiff")
# 2. Create the file (here: although exactly the same, we go through the syntax)
outDS = drvR.Create(outfile,cols,rows,nbands,dtype)
outDS.SetProjection(pr)
outDS.SetGeoTransform(gt)
# 3. Write the array into the newly generated file
outDS.GetRasterBand(1).WriteArray(arr,0,0) # array, offset_x, offset_y)
'''

# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #

print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")