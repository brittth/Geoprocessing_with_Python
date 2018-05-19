# ####################################### LOAD REQUIRED LIBRARIES ############################################# #

import time
import os
import gdal
import numpy as np
import numpy.ma as ma

# ####################################### SET TIME-COUNT ###################################################### #

starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")

# ####################################### FOLDER PATHS & global variables ##################################### #
root_folder = "D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 5 - Raster processing II/Assignment03 - data/"

DEM = "DEM_Humboldt_sub.tif"
SLOPE = "SLOPE_Humboldt_sub.tif"
THP = "THP_Humboldt_sub.tif"

# ####################################### FUNCTIONS ########################################################## #

def RasterOverlapToArray(file_list):
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
    print("Common extent spatial resolution: ", spat_res,"\n")
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

def ThresholdBinaryArrayMask(array, operator, threshold):
    if operator == '<':
        array[array < threshold] = 1  # replace all values <1000 with 1
    elif operator == '>':
        array[array > threshold] = 1  # replace all values <1000 with 1
    elif operator == '<=':
        array[array <= threshold] = 1  # replace all values <1000 with 1
    elif operator == '>=':
        array[array >= threshold] = 1  # replace all values <1000 with 1
    elif operator == '==':
        array[array == threshold] = 1  # replace all values <1000 with 1
    elif operator == '!=':
        array[array != threshold] = 1  # replace all values <1000 with 1
    array[array != 1] = 0  # replace all values other than 1 with 0
# ####################################### PROCESSING ########################################################## #

##EXERCISE 1
print("EXCERCIZE I\n")
#list files for whom the common extent is needed
file_list = os.listdir(root_folder)
#print(file_list)

#get the coordinates of the common extent and transform it into an arrays
array_list = []
RasterOverlapToArray(file_list)
arr_dem = array_list[0]
arr_slo = array_list[1]
arr_thp = array_list[2]

#calculate elevation and slope statistics while excluding/masking NoData values: mean, min, max
arr_dem = ma.masked_where(arr_dem >= 8000, arr_dem)
arr_slo = ma.masked_where(arr_slo < 0, arr_slo)
arr_thp = ma.masked_where(arr_thp > 10000, arr_thp)
print(' mean DEM:', np.mean(arr_dem), "\n", 'min DEM:', np.min(arr_dem),'\n','max DEM:', np.max(arr_dem),'\n',
      'mean SLOPE:', np.mean(arr_slo),'\n', 'min SLOPE:', np.min(arr_slo),'\n','max SLOPE:', np.max(arr_slo))

#build a binary mask in which areas with elevation < 1000m and slope <30deg have the value ‘1’, and all other areas the value ‘0’
    #shorter without a function, but better to have a function longterm
arr_dem_mask = arr_dem #to be overwritten
ThresholdBinaryArrayMask(arr_dem_mask, "<", 1000)
arr_slo_mask = arr_slo #to be overwritten
ThresholdBinaryArrayMask(arr_slo_mask, "<", 30)
arr_mask = arr_dem_mask + arr_slo_mask #add the array values
arr_mask[arr_mask == 1] = 0 #replace all 1s with 0s
arr_mask[arr_mask == 2] = 1 #replace all 2s with 1s
#print(arr_mask)

# Calculate the proportional area (two decimal digits) of raster cells having the value ‘1’ relative to the entire area
numrows = len(arr_mask)    # 1240 rows
numcols = len(arr_mask[0]) # 599 columns
numcells = numrows * numcols # 742760 cells
ones = (len(arr_mask[arr_mask == 1])) # 450992 1s present
#zeros = (len(arr_mask[arr_mask == 0])) # 291768 1s present
ds = gdal.Open(root_folder + DEM, gdal.GA_ReadOnly)
gt = ds.GetGeoTransform()  # UL_x, x-coordinate spatial resolution, UL_y, # y-coord. spat.res.
spat_res = [gt[1], abs(gt[5])]
entire_area = numcells * spat_res[0] * spat_res[1]
ones_area = ones * spat_res[0] * spat_res[1]
ones_prop_area = ones_area/entire_area
ones_prop_area = round(ones_prop_area, 2)
print("\nThe proportional area of cells containing 1s is: ",ones_prop_area," or ",ones_prop_area*100,"%.")


# Write this binary mask into a new raster file
#TBC
'''
    # Get the basic properties of the raster file
    gt = ds.GetGeoTransform()
    pr = ds.GetProjection()
    cols = ds.RasterXSize
    rows = ds.RasterYSize
    nbands = ds.RasterCount

    # Get the raster values (from the entire raster)
    rb = ds.GetRasterBand(1)
    dtype = rb.DataType
    arr = rb.ReadAsArray(0,0,cols,rows) # (origin_x, origin_y, sliceSize_x, SliceSize_y)
    # 0. Formulate an outputName
    outfile = root_folder + "DEM_Humboldt_sub_copy.tif"
    # 1. Create a driver with which we write the output
    drvR = gdal.GetDriverByName('GTiff')
    # 2. Create the file (here: allthough exactly the same, we go through the syntax)
    outDS = drvR.Create(outfile, cols, rows, nbands, dtype)
    outDS.SetProjection(pr)
    outDS.SetGeoTransform(gt)
    # 3. Write the array into the newly generated file
    outDS.GetRasterBand(1).WriteArray(arr, 0, 0) # (array, offset_x, offset_y)
'''

##EXERCISE 2
print("\n\nEXCERCIZE II\n")
#For each of the areas of the different values in the THP raster dataset calculate the mean values slope and elevation with two decimal digits.
    #arr_stack = ma.dstack((arr_dem, arr_slo)) #stack the two half masked arrays
years = list(range(np.min(arr_thp), (np.max(arr_thp)+1))) # +1 because the last number is exclusive
values_file = []
for year in years:
    year_dem_mask = ma.masked_where(arr_thp != year, arr_dem)
    year_slo_mask = ma.masked_where(arr_thp != year, arr_slo)
    values = []
    values.append(year)
    values.append(round(np.mean(year_dem_mask), 2))
    values.append(round(np.mean(year_slo_mask), 2))
    values_file.append(values)
    #print("\n", year)
    #print(year_dem_mask)
    #print(year_slo_mask)
    #print("mean DEM: ", round(np.mean(year_dem_mask),2))
    #print("mean SLOPE: ", round(np.mean(year_slo_mask), 2))
print(values_file)

'''#TEST
a = [10, 20, 30, 40, 10]
a= np.array(a, dtype=np.int16)
b = [1997,0,1997,0,1997]
b= np.array(b, dtype=np.int16)
c = ma.masked_where(b != 1997, a)
print(c)
print(np.mean(c))
'''

#Write the results into a comma-separated values file. Each row thereby should have the format Year, Mean_elev, Mean_slope
outF = open("values_file.txt", "w") #create new txt file
for line in values_file:
    outF.write(str(line[0]))
    outF.write(",")
    outF.write(str(line[1]))
    outF.write(",")
    outF.write(str(line[2]))
    outF.write("\n")
outF.close()

'''
# Open Raster
ds = gdal.Open(root_folder + file)

# Get the basic properties of the raster file
gt = ds.GetGeoTransform()
pr = ds.GetProjection()
cols = ds.RasterXSize
rows = ds.RasterYSize
nbands = ds.RasterCount

# Get the raster values (from the entire raster)
rb = ds.GetRasterBand(1)
dtype = rb.DataType
arr = rb.ReadAsArray(0,0,cols,rows) # (origin_x, origin_y, sliceSize_x, SliceSize_y)

# 0. Formulate an outputName
outfile = root_folder + "DEM_Humboldt_sub_copy.tif"
# 1. Create a driver with which we write the output
drvR = gdal.GetDriverByName ("GTiff")
# 2. Create the file (here: although exactly the same, we go through the syntax)
outDS = drvR.Create(outfile,cols,rows,nbands,dtype)
outDS.SetProjection(pr)
outDS.SetGeoTransform(gt)
# 3. Write the array into the newly generated file
outDS.GetRasterBand(1).WriteArray(arr,0,0) # array, offset_x, offset_y)
'''

# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #

print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")