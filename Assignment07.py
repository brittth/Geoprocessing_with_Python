# ####################################### LOAD REQUIRED LIBRARIES ############################################# #

import time
import os
import gdal
import geopandas as gpd
from osgeo import ogr
import struct

# ####################################### SET TIME-COUNT ###################################################### #

starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")

# ####################################### FOLDER PATHS & global variables ##################################### #

wd = "D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 9 - Real-world problems II/Assignment07_data/"
pts = wd + 'Points.shp'
og = wd + 'Old_Growth.shp'
prl = wd + 'PrivateLands.shp'
el = wd + 'Elevation.tif'
dist = wd + 'DistToRoad.tif'

# ####################################### FUNCTIONS ########################################################## #

def reprojectSHP2Lambert(file_path, outfile_name):
    ds = gpd.read_file(file_path)
    ds_lambert = ds.to_crs({'init': 'EPSG:3035'})
    ds_lambert.to_file(wd + outfile_name)
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds_pr = driver.Open(wd + outfile_name, 0)
    ds_pr = ds_pr.GetLayer()
    return ds_pr

def reprojectSHP2WGS84(file_path, outfile_name):
    ds = gpd.read_file(file_path)
    ds_lambert = ds.to_crs({'init': 'EPSG:4326'})
    ds_lambert.to_file(wd + outfile_name)
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds_pr = driver.Open(wd + outfile_name, 0)
    ds_pr = ds_pr.GetLayer()
    return ds_pr

# ####################################### PROCESSING ########################################################## #

driver = ogr.GetDriverByName('ESRI Shapefile')
points = driver.Open(pts)
pts_ly = points.GetLayer()


#extract values from points
feat = pts_ly.GetNextFeature()
while feat:
    print(feat.GetField('Id'))
    #reproject feature
    ds = gpd.read_file(file_path)
    ds_lambert = ds.to_crs({'init': 'EPSG:4326'})
    ds_lambert.to_file(wd + outfile_name)
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds_pr = driver.Open(wd + outfile_name, 0)
    #contained in PrivateLands
        #loop through prl
    for section in prl:
        #print object id
        prl_id = prl.GetField('OBJECTID')
        print(prl_id)
        #get extent of prl
        geom = prl.GetGeometryRef()
        prl_ext = geom.GetEnvelope()
        #check if point within borders of PA (not extent)
        #pts_ly = ogr.Geometry(ogr.wkbPoint)
        if geom.Contains(pts_ly):
            print('1')
        else:
            print('0')

    #contained in Old_Growth
    #extract Elevation
    #extract DistToRoad


    feat = pts_ly.GetNextFeature()
pts_ly.ResetReading()

####
'''
src_filename = wd + 'DistToRoad.tif'
shp_filename = wd + 'Points_pr.shp'

src_ds=gdal.Open(src_filename)
gt=src_ds.GetGeoTransform()
rb=src_ds.GetRasterBand(1)

ds=ogr.Open(shp_filename)
lyr=ds.GetLayer()
for feat in lyr:
    geom = feat.GetGeometryRef()
    mx,my=geom.GetX(), geom.GetY()  #coord in map units

    #Convert from map to pixel coordinates.
    #Only works for geotransforms with no rotation.
    px = int((mx - gt[0]) / gt[1]) #x pixel
    py = int((my - gt[3]) / gt[5]) #y pixel

    structval=rb.ReadRaster(px,py,1,1,buf_type=gdal.GDT_UInt16) #Assumes 16 bit int aka 'short'
    intval = struct.unpack('h' , structval) #use the 'short' format code (2 bytes) not int (4 bytes)

    print (intval[0]) #intval is a tuple, length=1 as we only asked for 1 pixel value
'''
# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #

print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")

'''#reproject shapefiles to Lambert
pts_l = reprojectSHP2Lambert(pts, 'Points_lam.shp')
og_l  = reprojectSHP2Lambert(og, 'Old_Growth_lam.shp')
prl_l = reprojectSHP2Lambert(prl, 'PrivateLands_lam.shp')

#reproject shapefiles to WGS84
pts_w = reprojectSHP2Lambert(pts, 'Points_wgs.shp')
og_w  = reprojectSHP2Lambert(og, 'Old_Growth_wgs.shp')
prl_w = reprojectSHP2Lambert(prl, 'PrivateLands_wgs.shp')'''