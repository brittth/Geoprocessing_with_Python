# ####################################### LOAD REQUIRED LIBRARIES ############################################# #

import time
import os
from osgeo import gdal, ogr, osr
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import struct
import random
import sys

# ####################################### SET TIME-COUNT ###################################################### #

starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")

# ####################################### FUNCTIONS ########################################################### #

#GetCoordinates --> get coordinates for multiple tif files
    # input: list of paths to input files --> file_path_list
    # UL --> Upper Left corner
    # LR --> Lower Right corner
def GetCoordinates(file_path_list):
    UL_x_list = []
    UL_y_list = []
    LR_x_list = []
    LR_y_list = []
    counter = 0
    for file_path in file_path_list:
        ds = gdal.Open(file_path, gdal.GA_ReadOnly)
        gt = ds.GetGeoTransform()  # UL_x, x-coordinate spatial resolution, UL_y, # y-coord. spat.res.
        # Upper left
        UL_x, UL_y = gt[0], gt[3]
        # Lower right
        LR_x = UL_x + (gt[1] * ds.RasterXSize)
        LR_y = UL_y + (gt[5] * ds.RasterYSize)
        UL_x_list.append(UL_x)
        UL_y_list.append(UL_y)
        LR_x_list.append(LR_x)
        LR_y_list.append(LR_y)
        #print("Coordinates of raster #" + str(counter) + ": " + "(" + str(UL_x) + "," + str(UL_y) + ") and (" + str(LR_x) + "," + str(LR_y) + ")")
        counter += 1
    return UL_x_list, UL_y_list, LR_x_list, LR_y_list

# ####################################### FOLDER PATHS & GLOBAL VARIABLES ##################################### #

rootFolder = "D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/MAP/Geoprocessing-in-python_MAP2018_data/Task01_data/"

L8_doy = rootFolder + "2015_L8_doy015/"
L8_met = rootFolder + "2015_L8_metrics/"
S1_met_VH = rootFolder + "2015_S1_metrics/VH_mean/"
S1_met_VV = rootFolder + "2015_S1_metrics/VV_mean/"

path_VCF = rootFolder + "2000_VCF/20S_070W.tif"

# ####################################### PROCESSING ########################################################## #

# IDENTIFY EXTENT OF THE AREA COVERED BY THE 4 TILE
# write the file names containing ".bsq" or "tif" of each tile into a file path list
folder_list = [L8_doy, L8_met,S1_met_VH,S1_met_VV]
file_path_list_tiles = []
for folder in folder_list:
    file_list = os.listdir(folder)
    for file in file_list:
        file_path = folder + file
        file_path_list_tiles.append(file_path)
#print("All files in folder: \n",file_path_list_tiles,"\n")
file_path_list_bsq_tif = []
for file in file_path_list_tiles:
    if "bsq" in file:
        file_path_list_bsq_tif.append(file)
    if "tif" in file:
        file_path_list_bsq_tif.append(file)
#print("Only bsq files in folder: \n",file_path_list_bsq_tif,"\n")

# identify UL and LR corner coordinates of the area covered by the 4 tiles
#print("\nExtracting corner coordinates of the 4 tiles:")
UL_x_list, UL_y_list, LR_x_list, LR_y_list = GetCoordinates(file_path_list_bsq_tif)
UL_x = min(UL_x_list)
UL_y = max(UL_y_list)
LR_x = max(LR_x_list)
LR_y = min(LR_y_list)
print("\nCorner coordinates of the area covered by the 4 tiles: \n UL(",UL_x,",",UL_y,") and LR(",LR_x,",",LR_y,")")


# LOAD RASTER AND GET TRANSFORMATION RULES
# VCF raster
vcf = gdal.Open(path_VCF)           # read VFC raster
vcf_pr = vcf.GetProjection()        # get projection from raster
target_SR = osr.SpatialReference()  # create empty spatial reference
target_SR.ImportFromWkt(vcf_pr)     # get spatial reference from projection of raster
#print("\nSpatial Reference of the VFC raster file: \n",target_SR)

# get transformation rule for tiles to VFC target spatial reference
ras = gdal.Open(file_path_list_bsq_tif[0])  # read tile raster (first in list selected)
ras_pr = ras.GetProjection()                # get projection from raster
source_SR = osr.SpatialReference()          # create empty spatial reference
source_SR.ImportFromWkt(ras_pr)             # get spatial reference from projection of raster
coordTrans = osr.CoordinateTransformation(source_SR, target_SR)# transformation rule for coordinates from tile raster to VFC raster


# PREPARATION FOR POINT EXTRACTION
# point id (each point) and unique point id (only stored point)
ID = 0
UID = 0
# random points data frame preparation
pnt_df = pd.DataFrame(columns=["UID", "X_COORD", "Y_COORD", "VCF"]) # FOR TESTING ADD: , "stratum"])
# create lists to store point information in
pnt_list = []   # all stored points
c0020 = []      # 0-20% stratum
c2140 = []      # 21-40% stratum
c4160 = []      # 41-60% stratum
c6180 = []      # 61-80% stratum
c80100 = []     # 81-100% stratum
feature_matrix = [] # x
target_vector = []  # y


# RANDOM POINT GENERATION AND STORAGE
while len(c0020) < 100 or len(c2140) < 100 or len(c4160) < 100 or len(c6180) < 100 or len(c80100) < 100:
    # generate random points
    x_random = random.choice(np.arange(UL_x, LR_x, 30)) # generate random x coordinate from range of x values
    y_random = random.choice(np.arange(LR_y, UL_y, 30)) # generate random y coordinate from range of y values

    # create a geometry from coordinates
    pnt = ogr.Geometry(ogr.wkbPoint)  # create point class object Point
    pnt.AddPoint(x_random, y_random)  # add point coordinate

    # extract band values of all tile rasters at Point locations
    tileBand_values = []                        # prepare list for tile band values per point
    tileBand_values_inner = []                  # prepare list for tile band values per raster
    for tile_ras in file_path_list_bsq_tif:     # go through all tile rasters
        print("raster ", tile_ras)
        ras = gdal.Open(tile_ras)               # read tile raster
        tile_gt = ras.GetGeoTransform()         # get projection and transformation
        tile_px = int((x_random - tile_gt[0]) / tile_gt[1]) # calculate absolute raster coordinates
        tile_py = int((y_random - tile_gt[3]) / tile_gt[5]) # calculate absolute raster coordinates
        rb_count = ras.RasterCount              # get number of raster bands in raster
        # extract value for band
        for i in (range(1,rb_count)):
            rb = ras.GetRasterBand(i)
            struc_tile_var = rb.ReadRaster(tile_px, tile_py, 1, 1)
            if struc_tile_var is None:
                tile_value = struc_tile_var
            else:
                tile_val = struct.unpack('H', struc_tile_var)
                tile_value = tile_val[0]
            # store band value in list
            print(tile_value)
            tileBand_values_inner.append(tile_value)
        tileBand_values.append(tileBand_values_inner)

    # assign spatial reference system from VFC raster to Point geometry
    coord_cl = pnt.Clone()                      # clone sample geometry
    coord_cl.Transform(coordTrans)              # apply coordinate transformation
    x, y = coord_cl.GetX(), coord_cl.GetY()     # get x and y coordinates of transformed sample point
    #print("\nRandom Point #",ID,":")
    #print("Coordinates :", x_random, y_random)
    #print("Transformed coordinates :", x, y)

    # extract value from point
    vcf_gt = vcf.GetGeoTransform()              # get projection and transformation
    vcf_px = int((x - vcf_gt[0]) / vcf_gt[1])   # calculate absolute raster coordinates
    vcf_py = int((y - vcf_gt[3]) / vcf_gt[5])   # calculate absolute raster coordinates
    vcf_rb = vcf.GetRasterBand(1)               # get raster band
    struc_vcf_var = vcf_rb.ReadRaster(vcf_px, vcf_py, 1, 1) # extract information
    if struc_vcf_var is None:                   # decode information
        vcf_value = struc_vcf_var
    else:
        vcf_val = struct.unpack('b', struc_vcf_var) # [b=signed char]
        vcf_value = vcf_val[0]

    print("\nRandom Point #", ID) # console output to keep track

    # write points into point list if the respective stratum is not complete yet
    if vcf_value <= 20 and len(c0020) < 100:    # 0-20% stratum
        c0020.append(vcf_value)                 # assign point to stratum
        #stratum = 1                            # FOR TESTING: give class number for preview in dataframe
        pnt_list.append(pnt)                    # append point to point list
        feature_matrix.append(tileBand_values)  # append tile band values to feature matrix list
        target_vector.append(vcf_value)         # append vcf value to target vector list
        pnt_df.loc[len(pnt_df) + 1] = [UID, x, y, vcf_value] # prepare data frame for shapefile # FOR TESTING ADD: , stratum])
        UID += 1                            # count up unique ID only when point has been added
    elif vcf_value <= 40 and len(c2140) < 100: # 21-40% stratum
        c2140.append(vcf_value)
        #stratum = 2
        pnt_list.append(pnt)
        feature_matrix.append(tileBand_values)
        target_vector.append(vcf_value)
        pnt_df.loc[len(pnt_df) + 1] = [UID, x, y, vcf_value] # FOR TESTING ADD: , stratum])
        UID += 1
    elif vcf_value <= 60 and len(c4160) < 100: # 41-60% stratum
        c4160.append(vcf_value)
        #stratum = 3
        pnt_list.append(pnt)
        feature_matrix.append(tileBand_values)
        target_vector.append(vcf_value)
        pnt_df.loc[len(pnt_df) + 1] = [UID, x, y, vcf_value] # FOR TESTING ADD: , stratum])
        UID += 1
    elif vcf_value <= 80 and len(c6180) < 100: # 61-80% stratum
        c6180.append(vcf_value)
        #stratum = 4
        pnt_list.append(pnt)
        feature_matrix.append(tileBand_values)
        target_vector.append(vcf_value)
        pnt_df.loc[len(pnt_df) + 1] = [UID, x, y, vcf_value] # FOR TESTING ADD: , stratum])
        UID += 1
    elif vcf_value <= 100 and len(c80100) < 100: # 81-100% stratum
        c80100.append(vcf_value)
        #stratum = 5
        pnt_list.append(pnt)
        feature_matrix.append(tileBand_values)
        target_vector.append(vcf_value)
        pnt_df.loc[len(pnt_df) + 1] = [UID, x, y, vcf_value] # FOR TESTING ADD: , stratum])
        UID += 1

    # console output to keep track
    print("\nTotal Points:",len(pnt_list), "\nc0020:", len(c0020),"\nc2140:", len(c2140),"\nc4160:", len(c4160),"\nc6180:", len(c6180),"\nc80100:", len(c80100))

    ID += 1 # to keep track of random points tested for the stratum conditions


# CHECK RESULT
#print("\nPoint list: \n",pnt_list)

# count Points geometries in Multipoint geometry
#print("\nNumber of random points: ",len(pnt_list))


# STORE RANDOM POINTS WITH VCF VALUES IN SHAPEFILE
print("\nMultiPoint Dataframe : \n",pnt_df)

# create Shapefile from Pandas dataframe
pnt_df['geometry'] = pnt_df.apply(lambda x: Point((float(x.X_COORD), float(x.Y_COORD))), axis=1)# combine lat and lon column to a shapely Point() object (w/ geometry column)
shp_df = gpd.GeoDataFrame(pnt_df, geometry='geometry')                                          # create new dataframe for shapefile with designated geometry column
shp_df.to_file('THEMANN_BRITTA_MAP-task01_randomPoints.shp', driver='ESRI Shapefile')           # write dataframe to shapefile


# STORE RANDOM POINTS WITH RASTER VALUES IN ARRAYS
# Feature Matrix (x) --> classes
arr_fm = np.asarray(feature_matrix)
print("\nFeature Matrix (x) shape: ",arr_fm.shape) #(500,?) --> 770 rows and 4 columns
x_dim = arr_fm.shape[1]
y_dim = arr_fm.shape[0]
outName = "SURNAME_NAME_MAP-task01_np-array_x-values.npy"
np.save(outName, arr_fm)
print(arr_fm)

# Target Vector (y) --> classes
arr_tv = np.asarray(target_vector)
print("\nTarget vector (y) shape:", arr_tv.shape) #(500,) --> 500 rows and 1 column
x_dim = 1 #arr_train_cl.shape[1] --> error
y_dim = arr_tv.shape[0]
outName = "THEMANN_BRITTA_MAP-task01_np-array_y-values.npy"
np.save(outName, arr_tv)
print(arr_tv)


# READ SHAPEFILE (to keep working without having to execute the above each time)
#driver = ogr.GetDriverByName("ESRI Shapefile")
#pnt = driver.Open("THEMANN_BRITTA_MAP-task01_randomPoints.shp",1)
#pnt_lyr = pnt.GetLayer()

#------------------------------------------------------ PART II -------------------------------------------------------#
'''
# extracted training values --> trainingDS_features_4_770.npy
arr_train = np.asarray(df_list)
print("\ntrainingDS_features ",arr_train.shape) #(770,4) --> 770 rows and 4 columns

# classes array --> trainingDS_labels_1_770.npy
arr_train_cl = np.asarray(pt_list)
print("trainingDS_labels ", arr_train_cl.shape) #(770,) --> 770 rows and 1 column
'''
#2) Create numpy arrays
    #2.1) Folder structure untouched
    #2.2) Extract all band values for each raster file
        #scikit-learn structure: Feature Matrix (x) & Target Vector (y)
        #for-loop to go through each band of a raster
    #2.3) Raster file order not important

# SURNAME_NAME_MAP-task01_np-array_x-values.npy
# SURNAME_NAME_MAP-task01_np-array_y-values.npy
# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #

print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")
