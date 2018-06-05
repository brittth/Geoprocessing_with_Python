# ####################################### LOAD REQUIRED LIBRARIES ############################################# #

import time
import os
import numpy as np
import scipy as sc
from osgeo import gdal
import ospybook as pb

# ####################################### SET TIME-COUNT ###################################################### #

starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")

# ####################################### FOLDER PATHS & global variables ##################################### #

wd = "D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 8 - Real-world problems I/Assignment06_data/"
tile1 = wd + 'Tile_x26999_y12999_1000x1000.tif'
tile2 = wd + 'Tile_x19999_y32999_1000x1000.tif'
tile3 = wd + 'Tile_x17999_y20999_1000x1000.tif'

# ####################################### FUNCTIONS ########################################################## #

#Function to get slices of any size from an array
def make_slices(data, win_size):
    """Return a list of slices given a window size.
    data - two-dimensional array to get slices from
    win_size - tuple of (rows, columns) for the moving window
    """
    # calculate slice size
    rows = data.shape[0] - win_size[0] + 1
    cols = data.shape[1] - win_size[1] + 1
    slices = []
    # create the slices
    for i in range(win_size[0]):
        for j in range(win_size[1]):
            slices.append(data[i:rows+i, j:cols+j])
    return slices


def make_raster(in_ds, fn, data, data_type, nodata=None):
    """Create a one-band GeoTIFF.
    in_ds - datasource to copy projection and geotransform from
    fn - path to the file to create
    data - NumPy array containing data to write
    data_type - output data type
    nodata - optional NoData value
    """
    driver = gdal.GetDriverByName('GTiff')
    out_ds = driver.Create(
    fn, in_ds.RasterXSize, in_ds.RasterYSize, 1, data_type)
    out_ds.SetProjection(in_ds.GetProjection())
    out_ds.SetGeoTransform(in_ds.GetGeoTransform())
    out_band = out_ds.GetRasterBand(1)
    if nodata is not None:
    out_band.SetNoDataValue(nodata)
    out_band.WriteArray(data)
    out_band.FlushCache()
    out_band.ComputeStatistics(False)
    return out_ds


# ####################################### PROCESSING ########################################################## #
# Moving window sizes:(a) 150m, (b) 300m, and (c) 450m
# Shannon’s diversity index: SHDI = −SUM[m,i=1] (Pi*lnPi)
# 1, 17 --> Forest
# 2, 3, 5, 11, 13, 18, 19 --> Open habitat in 2015 (pasture, natural grassland, savanna)

#load raster as array
ds = gdal.Open(tile1)
band1 = ds.GetRasterBand(1)
t1 = ds.GetRasterBand(1).ReadAsArray()
ds = gdal.Open(tile2)
t2 = ds.GetRasterBand(1).ReadAsArray()
ds = gdal.Open(tile3)
t3 = ds.GetRasterBand(1).ReadAsArray()

#calculate window size in pixels
w150 = int((150/30*2)+1)
w300 = (300/30*2)+1
w450 = (450/30*2)+1

#make window slices --> make_slices(data, win_size)
slices = make_slices(t1,(w150,w150))
stacked_data = np.ma.dstack(slices)
rows, cols = band1.YSize, band1.XSize #check size raster
out_data = np.ones((rows, cols), np.int32) * -99 #raster in original size with only -99 pixel values

# compute SHDI from tif image
in_fn = tile1
out_fn = 'SHDI_Tile_x26999_y12999_1000x1000.tif'
ds = gdal.Open(in_fn)
# in_band = ds.GetRasterBand(1)
    #pixel count of relevant categories
pixnum = band1.YSize * band1.XSize

cat_list = [1, 17, 2, 3, 5, 11, 13, 18 , 19]
bla = []
for slice in slices:
    for pixel in slice:
        for cat in cat_list:
            if pixel == cat:


    # define SHDI function: SHDI = −SUM[m,i=1] (Pi*lnPi)
cat_list = [1, 17, 2, 3, 5, 11, 13, 18 , 19]
result = []
for cat in cat_list:
    p = count(cat) / count(allcat)
    value = (p * np.log(p))
    result.append(value)
shdi = (-1) * sum(result)

#calculate shdi
out_data[5:-5, 5:-5] = #eigene function np.mean(stacked_data, 2)

pb.make_raster(in_ds, out_fn, out_data, gdal.GDT_Int32, -99)
del in_ds




red = ds.GetRasterBand(1).ReadAsArray().astype(np.float)
nir = ds.GetRasterBand(4).ReadAsArray()
red = np.ma.masked_where(nir + red == 0, red) #mask the red band
ndvi = (nir - red) / (nir + red)
ndvi = ndvi.filled(-99) #fill the empty cells

#out_ds = pb.make_raster(ds, out_fn, ndvi, gdal.GDT_Float32, -99) #set NoData as the fill value
#overviews = pb.compute_overview_levels(out_ds.GetRasterBand(1))
#out_ds.BuildOverviews('average', overviews)
#del ds, out_ds

# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #

print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")