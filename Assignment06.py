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
#def make_slices(data, win_size):
def make_slices(data, rows, cols):
    yrange = data.shape[0] - rows + 1
    xrange = data.shape[1] - cols + 1
    #print(xrange)
    #print(yrange)
    slices = []
    counter = 0
    for i in range(xrange):
        counter += 1
        for j in range(yrange):
            data_st = data[i:rows+i,j:cols+j]
            arr1d = data_st.flatten()
            slices.append(arr1d)
            #print(slices)
    print(counter)
    sl_arr = np.asarray(slices)
    return(sl_arr)

ds = gdal.Open(tile3)
t3 = np.array(ds.ReadAsArray())
w150 = int((150/30*2)+1)
slices = make_slices(t3,11,11)
print(slices)
'''

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
print(w150)
w300 = int((300/30*2)+1)
w450 = int((450/30*2)+1)

#make window slices --> make_slices(data, win_size)
slices = make_slices(t1,w150,w150)
print(slices)
stacked_data = np.ma.dstack(slices)
#rows, cols = band1.YSize, band1.XSize #check size raster
#out_data = np.ones((rows, cols), np.int32) * -99 #raster in original size with only -99 pixel values

# compute SHDI from tif image
#in_fn = tile1
#out_fn = 'SHDI_Tile_x26999_y12999_1000x1000.tif'
#ds = gdal.Open(in_fn)
# in_band = ds.GetRasterBand(1)
    #pixel count of relevant categories

cat_list = [1, 17, 2, 3, 5, 11, 13, 18 , 19]
counter = 0
for slice in slices:
    #calculate category proportions per slice/window
    print(slice.shape)
    counter += 1
    unique, counts = np.unique(slice, return_counts=True)
    allcat_dict = dict(zip(unique, counts))

    #calculate proportion of all relevant categories
    sum_dict = {}
    for cat in cat_list:
        if cat in allcat_dict:
            sum_dict.update({cat: allcat_dict[cat]})
    allcat_sum = sum(sum_dict.values())

    # calculate proportion of each relevant categories
    result = []
    for cat in cat_list:
        if cat in allcat_dict:
            prop = (allcat_dict[cat]/allcat_sum)
            print('Proportion of Category ' + str(cat) + ' in Slice ' + str(counter) + ': ' + str(prop))

            # define SHDI function: SHDI = −SUM[m,i=1] (Pi*lnPi)
            value = (prop * np.log(prop))
            result.append(value)
    shdi = (-1) * sum(result)
    print(shdi)

#out_data[5:-5, 5:-5] = #eigene function np.mean(stacked_data, 2)

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
'''
# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #

print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")