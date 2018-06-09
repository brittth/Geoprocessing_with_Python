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

def insertArray(insertion_array, window_size):
    arr = np.zeros(1000*1000).reshape(1000,1000)
    arr[int((window_size-1)/2):int(((window_size-1)/2)+(1000-window_size+1)), int((window_size-1)/2):int(((window_size-1)/2)+(1000-window_size+1))] = insertion_array
    return arr

def Array2Raster(outfile_name, originfile_path, x_offset, y_offset, array, outfile_datatype):
    ds = gdal.Open(originfile_path)
    # Get the basic properties of the raster file
    gt = ds.GetGeoTransform()
    pr = ds.GetProjection()
    cols = ds.RasterXSize
    rows = ds.RasterYSize
    nbands = ds.RasterCount
    # 1. Create a driver with which we write the output
    drvR = gdal.GetDriverByName('GTiff')
    # 2. Create the file (here: although exactly the same, we go through the syntax)
    outDS = drvR.Create(outfile_name, cols, rows, nbands, outfile_datatype)
    outDS.SetProjection(pr)
    outDS.SetGeoTransform(gt)
    # 3. Write the array into the newly generated file
    outDS.GetRasterBand(1).WriteArray(array, x_offset, y_offset) # (array, offset_x, offset_y)

# ####################################### PROCESSING ########################################################## #
# Moving window sizes:(a) 150m, (b) 300m, and (c) 450m
# Shannon’s diversity index: SHDI = −SUM[m,i=1] (Pi*lnPi)
# 1, 17 --> Forest
# 2, 3, 5, 11, 13, 18, 19 --> Open habitat in 2015 (pasture, natural grassland, savanna)

#load raster as array
ds = gdal.Open(tile1)
t1 = np.array(ds.ReadAsArray())
ds = gdal.Open(tile2)
t2 = np.array(ds.ReadAsArray())
ds = gdal.Open(tile3)
t3 = np.array(ds.ReadAsArray())

#calculate window size in pixels
w150 = int((150/30*2)+1)
w300 = int((300/30*2)+1)
w450 = int((450/30*2)+1)

#make window slices --> make_slices(data, x_win_size, y_win_size)
sl1_150 = make_slices(t1,w150,w150)
sl1_300 = make_slices(t1,w300,w300)
sl1_450 = make_slices(t1,w450,w450)

sl2_150 = make_slices(t2,w150,w150)
sl2_300 = make_slices(t2,w300,w300)
sl2_450 = make_slices(t2,w450,w450)

sl3_150 = make_slices(t3,w150,w150)
sl3_300 = make_slices(t3,w300,w300)
sl3_450 = make_slices(t3,w450,w450)

# calculate shdi for each slice
cat_list = [1, 17, 2, 3, 5, 11, 13, 18, 19]
data_list = [sl1_150,sl1_300,sl1_450,sl2_150,sl2_300,sl2_450,sl3_150,sl3_300,sl3_450]
shdi_list_list = [0] * 9
iter = 0
for element in data_list:
    counter = 0
    shdi_list =[]
    for i in element: #if loop directly in function above, then error
        counter += 1
        print('\nSlice #',counter,':')
        shdi = calculateSHDI(cat_list,element[i])
        shdi_list.append(shdi) #save shdi values in list
    shdi_list_list[iter] = shdi_list
    iter += 1
#print(shdi_list_list)

shdi_list_sl1_150 = shdi_list_list[0]
shdi_list_sl1_300 = shdi_list_list[1]
shdi_list_sl1_450 = shdi_list_list[2]

shdi_list_sl2_150 = shdi_list_list[3]
shdi_list_sl2_300 = shdi_list_list[4]
shdi_list_sl2_450 = shdi_list_list[5]

shdi_list_sl3_150 = shdi_list_list[6]
shdi_list_sl3_300 = shdi_list_list[7]
shdi_list_sl3_450 = shdi_list_list[8]

shdi_list_list.clear() #delete list
print('SHDI List created')

# divide shdi_list into chucks of certain length
shdi_chunks_sl1_150 = list(chunks(shdi_list, (1000-w150+1))) #list of 990 lists with 990 values
shdi_chunks_sl2_150 = list(chunks(shdi_list, (1000-w150+1)))
shdi_chunks_sl3_150 = list(chunks(shdi_list, (1000-w150+1)))
print('SHDI Lists in chunks created with chunk length of ', len(shdi_chunks_sl3_150),'.')

shdi_chunks_sl1_300 = list(chunks(shdi_list, (1000-w300+1))) #list of 980 lists with 980 values
shdi_chunks_sl2_300 = list(chunks(shdi_list, (1000-w300+1)))
shdi_chunks_sl3_300 = list(chunks(shdi_list, (1000-w300+1)))
print('SHDI Lists in chunks created with chunk length of ', len(shdi_chunks_sl3_300),'.')

shdi_chunks_sl1_450 = list(chunks(shdi_list, (1000-w450+1))) #list of 970 lists with 970 values
shdi_chunks_sl2_450 = list(chunks(shdi_list, (1000-w450+1)))
shdi_chunks_sl3_450 = list(chunks(shdi_list, (1000-w450+1)))
print('SHDI Lists in chunks created with chunk length of ', len(shdi_chunks_sl3_450),'.')

#convert shdi_chunks into an array
shdi_arr_sl1_150 = np.asarray(shdi_chunks_sl1_150)
shdi_arr_sl2_150 = np.asarray(shdi_chunks_sl2_150)
shdi_arr_sl3_150 = np.asarray(shdi_chunks_sl3_150)
print('The SHDI arrays have a shape of:',shdi_arr_sl3_150.shape)
print('The SHDI arrays have the data type: ',shdi_arr_sl3_150.dtype)

shdi_arr_sl1_300 = np.asarray(shdi_chunks_sl1_300)
shdi_arr_sl2_300 = np.asarray(shdi_chunks_sl2_300)
shdi_arr_sl3_300 = np.asarray(shdi_chunks_sl3_300)
print('The SHDI arrays have a shape of:',shdi_arr_sl3_300.shape)
print('The SHDI arrays have the data type: ',shdi_arr_sl3_300.dtype)

shdi_arr_sl1_450 = np.asarray(shdi_chunks_sl1_450)
shdi_arr_sl2_450 = np.asarray(shdi_chunks_sl2_450)
shdi_arr_sl3_450 = np.asarray(shdi_chunks_sl3_450)
print('The SHDI arrays have a shape of:',shdi_arr_sl3_450.shape)
print('The SHDI arrays have the data type: ',shdi_arr_sl3_450.dtype)

#insert smaller array into a larger zeros array
arr_sl1_150 = insertArray(shdi_arr_sl1_150, w150)
arr_sl2_150 = insertArray(shdi_arr_sl2_150, w150)
arr_sl3_150 = insertArray(shdi_arr_sl3_150, w150)
print('The smaller arrays of size',shdi_arr_sl3_150.shape,'was inserted into the larger array of size',arr_sl3_150.shape,'.')

arr_sl1_300 = insertArray(shdi_arr_sl1_300, w300)
arr_sl2_300 = insertArray(shdi_arr_sl2_300, w300)
arr_sl3_300 = insertArray(shdi_arr_sl3_300, w300)
print('The smaller arrays of size',shdi_arr_sl3_300.shape,'was inserted into the larger array of size',arr_sl3_300.shape,'.')

arr_sl1_450 = insertArray(shdi_arr_sl1_450, w450)
arr_sl2_450 = insertArray(shdi_arr_sl2_450, w450)
arr_sl3_450 = insertArray(shdi_arr_sl3_450, w450)
print('The smaller arrays of size',shdi_arr_sl3_450.shape,'was inserted into the larger array of size',arr_sl3_450.shape,'.')

    #smaller test array for demonstration --> works perfectly
#arr3 = np.zeros(25).reshape(5,5)
#print(arr3.shape)
#arr4 = np.ones(9).reshape(3,3)
#print(arr4.shape)
#arr3[1:4,1:4] = arr4
#print(arr3.shape)
#print(arr3)

#convert array to raster and write to disc
Array2Raster('1_150.tif', tile1, 0, 0, arr_sl1_150, gdal.GDT_Float64)
Array2Raster('1_300.tif', tile1, 0, 0, arr_sl1_300, gdal.GDT_Float64)
Array2Raster('1_450.tif', tile1, 0, 0, arr_sl1_450, gdal.GDT_Float64)

Array2Raster('2_150.tif', tile2, 0, 0, arr_sl2_150, gdal.GDT_Float64)
Array2Raster('2_300.tif', tile2, 0, 0, arr_sl2_300, gdal.GDT_Float64)
Array2Raster('2_450.tif', tile2, 0, 0, arr_sl2_450, gdal.GDT_Float64)

Array2Raster('3_150.tif', tile3, 0, 0, arr_sl3_150, gdal.GDT_Float64)
Array2Raster('3_300.tif', tile3, 0, 0, arr_sl3_300, gdal.GDT_Float64)
Array2Raster('3_450.tif', tile3, 0, 0, arr_sl3_450, gdal.GDT_Float64)

# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #

print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")