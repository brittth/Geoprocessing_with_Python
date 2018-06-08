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
    slices = []
    counter = 0
    for i in range(xrange):
        counter += 1
        for j in range(yrange):
            # counter += 1
            data_st = data[i:rows+i,j:cols+j]
            arr1d = data_st.flatten()
        slices.append(arr1d) #indent one more to the right for 980100 --> AS IS, SLICES ONLY FOR FIRST ROW
    print('\nWindow size: (',rows,',',cols,')')
    print('Number of windows: ',counter)
    sl_arr = np.asarray(slices)
    print('Shape of array: ', sl_arr.shape)
    print(sl_arr)
    return(sl_arr)

def calculateSHDI(category_list,slice_arr):
    # write occurrences of all categories into a dictionary
    unique, counts = np.unique(slice_arr, return_counts=True)
    allcat_dict = dict(zip(unique, counts))
    # write occurrences of all RELEVANT categories into a dictionary
    sum_dict = {}
    for cat in category_list:
        if cat in allcat_dict:
            sum_dict.update({cat: allcat_dict[cat]})
    allcat_sum = sum(sum_dict.values())
    # calculate proportion of each RELEVANT category
    result = []
    for cat in cat_list:
        if cat in allcat_dict:
            prop = (allcat_dict[cat] / allcat_sum)
            #print('Proportion of Category ' + str(cat) + ': ' + str(prop))
            # define SHDI function: SHDI = −SUM[m,i=1] (Pi*lnPi)
            value = (prop * np.log(prop))
            result.append(value)
    shdi = (-1) * sum(result)
    print('SHDI: ',shdi)
    return shdi

# Create a function called "chunks" with two arguments, l and n:
def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]

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
'''

# ####################################### PROCESSING ########################################################## #
# Moving window sizes:(a) 150m, (b) 300m, and (c) 450m
# Shannon’s diversity index: SHDI = −SUM[m,i=1] (Pi*lnPi)
# 1, 17 --> Forest
# 2, 3, 5, 11, 13, 18, 19 --> Open habitat in 2015 (pasture, natural grassland, savanna)

#load raster as array
#ds = gdal.Open(tile1)
#band1 = ds.GetRasterBand(1)
#t1 = np.array(ds.ReadAsArray())
#ds = gdal.Open(tile2)
#t2 = np.array(ds.ReadAsArray())
ds = gdal.Open(tile3)
t3 = np.array(ds.ReadAsArray())

#calculate window size in pixels
w150 = int((150/30*2)+1)
#w300 = int((300/30*2)+1)
#w450 = int((450/30*2)+1)

#make window slices --> make_slices(data, x_win_size, y_win_size)
#sl1_150 = make_slices(t1,w150,w150)
#sl1_300 = make_slices(t1,w300,w300)
#sl1_450 = make_slices(t1,w450,w450)

#sl2_150 = make_slices(t2,w150,w150)
#sl2_300 = make_slices(t2,w300,w300)
#sl2_450 = make_slices(t2,w450,w450)

sl3_150 = make_slices(t3,w150,w150)
#sl3_300 = make_slices(t3,w300,w300)
#sl3_450 = make_slices(t3,w450,w450)

# calculate shdi for each slice
cat_list = [1, 17, 2, 3, 5, 11, 13, 18, 19]
#np.apply_along_axis(calculateSHDI(cat_list, sl3_150), 1, sl3_150) #--> ERROR
counter = 0
shdi_list = []
for i in sl3_150: #if loop directly in function above, then error
    counter += 1
    print('\nSlice #',counter,':')
    shdi = calculateSHDI(cat_list,sl3_150[i])
    shdi_list.append(shdi) #save shdi values in list
print(len(shdi_list))

# divide shdi_list into chucks of 990 length
shdi_chunks = list(chunks(shdi_list, 990)) #list of 1 list with 990 values, should be more when more than 1 row is considered
print(shdi_chunks)
print(len(shdi_chunks))

#convert shdi_chunks into an array
shdi_arr = np.asarray(shdi_chunks)
print(shdi_arr.shape)
print(shdi_arr.dtype)

#convert array to raster and write to disc
#outfile = drvR.Create(outPath, cols, rows, 1, gdal.GDT_Float32) #robert(forum)
'''
# ATTEMPT 3 FROM STACKOVERFLOW WEBSITE
arr = np.zeros(100).reshape(10,10)
arr2 = np.ones(4).reshape(2,2)
arr[4:6, 4:6] = arr2
print(arr)
'''

# ATTEMPT 2 FROM COOKBOOK WEBSITE
def array2raster(newRasterfn,rasterOrigin,pixelWidth,pixelHeight,array):
    cols = array.shape[1]
    rows = array.shape[0]
    originX = rasterOrigin[0]
    originY = rasterOrigin[1]

    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(newRasterfn, cols, rows, 1, gdal.GDT_Byte)
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
    outband = outRaster.GetRasterBand(1)
    outband.WriteArray(array)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromEPSG(4326)
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()
result = array2raster(newRasterfn,rasterOrigin,pixelWidth,pixelHeight,array)
print(result)

''' # ATTEMPT 1 FROM BOOK CHAPTER 
"""Create a one-band GeoTIFF.
in_ds - datasource to copy projection and geotransform from
fn - path to the file to create
data - NumPy array containing data to write
data_type - output data type
nodata - optional NoData value
"""
in_ds = tile3
fn = wd
data = shdi_arr
data_type = gdal.GDT_Float32
nodata = -999

driver = gdal.GetDriverByName('GTiff')
out_ds = driver.Create(fn, in_ds.RasterXSize, in_ds.RasterYSize, 1, data_type)
out_ds.SetProjection(in_ds.GetProjection())
out_ds.SetGeoTransform(in_ds.GetGeoTransform())
out_band = out_ds.GetRasterBand(1)
if nodata is not None:
    out_band.SetNoDataValue(nodata)
    out_band.WriteArray(data)
    out_band.FlushCache()
    out_band.ComputeStatistics(False)
    #return out_ds

'''



#####################  ARCHIVE  #####################
#stacked_data = np.ma.dstack(slices)
#rows, cols = band1.YSize, band1.XSize #check size raster
#out_data = np.ones((rows, cols), np.int32) * -99 #raster in original size with only -99 pixel values

# compute SHDI from tif image
#in_fn = tile1
#out_fn = 'SHDI_Tile_x26999_y12999_1000x1000.tif'
#ds = gdal.Open(in_fn)
# in_band = ds.GetRasterBand(1)
    #pixel count of relevant categories



#out_data[5:-5, 5:-5] = #eigene function np.mean(stacked_data, 2)
'''
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