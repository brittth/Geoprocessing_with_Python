# ####################################### LOAD REQUIRED LIBRARIES ############################################# #

import time
import os
from osgeo import gdal, ogr, osr
import pandas as pd
import numpy as np
import struct

# ####################################### SET TIME-COUNT ###################################################### #

starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")

# ####################################### FUNCTIONS ########################################################### #

def RasterOverlapToArray(file_list):
    array_list = []
    UL_x_list = []
    UL_y_list = []
    LR_x_list = []
    LR_y_list = []
    for file in file_list:
        ds = gdal.Open(root_folder + file, gdal.GA_ReadOnly)
        gt = ds.GetGeoTransform()  # UL_x, x-coordinate spatial resolution, UL_y, # y-coord. spat.res.
        # Upper left
        UL_x, UL_y = gt[0], gt[3] #calculate corner lat/lon coordinates (for x/y cell coordinates use inv_gt)
        UL_x_list.append(UL_x)
        UL_y_list.append(UL_y)
        # Lower right
        LR_x = UL_x + (gt[1] * ds.RasterXSize)
        LR_y = UL_y + (gt[5] * ds.RasterYSize)
        LR_x_list.append(LR_x)
        LR_y_list.append(LR_y)
    UL_x_ext = max(UL_x_list)#corner coordinates and extent of common extent
    UL_y_ext = min(UL_y_list)
    LR_x_ext = min(LR_x_list)
    LR_y_ext = max(LR_y_list)
    extent_x = int(round((min(LR_x_list) - max(UL_x_list))/gt[1])) #width of common extent/pixel width = number of columns
    extent_y = int(round(min(UL_y_list) - max(LR_y_list))/gt[1]) #height of common extent/pixel height = number of rows
    overlap = [UL_x_ext, UL_y_ext, LR_x_ext, LR_y_ext] #only upper left and lower right coordinates
    print("Common extent UL/LR coordinates: ",overlap)
    print("Common extent in x and y direction: ",extent_x, extent_y)
    spat_res = [gt[1], abs(gt[5])]
    print("Common extent spatial resolution: ", spat_res, "\n")
    for file in file_list:  #convert real-world coordinates (lat/lon) to image coordinates (x,y)
        print(file) #for overview in console
        ds = gdal.Open(root_folder + file, gdal.GA_ReadOnly)
        gt = ds.GetGeoTransform()  # UL_x, x-coordinate spatial resolution, UL_y, # y-coord. spat.res.
        inv_gt = gdal.InvGeoTransform(gt)  # transform geographic coordinates into array coordinates
        x1,y1 = gdal.ApplyGeoTransform(inv_gt, overlap[0], overlap[1])
        x2,y2 = gdal.ApplyGeoTransform(inv_gt, overlap[2], overlap[3])
        minX = int(round(min(x1,x2))) # x value for UL/origin
        minY = int(round(min(y1,y2))) # y value for UL/origin
        maxX = int(round(max(x1,x2))) # x value for LR
        maxY = int(round(max(y1,y2))) # y value for LR
        print("Cell coordinates of common extent: ", minX,maxX,minY,maxY) #cell coordinates of extent for each file
        x1off, y1off = map(int, [x1, y1]) #UL
        print("UL x offset: ", x1off)
        print("UL y offset: ", y1off,"\n")
        array_list.append(ds.ReadAsArray(x1off, y1off, extent_x, extent_y)) #Upper Left corner
    return array_list

# ####################################### FOLDER PATHS & global variables ##################################### #

root_folder = "D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 11 - Machine Learning/Assignment09_Data/"

im1 = "LE07_L1TP_117056_20040211_20170122_01_T1_sr_evi.tif"
im2 = "LE07_L1TP_117056_20130627_20161124_01_T1_sr_evi.tif"
im3 = "LT05_L1TP_117056_19980407_20161228_01_T1_sr_evi.tif"
im4 = "LT05_L1TP_117056_20000717_20161214_01_T1_sr_evi.tif"
pts = "RandomPoints.shp"

# ####################################### PROCESSING ########################################################## #

#raster file list as input for RasterOverlaptoArray function
file_list = [im1,im2,im3,im4]

#get raster overlap as array
array_list = RasterOverlapToArray(file_list)
print(array_list)

#prepare classifcation array
if array_list[0].shape == array_list[1].shape == array_list[2].shape == array_list[3].shape:
    print("The overlaps have identical shape!")
else:
    print("The overlap shapes do not match!")
arr_class = array_list[0]*0
print(arr_class)

#load point shapefile
driver = ogr.GetDriverByName("ESRI Shapefile")
pts = driver.Open(root_folder + pts,1)
pts_lyr = pts.GetLayer()

#get raster information for coordinate transformation
source_SR = pts_lyr.GetSpatialRef()     # get spatial reference from sample layer
ol = gdal.Open(root_folder + im1)       # open any raster (they all have the same projection
pr_ol = ol.GetProjection()              # get projection from raster
target_SR_ol = osr.SpatialReference()   # create empty spatial reference
target_SR_ol.ImportFromWkt(pr_ol)       # get spatial reference from projection of raster
coordTrans_ol = osr.CoordinateTransformation(source_SR, target_SR_ol)     # transformation rule for coordinates from samples to elevation raster

#extract values from points
feat = pts_lyr.GetNextFeature()
while feat:
    #to keep track
    feat_id = feat.GetField('Id')
    print("\n",feat_id)

    #get reference system
    coord = feat.GetGeometryRef()
    coord_cl = coord.Clone()
    coord_cl.Transform(coordTrans_ol)  # apply coordinate transformation
    x, y = coord_cl.GetX(), coord_cl.GetY()

    #for each raster file
    for raster in file_list:
        print(raster)
        ras = gdal.Open(root_folder + raster)
        gt_ol = ras.GetGeoTransform()  # get projection and transformation to calculate absolute raster coordinates
        px_ol = int((x - gt_ol[0]) / gt_ol[1])
        py_ol = int((y - gt_ol[3]) / gt_ol[5])
        rb_ol = ras.GetRasterBand(1)
        print(rb_ol.DataType)
        struc_var_ol = rb_ol.ReadRaster(px_ol, py_ol, 1, 1)
        print(struc_var_ol)
        if struc_var_ol is None:
            value_ol = struc_var_ol
        else:
            val_ol = struct.unpack('H', struc_var_ol)
            value_ol = val_ol[0]
    #go to next feature
    feat = pts_lyr.GetNextFeature()
pts_lyr.ResetReading()



# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #

print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")