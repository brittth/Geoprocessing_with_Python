# ####################################### LOAD REQUIRED LIBRARIES ############################################# #

import time
import os
import pandas as pd
from osgeo import gdal, ogr, osr
import struct
import pandas as pd
import numpy as np
import numpy.ma as ma
import math

# ####################################### SET TIME-COUNT ###################################################### #

starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")

# ####################################### FOLDER PATHS & global variables ##################################### #

baseFolder = "D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 10 - Real-world problems III/Assignment08_data/"

# ####################################### FUNCTIONS ########################################################## #

def TransformGeometry(geometry, target_sref):
    #Returns cloned geometry, which is transformed to target spatial reference
    geom_sref= geometry.GetSpatialReference()
    transform = osr.CoordinateTransformation(geom_sref, target_sref)
    geom_trans = geometry.Clone()
    geom_trans.Transform(transform)
    return geom_trans

def SpatialReferenceFromRaster(ds):
    #Returns SpatialReference from raster dataset
    pr = ds.GetProjection()
    sr = osr.SpatialReference()
    sr.ImportFromWkt(pr)
    return sr

def CopySHPDisk(layer, outpath):
    drvV = ogr.GetDriverByName('ESRI Shapefile')
    outSHP = drvV.CreateDataSource(outpath) #outpath
    lyr = layer # .GetLayer() #shape
    sett90LYR = outSHP.CopyLayer(lyr, 'lyr')
    del lyr, sett90LYR, outSHP

# ####################################### PROCESSING ########################################################## #

parcels = ogr.Open(baseFolder + "Parcels.shp", 1)
parcels_lyr = parcels.GetLayer()
parcels_cs = parcels_lyr.GetSpatialRef()

# Load data
# Marihuana
    # Get Projection infos
mary = ogr.Open(baseFolder + "Marihuana_Grows.shp")
mary_lyr = mary.GetLayer()
mary_cs = mary_lyr.GetSpatialRef()
# Roads
roads = ogr.Open(baseFolder + "Roads.shp", 1)
roads_lyr = roads.GetLayer()
# THP
thp = ogr.Open(baseFolder + "TimberHarvestPlan.shp", 1)
thp_lyr = thp.GetLayer()
# Public land
publ = ogr.Open(baseFolder + "PublicLands.shp", 1)
publ_lyr = thp.GetLayer()
# DEM (raster)
dem = gdal.Open(baseFolder + "DEM_Humboldt.tif")
gt = dem.GetGeoTransform()
pr = dem.GetProjection()
sr_raster = SpatialReferenceFromRaster(dem)

# Parcels
parcels_cs = parcels_lyr.GetSpatialRef()
feat = parcels_lyr.GetNextFeature()

# Create output dataframe
out_df = pd.DataFrame(columns=["Parcel APN", "NR_GH-Plants", "NR_OD-Plants", "Dist_to_grow_m", "Km Priv. Road", "Km Local Road", "Mean elevation", "PublicLand_YN", "Prop_in_THP"])

while feat:
    geom = feat.GetGeometryRef()
    apn = feat.GetField('APN')

    # COL 1: Parcel APN column
    print('Parcel APN: ', apn)

    ######### Group 1: Count number of greenhouse and outdoor growths per parcel ############
    # Reprojection
    geom_par = feat.geometry().Clone()
    geom_par.Transform(osr.CoordinateTransformation(parcels_cs, mary_cs))

    # Set spatial filter to parcel
    mary_lyr.SetSpatialFilter(geom_par)

    # Set number of total number of greenhouse and outdoor growths to zero
    total_gh = total_od = 0

    # Count the occurrences of greenhouse (g_plants) and outdoor (o_plants) growths in the parcel
    point_feat = mary_lyr.GetNextFeature()
    while point_feat:
        total_gh += point_feat.GetField('g_plants')
        total_od += point_feat.GetField('o_plants')
        point_feat = mary_lyr.GetNextFeature()
    mary_lyr.ResetReading()

    # COL 2: Nr_GH-Plants
    print('Nr_GH-Plants: ', total_gh)

    # COL 3: Nr_GH-Plants
    print('Nr_OD-Plants: ', total_od)


    ######### Group 2: Find distance from parcel border to next growth ############
    # Set spatial filter to parcel
    mary_lyr.SetSpatialFilter(geom_par)

    # Count plants in parcel (Filter!)
    feature_count = mary_lyr.GetFeatureCount()
    #print("APN: " + str(apn) + " Feature Count: " + str(feature_count))

    # If plant exists in parcel, go through buffer until another plant is found
    if feature_count > 0:
        mary_lyr.SetSpatialFilter(None)
        bufferSize = 0
        exit = 0
        while exit == 0:
            bufferSize = bufferSize + 10
            buffer = geom_par.Buffer(bufferSize)
            mary_lyr.SetSpatialFilter(buffer)
            buffer_count = mary_lyr.GetFeatureCount()
            #print("Current buffer size: " + str(bufferSize) + " -- Current buffer count:" + str(buffer_count))
            if buffer_count > feature_count:
                exit += 1
                # Write distance/bufferSize into a list
                distance = bufferSize
                #print('BufferSize: ',bufferSize)
    # Append 0 if no plants are contained in the parcel
    else: distance = 0

    # Remove spatial filter
    mary_lyr.SetSpatialFilter(None)

    # COL 4: Dist_to_grow_m
    print('Dist_to_grow_m: ', distance)


    ######### Group 3: Calculate the total km for the two types of roads ('Local Roads', 'Private') & proportion of THP area in parcel ############
    # Set filter for relevant road types
    roads_lyr.SetAttributeFilter("FUNCTIONAL IN ('Local Roads', 'Private')")

    # Loop through two categories
    road_feat = roads_lyr.GetNextFeature()
    while road_feat:
        functional = road_feat.GetField('FUNCTIONAL')
        geom_roads = road_feat.GetGeometryRef()
        intersection = geom.Intersection(geom_roads)        # Calculate intersection of road types and individual parcel
        length = intersection.Length()
        # Get length of intersection
        if functional == 'Private':
            length_pr = length / 1000
            # COL 5: Km Priv. Road
            print('Km Priv. Road',length_pr)
        if functional == 'Local Roads':
            length_lr = length / 1000
            # COL 6: Km local Road
            print('Km local Road', length_lr)
        road_feat = roads_lyr.GetNextFeature()

    # Timber harvest plan --> only use one year (overlapping geometries)
    thp_lyr.SetAttributeFilter("THP_YEAR = '1999'")
    thp_lyr.SetSpatialFilter(geom)                  # Set filter for parcel
    thp_feat = thp_lyr.GetNextFeature()
    area_parcel = geom.GetArea()                    # Area of parcel
    thp_list = []

    # Loop through selected features
    while thp_feat:
        geom_thp = thp_feat.GetGeometryRef()
        intersect_thp = geom.Intersection(geom_thp) # Intersection of parcel and selected thp features
        area = intersect_thp.GetArea()              # Area of intersected thp feature
        thp_list.append(area)                       # Add area of thp feature to list
        thp_feat = thp_lyr.GetNextFeature()

    # Calculate proportion of THP area in parcel
    thp_sum = sum(thp_list)
    thp_prop = thp_sum/area_parcel
    #print('THP proportion: ',thp_prop,'\n')

    # COL 9: Prop_in_THP
    print('Prop_in_THP: ',thp_prop)


    ######### Group 4: Check for public land and get mean elevation of the parcel ############
    # Check for public land within parcel
    public = 0
    publ_lyr.SetSpatialFilter(geom)
    if publ_lyr.GetFeatureCount() >0:
        public = 1
        publ_lyr.SetSpatialFilter(None)

    # COL 8: PublicLand_YN
    print('PublicLand_YN: ', public)

    # Get mean elevation for parcel

    # Transform Coordinate System
    p_geom_trans = TransformGeometry(geom, sr_raster)
    # Get Coordinates of polygon envelope
    x_min, x_max, y_min, y_max = p_geom_trans.GetEnvelope()

    # Create dummy shapefile to story features geometry in (necessary for rasterizing)
    drv_mem = ogr.GetDriverByName('Memory')
    ds = drv_mem.CreateDataSource("")
    ds_lyr = ds.CreateLayer("", SpatialReferenceFromRaster(dem), ogr.wkbPolygon)
    featureDefn = ds_lyr.GetLayerDefn()
    out_feat = ogr.Feature(featureDefn)
    out_feat.SetGeometry(p_geom_trans)
    ds_lyr.CreateFeature(out_feat)
    out_feat = None
    # CopySHPDisk(ds_lyr, "tryout.shp") #If you wish to check the shp

    # Create the destination data source
    x_res = math.ceil((x_max - x_min) / gt[1])
    y_res = math.ceil((y_max - y_min) / gt[1])
    target_ds = gdal.GetDriverByName('MEM').Create('', x_res, y_res, gdal.GDT_Byte)
    target_ds.GetRasterBand(1).SetNoDataValue(-9999)
    target_ds.SetProjection(pr)
    target_ds.SetGeoTransform((x_min, gt[1], 0, y_max, 0, gt[5]))

    # Rasterization
    # to account for small overlaps of polygons in pixels
    gdal.RasterizeLayer(target_ds, [1], ds_lyr, burn_values=[1]) #options=['ALL_TOUCHED=TRUE']) --> this part was defect
    target_array = target_ds.ReadAsArray()
    # target_ds = None

    # Convert data from the DEM to the extent of the envelope of the polygon (to array)
    inv_gt = gdal.InvGeoTransform(gt)
    offsets_ul = gdal.ApplyGeoTransform(inv_gt, x_min, y_max)
    off_ul_x, off_ul_y = map(int, offsets_ul)
    raster_np = np.array(dem.GetRasterBand(1).ReadAsArray(off_ul_x, off_ul_y, x_res, y_res))

    # Calculate the mean of the array with masking
    test_array = np.ma.masked_where(target_array < 1, target_array)
    raster_masked = np.ma.masked_array(raster_np, test_array.mask)
    dem_mean = np.mean(raster_masked)

    # COL 7: Mean elevation
    print('Mean elevation: ', dem_mean,'\n')

    ##############################

    feat = parcels_lyr.GetNextFeature()
    # Prepare table
    out_df.loc[len(out_df) + 1] = [apn, total_gh, total_od, distance, length_pr, length_lr, dem_mean, public, thp_prop]

parcels_lyr.ResetReading()

# Write table to csv
out_df.to_csv("Assignment08_output.csv", index=None, sep=',', mode='a')

# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #

print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")