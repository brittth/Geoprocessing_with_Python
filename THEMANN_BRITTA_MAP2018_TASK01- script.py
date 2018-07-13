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

# ####################################### SET TIME-COUNT ###################################################### #

starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")

# ####################################### FUNCTIONS ########################################################### #

#GetCoordinates --> get coordinates for multiple tif files
    # input: list of input files --> file_list
    # UL --> Upper Left corner
    # LR --> Lower Right corner
def GetCoordinates(file_list, root_folder):
    UL_x_list = []
    UL_y_list = []
    LR_x_list = []
    LR_y_list = []
    for file in file_list:
        coord_list = []
        ds = gdal.Open(root_folder + file, gdal.GA_ReadOnly)
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
        print("Coordinates of " + file + ": " + "(" + str(UL_x) + "," + str(UL_y) + ") and (" + str(LR_x) + "," + str(LR_y) + ")")
    return UL_x_list, UL_y_list, LR_x_list, LR_y_list


# ####################################### FOLDER PATHS & GLOBAL VARIABLES ##################################### #

rootFolder = "D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/MAP/Geoprocessing-in-python_MAP2018_data/Task01_data/"

ras1 = "Tile_x18999_y38999_1000x1000_2014-2015_CHACO"
ras2 = "Tile_x18999_y38999_1000x1000_2014-2015_CHACO"
ras3 = "Tile_x18999_y38999_1000x1000_2014-2015_CHACO"
ras4 = "Tile_x18999_y38999_1000x1000_2014-2015_CHACO"
L8_doy = rootFolder + "2015_L8_doy015/"
L8_met = rootFolder + "2015_L8_metrics/"
S1_met_VH = rootFolder + "2015_S1_metrics/VH_mean/"
S1_met_VV = rootFolder + "2015_S1_metrics/VV_mean/"

path_VCF = rootFolder + "2000_VCF/20S_070W.tif"

path_L8_doy1 = L8_doy + ras1 + "_PBC_multiYear_Imagery.bsq"
path_L8_doy2 = L8_doy + ras2 + "_PBC_multiYear_Imagery.bsq"
path_L8_doy3 = L8_doy + ras3 + "_PBC_multiYear_Imagery.bsq"
path_L8_doy4 = L8_doy + ras4 + "_PBC_multiYear_Imagery.bsq"
'''
path_L8_metrics1 = L8_met + ras1 + "_PBC_multiYear_Metrics.bsq"
path_L8_metrics2 = L8_met + ras2 + "_PBC_multiYear_Metrics.bsq"
path_L8_metrics3 = L8_met + ras3 + "_PBC_multiYear_Metrics.bsq"
path_L8_metrics4 = L8_met + ras4 + "_PBC_multiYear_Metrics.bsq"

path_S1_metricsVH1 = S1_met_VH + ras1 + ".tif"
path_S1_metricsVH2 = S1_met_VH + ras2 + ".tif"
path_S1_metricsVH3 = S1_met_VH + ras3 + ".tif"
path_S1_metricsVH4 = S1_met_VH + ras4 + ".tif"

path_S1_metricsVV1 = S1_met_VV + ras1 + ".tif"
path_S1_metricsVV2 = S1_met_VV + ras2 + ".tif"
path_S1_metricsVV3 = S1_met_VV + ras3 + ".tif"
path_S1_metricsVV4 = S1_met_VV + ras4 + ".tif"
'''
# ####################################### PROCESSING ########################################################## #

#1) Create random points
    #1.1) Tree cover strata: 100x0-20% , 100x21-40%,... covered by all four tiles = 500 points

# write the file names containing ".bsq" of each tile into a file_list_bsq
file_list_all = os.listdir(L8_doy)
print("All files in folder: \n",file_list_all,"\n")
file_list_bsq = []
for file in file_list_all:
    if "bsq" in file:
        file_list_bsq.append(file)
print("Only bsq files in folder: \n",file_list_bsq,"\n")

# identify UL and LR corner coordinates of the area covered by the 4 tiles
print("Extracting corner coordinates of the 4 tiles:")
UL_x_list, UL_y_list, LR_x_list, LR_y_list = GetCoordinates(file_list_bsq,L8_doy)
UL_x = min(UL_x_list)
UL_y = max(UL_y_list)
LR_x = max(LR_x_list)
LR_y = min(LR_y_list)
print("\nCorner coordinates of the area covered by the 4 tiles: \n UL(",UL_x,",",UL_y,") and LR(",LR_x,",",LR_y,")")

# read VFC raster
vcf = gdal.Open(path_VCF)
# get projection from raster
vcf_pr = vcf.GetProjection()
target_SR = osr.SpatialReference()         # create empty spatial reference
target_SR.ImportFromWkt(vcf_pr)            # get spatial reference from projection of raster
print("\nSpatial Reference of the VFC raster file: \n",target_SR)

# generate random points

# random points data frame preparation
ID = 0
pnt_df = pd.DataFrame(columns=["UID", "X_COORD", "Y_COORD", "VCF"])

pnt_list = [] # create list to store point information in
pnts = ogr.Geometry(ogr.wkbMultiPoint)  # create point class object MultiPoint

while len(pnt_list) < 5:
    x_random = random.choice(np.arange(UL_x, LR_x, 30)) # generate random x coordinate from range of x values
    y_random = random.choice(np.arange(LR_y, UL_y, 30)) # generate random y coordinate from range of y values

    # create a geometry from coordinates
    pnt = ogr.Geometry(ogr.wkbPoint)  # create point class object Point
    pnt.AddPoint(x_random, y_random)  # add point coordinate

    # assign spatial reference system from VFC raster to Point geometry
    pnt.AssignSpatialReference(target_SR)
    print("\nSpatial Reference of point feature with ID ",ID,": \n", pnt.GetSpatialReference())

    #extract value from point


    # add Point geometry to MultiPoint geometry
    pnts.AddGeometry(pnt)

    # append to point list
    pnt_list.append(pnt)

    # prepare data to write to disc as csv
    pnt_df.loc[len(pnt_df) + 1] = [ID, x_random, y_random, "ToBeFilled"]
    ID += 1

#print("\nPoint list: \n",pnt_list)

# export MultiPoint geometry to WKT (Well Known Text)
pnts_wkt = pnts.ExportToWkt()
print("\nMultiPoint WKT: \n",pnts_wkt)

# count Points geometries in Multipoint geometry
print("\nGeometry has %i geometries" % (pnts.GetGeometryCount()))

# create Shapefile from Pandas dataframe
print("\nMultiPoint Dataframe : \n",pnt_df)
pnt_df['geometry'] = pnt_df.apply(lambda x: Point((float(x.X_COORD), float(x.Y_COORD))), axis=1) # combine lat and lon column to a shapely Point() object (w/ geometry column)
shp_df = gpd.GeoDataFrame(pnt_df, geometry='geometry') # create new dataframe for shapefile with designated geometry column
#shp_df.crs = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs" # add projection to dataframe
shp_df.to_file('MyGeometries.shp', driver='ESRI Shapefile') # write dataframe to shapefile

# CSV OUTPUT
# write random point sample to csv file in the rootFolder to check on the points
#pnt_df.to_csv(rootFolder + "test.csv", index=None, sep=';', mode='a')



c0020 = [] #0-20% stratum
c2140 = [] #21-40% stratum
c4160 = [] #41-60% stratum
c6180 = [] #61-80% stratum
c80100 = [] #81-100% stratum

        #while loop to get 100 per condition
        #condition is percentage tree cover according to VCF
    #1.2) Add ID-Field
        #after finishing while loop
    #1.3) Add attribute named VCF with tree cover percent
        #in while loop


#2) Create numpy arrays
    #2.1) Folder structure untouched
    #2.2) Extract all band values for each raster file
        #scikit-learn structure: Feature Matrix (x) & Target Vector (y)
        #for-loop to go through each band of a raster
    #2.3) Raster file order not important

#output form: pandas dataframe - ID,VCF,(x,y),raster band values
# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #

print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")