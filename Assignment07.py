# ####################################### LOAD REQUIRED LIBRARIES ############################################# #

import time
import os
import pandas as pd
from osgeo import gdal, ogr, osr
import struct

# ####################################### SET TIME-COUNT ###################################################### #

starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")

# ####################################### FOLDER PATHS & global variables ##################################### #

wd = "D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 9 - Real-world problems II/Assignment07_data/"
pts = wd + 'Points.shp'
ogro = wd + 'Old_Growth.shp'
prla = wd + 'PrivateLands.shp'
elev = wd + 'Elevation.tif'
distr = wd + 'DistToRoad.tif'

# ####################################### FUNCTIONS ########################################################## #

# ####################################### PROCESSING ########################################################## #

#Shapefiles
driver = ogr.GetDriverByName('ESRI Shapefile')
points = driver.Open(pts,1)
og = driver.Open(ogro, 1)
prl = driver.Open(prla,1)
pts_ly = points.GetLayer()
og_ly = og.GetLayer()
prl_ly = prl.GetLayer()

#Raster files
el = gdal.Open(elev)
dist = gdal.Open(distr)

source_SR = pts_ly.GetSpatialRef()         # get spatial reference from sample layer

#Elevation
pr_el = el.GetProjection()               # get projection from raster
target_SR_el = osr.SpatialReference()         # create empty spatial reference
target_SR_el.ImportFromWkt(pr_el)             # get spatial reference from projection of raster
coordTrans_el = osr.CoordinateTransformation(source_SR, target_SR_el)     # transformation rule for coordinates from samples to elevation raster

#DistToRoads
pr_dist = dist.GetProjection()           # get projection from raster
target_SR_dist = osr.SpatialReference()       # create empty spatial reference
target_SR_dist.ImportFromWkt(pr_dist)         # get spatial reference from projection of raster
coordTrans_dist = osr.CoordinateTransformation(source_SR, target_SR_dist) # transformation rule for coordinates from samples to roads raster

#OldGrowth
target_SR_og = og_ly.GetSpatialRef()         # create empty spatial reference
coordTrans_og = osr.CoordinateTransformation(source_SR, target_SR_og)     # transformation rule for coordinates from samples to shapefile

#PrivateLands
target_SR_prl = prl_ly.GetSpatialRef()       # create empty spatial reference
coordTrans_prl = osr.CoordinateTransformation(source_SR, target_SR_prl) # transformation rule for coordinates from samples to shapefile

#empty data frame list
df = []

#extract values from points
feat = pts_ly.GetNextFeature()
while feat:
    feat_id = feat.GetField('Id')
    print(feat_id)

    coord = feat.GetGeometryRef()

    # PrivateLands
    coord_cl = coord.Clone()
    coord_cl.Transform(coordTrans_prl)  # apply coordinate transformation
    prl_ly.SetSpatialFilter(coord_cl)
    count = prl_ly.GetFeatureCount()
    if count > 0:
        value_prl = 1
    else:
        value_prl = 0

    #OldGrowth
    coord_cl = coord.Clone()
    coord_cl.Transform(coordTrans_og)  # apply coordinate transformation
    og_ly.SetSpatialFilter(coord_cl)
    count = og_ly.GetFeatureCount()
    if count > 0:
        value_og = 1
    else:
        value_og = 0

    # Elevation
    coord_cl = coord.Clone()
    coord_cl.Transform(coordTrans_el)  # apply coordinate transformation
    gt_el = el.GetGeoTransform()  # get projection and transformation to calculate absolute raster coordinates
    x, y = coord_cl.GetX(), coord_cl.GetY()
    px_el = int((x - gt_el[0]) / gt_el[1])
    py_el = int((y - gt_el[3]) / gt_el[5])
    rb_el = el.GetRasterBand(1)
    print(rb_el.DataType)
    struc_var_el = rb_el.ReadRaster(px_el, py_el, 1, 1)
    print(struc_var_el)
    val_el = struct.unpack('H', struc_var_el)
    value_el = val_el[0]

    # DistToRoad
    coord_cl = coord.Clone()
    coord_cl.Transform(coordTrans_dist)  # apply coordinate transformation
    gt_dist = dist.GetGeoTransform()  # get projection and transformation to calculate absolute raster coordinates
    x, y = coord_cl.GetX(), coord_cl.GetY()
    px_dist = int((x - gt_dist[0]) / gt_dist[1])
    py_dist = int((y - gt_dist[3]) / gt_dist[5])
    rb_dist = dist.GetRasterBand(1)
    print(rb_dist.DataType)
    struc_var_dist = rb_dist.ReadRaster(px_dist, py_dist, 1, 1)
    print(struc_var_dist)
    val_dist = struct.unpack('f', struc_var_dist)
    value_dist = val_dist[0]

    #copy results into the df list
    df.append([feat_id,value_prl,value_og,value_el,value_dist])

    #go to next feature
    feat = pts_ly.GetNextFeature()
pts_ly.ResetReading()

#prepare table
col_names = ['Point ID','Private','OldGrowth','Elevation', 'Road_Dist'] #assign 'column' names to values
df = pd.DataFrame.from_records(df,columns = col_names)  #combines the col_names with its values
df = pd.melt(df, id_vars = ['Point ID'], value_vars=['Private','OldGrowth','Elevation', 'Road_Dist']) #change table orientation, column become rows
df = df.sort_values(by ='Point ID') #sort by Point ID
print(df)

#write csv to disc
df.to_csv(path_or_buf = 'output.csv', index = False)

# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #

print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")