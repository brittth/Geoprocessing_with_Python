# ####################################### FOR NEW PACKAGE ########################################################## #

# type in anaconda before package installation: activate py36

# ####################################### FUNCTIONS ########################################################## #

#AssignSceneToSensor --> separate the scene path list into different lists according to their sensor
    #directory_list --> list of scene paths
    #search_term --> term that identifies folder as scene of certain sensor (eg. "LT04" for Landsat 4)
    #output_list_name --> name of the PREVIOUSLY CREATED list to which to append the search results
def AssignSceneToSensor (directory_list, search_term, output_list_name):
    for scene_directory in directory_list:
        if search_term in scene_directory:
            output_list_name.append(scene_directory)
    #returns: no print, but saves the result in the given output_list_name
        #application example:
        #dir_list_L4 = []
        #AssignSceneToSensor(dir_list_sc, "LT04", dir_list_L4)

#GetLandsatFileSuffixes --> create lists for Landsat sensor typical file endings
#print((os.listdir(dir_list_L4[1])[1])[40:]) #check were relevant string ending starts --> 40
def GetLandsatFileSuffixes(directory_list, output_list_name):
    for scene in directory_list:                    #takes each scene folder from the directory list
        for file in os.listdir(scene):              #for each file in the scene folder
            output_list_name.append((file[40:]))    #cut off the first 40 characters, as they are the scene name, and write the left over suffixes into the output list
    #returns: no print, but saves the result in the given output_list_name
        #application example (Landsat 4):
            #file_endings_L4 = []  # empty text_file to write the file ending list
            #GetLandsatFileSuffixes(dir_list_L4, file_endings_L4)
            #file_endings_L4 = set(file_endings_L4) #to have each suffix only once in the list
            #print(file_endings_L4) #for illustration
                #returns:
                # {'.xml', '_sr_band5.tif', '_radsat_qa.tif', '_sensor_azimuth_band4.tif', '_GCP.txt', '_VER.jpg', '_solar_azimuth_band4.tif',
                # '_MTL.txt', '_sr_band3.tif', '_solar_zenith_band4.tif', '_sr_band1.tif', '_pixel_qa.tif', '_VER.txt', '_ANG.txt', '_sr_band4.tif',
                # '_sr_atmos_opacity.tif', '_sr_band2.tif', '_sr_band7.tif', '_sensor_zenith_band4.tif', '_bt_band6.tif', '_sr_cloud_qa.tif'}


#CreateLandsatFilesTemplate --> create template files list for each sensor and lists of actual files present
    #directory_list
    #file_suffix_list
    #output_list_name_exfiles
    #output_list_name_potfiles
def CreateLandsatFilesTemplate(directory_list,file_suffix_list,output_list_name_exfiles,output_list_name_potfiles,):
    for scene_path in directory_list:
        files_scene = (os.listdir(scene_path))      #list of actual files present per scene
        scene_name = files_scene[1][:40]            #gather the prefix for the endings
        output_list_name_exfiles.extend(files_scene) #with each iteration add existing file to file list
        for ending in file_suffix_list:
            output_list_name_potfiles.append(((str(scene_name))+ ending))#creates template list of all files that should exist
    #returns: no print, but saves the result in the given output_list_name_exfiles and output_list_name_potfiles
        # application example (Landsat 4):
            # files_L4=[] #for template list
            # actual_files_L4 = [] #for actually existing files
            # CreateLandsatFilesTemplate(dir_list_L4,file_endings_L4,actual_files_L4,files_L4)
            # print(len(files_L4))
            # print(len(actual_files_L4))
            # print(actual_files_L4)
                #returns:
                # 252
                # 251
                # ['LT04_L1TP_229077_19830812_20170220_01_T1.xml', 'LT04_L1TP_229077_19830812_20170220_01_T1_ANG.txt',
                # 'LT04_L1TP_229077_19830812_20170220_01_T1_bt_band6.tif', 'LT04_L1TP_229077_19830812_20170220_01_T1_GCP.txt',
                # 'LT04_L1TP_229077_19830812_20170220_01_T1_MTL.txt', 'LT04_L1TP_229077_19830812_20170220_01_T1_pixel_qa.tif',
                # 'LT04_L1TP_229077_19830812_20170220_01_T1_radsat_qa.tif', 'LT04_L1TP_229077_19830812_20170220_01_T1_sensor_azimuth_band4.tif',
                # ...]

# CompareExFilesToPotFiles --> compare number of existing files to the number of files that should exist
    #layer_list --> list of layer names (i.e. without suffixes)
    #suffix_list --> list of data type suffixes (incl. name attachements)
    #missing_files_list --> previously empty list, will be list of missing files
    #incomplete_layers_list --> previously empty list, will be list of incomplete layers
    #existing_files --> list of existing files of the same type (vector/raster)
    #output_list_name--> previously empty list, will be complete list of files of that type (vector/raster) that should exist
def CompareExFilesToPotFiles(layer_list, suffix_list, missing_files_list, incomplete_layers_list, existing_files, output_list_name):
    for layer in layer_list:
        for ending in set(suffix_list):
            output_list_name.append(layer + ending)
    missing_files_list = []  # list of missing files
    incomplete_layers_list = []  # list of incomplete layers
    diff = lambda output_list_name, existing_files: [x for x in output_list_name if x not in existing_files]
    missing_files_list.extend(diff(output_list_name, existing_files))  # missing files written into list
    for file in missing_files_list:
        incomplete_layers_list.append(file.split(".")[0])  # endings removed to only get the layers
    incomplete_layers_list = set(incomplete_layers_list)  # reduced to unique layer names
    print("\nThere are " + str((len(layer_list)) * (len(set(suffix_list))) - (len(existing_files))) + " file(s) missing from "
          + str(len(incomplete_layers_list)) + " vector layer(s).")
    print("The incomplete vector layers are: " + str(incomplete_layers_list))
    #returns: printed sentences with results
        #application example:
            # vector_files = []  # complete list of vector files that should exist
            # diff_v_list=[] #list of missing files
            # diff_v_list_name = [] #list of incomplete layers
            # CompareExFilesToPotFiles(vector_layers,vector_endings,diff_v_list,diff_v_list_name,vector_existing_files,vector_files)
                #returns:
                # There are 8 file(s) missing from 4 vector layer(s).
                # The incomplete vector layers are: {'DEM_Humboldt_aspect', 'Veg_AsRaster_30m', 'DEM_Humboldt', 'DEM_Humboldt_slope'}


# GetCoordinates --> get coordinates for multiple tif files
    # input: list of input files --> file_list
    # UL --> Upper Left corner
    # LR --> Lower Right corner
def GetCoordinates(file_list):
    for file in file_list:
        ds = gdal.Open(root_folder + file, gdal.GA_ReadOnly)
        gt = ds.GetGeoTransform()  # UL_x, x-coordinate spatial resolution, UL_y, # y-coord. spat.res.
        # Upper left
        UL_x, UL_y = gt[0], gt[3]
        # Lower right
        LR_x = UL_x + (gt[1] * ds.RasterXSize)
        LR_y = UL_y + (gt[5] * ds.RasterYSize)
        print("Coordinates of " + file + ": " + "(" + str(UL_x) + "," + str(UL_y) + ") and (" + str(LR_x) + "," + str(
            LR_y) + ")")
    #returns: printed sentences with results
        #application example:
        # GetCoordinates(file_list)
            #returns:
            # Coordinates of LC08_L1TP_117056_20140521_20170422_01_T1_sr_evi.tif: (505215.0, 673455.0) and (563925.0, 614415.0)
            # Coordinates of LE07_L1TP_117056_20040211_20170122_01_T1_sr_evi.tif: (505455.0, 666525.0) and (564195.0, 607485.0)

# GetIntersectCoordinates --> get coordinates of the largest common extent of multiple tif files
    # input: list of input files --> file_list
    # UL --> Upper Left corner
    # LR --> Lower Right corner
def GetIntersectCoordinates(file_list):
    UL_x_list = []
    UL_y_list = []
    LR_x_list = []
    LR_y_list = []
    for file in file_list:
        ds = gdal.Open(root_folder + file, gdal.GA_ReadOnly)
        gt = ds.GetGeoTransform()  # UL_x, x-coordinate spatial resolution, UL_y, # y-coord. spat.res.
        # Upper left
        UL_x, UL_y = gt[0], gt[3]
        UL_x_list.append(UL_x)
        UL_y_list.append(UL_y)
        # Lower right
        LR_x = UL_x + (gt[1] * ds.RasterXSize)
        LR_y = UL_y + (gt[5] * ds.RasterYSize)
        LR_x_list.append(LR_x)
        LR_y_list.append(LR_y)
    UL_x_ext = max(UL_x_list)
    UL_y_ext = min(UL_y_list)
    LR_x_ext = min(LR_x_list)
    LR_y_ext = max(LR_y_list)
    LL_x_ext = UL_x_ext
    LL_y_ext = LR_y_ext
    UR_x_ext = LR_x_ext
    UR_y_ext = UL_y_ext
    print("The coordinates of the largest common extent are as follows:\n Upper left corner: (" + str(UL_x_ext) + "," + str(
        UL_y_ext) + ")\n Upper right corner: (" + str(UR_x_ext) + "," + str(UR_y_ext) + ")\n Lower left corner: (" + str(
        LL_x_ext) + "," + str(LL_y_ext) + ")\n Lower right corner: (" + str(LR_x_ext) + "," + str(LR_y_ext) + ")")
    #returns: printed sentences with coordinates
    #application example:
    # GetIntersectCoordinates(file_list)
        #returns:
        # The coordinates of the largest common extent are as follows:
        #  Upper left corner: (511635.0,663435.0)
        #  Upper right corner: (563925.0,663435.0)
        #  Lower left corner: (511635.0,614415.0)
        #  Lower right corner: (563925.0,614415.0)


# RasterOverlapToArray --> find and transform the overlap of raster files from a list into arrays stored in an array list
    # input: list of files --> file_list, path to file folder stored as root_folder
    # prerequisites: create an empty array list --> array_list = [], import gdal
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
    print("Common extent spatial resolution: ", spat_res, "\n")
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
    #returns: printed sentences with information on the common extent and stores the resulting arrays in an array list
    #application example:
    # RasterOverlapToArray(file_list)
        # returns:
        # Common extent UL/LR coordinates:  [1399618.9749825108, 705060.6257949192, 1565979.932774514, 360674.0019850965]
        # Common extent in x and y direction:  599 1240
        # Common extent spatial resolution:  [277.73114823372805, 277.731148233728]
        #
        # DEM_Humboldt_sub.tif
        # Cell coordinates of common extent:  245 844 278 1518
        # UL x offset:  245
        # UL y offset:  278
        #
        # SLOPE_Humboldt_sub.tif
        # Cell coordinates of common extent:  109 708 177 1417
        # UL x offset:  109
        # UL y offset:  177

#ThresholdBinaryArrayMask --> create a binary mask based on a threshold, 1s statement fulfilled, 0s all others
    #input: array, which will be overwritte, so copy if original should be kept
    #       operator --> type as string
    #       threshold --> type as number
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
    #returns: overwrites input array with binary mask
    #application example:
    # arr_dem_mask = arr_dem #to be overwritten
    # ThresholdBinaryArrayMask(arr_dem_mask, "<", 1000)
    # print(arr_mask)
        #returns:
        # [[0.0 0.0 0.0 ... 0.0 0.0 0.0]
        # [0.0 0.0 0.0 ... 0.0 0.0 0.0]
        # [0.0 0.0 0.0 ... 0.0 0.0 1.0]
        # ...
        # [1.0 1.0 1.0 ... 0.0 0.0 0.0]
        # [1.0 1.0 1.0 ... 0.0 0.0 0.0]
        # [1.0 1.0 1.0 ... 0.0 0.0 0.0]]

#BinArray2Raster --> write a binary array into a raster file
    # input requires template raster file (originfile_path)
def BinArray2Raster(outfile_name, originfile_path, x_offset, y_offset, array):
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
    outDS = drvR.Create(outfile_name, cols, rows, nbands, gdal.GDT_Byte)
    outDS.SetProjection(pr)
    outDS.SetGeoTransform(gt)
    # 3. Write the array into the newly generated file
    outDS.GetRasterBand(1).WriteArray(array, x_offset, y_offset) # (array, offset_x, offset_y)
    #returns: writes a raster to disc, located in the same folder as the script
    #application example:
    # originfile_path = root_folder + THP  # since its has the same extent and spatial resolution as arr_mask
    # BinArray2Raster("binary_mask.tif", originfile_path, 0, 0, arr_mask)
        #returns: creates binary_mask.tif
# ####################################### TEMPLATES ########################################################## #

#count scenes per sensor for each folder (ex. footprint)
import os #list directories
import re #use regular expressions
    #dir_list_fp is a list of footprint paths (path_fp)
    #folder structure is footprint(ex. 228_077)--> scene(ex. LT052280772011102901T1)
    # for each footprint folder find the number of scenes for each sensor
    # here only sensors: Landsat 4, 5, 7 and 8 have been used
    #"^..." --> substring to be found
for path_fp in dir_list_fp:
    L4 = filter((re.compile("^LT04")).match, os.listdir(path_fp))   #re.compile() to set search term, .match to look for search term, os.lissir(path_fp) represent search location
    L5 = filter((re.compile("^LT05")).match, os.listdir(path_fp))
    L7 = filter((re.compile("^LE07")).match, os.listdir(path_fp))
    L8 = filter((re.compile("^LC08")).match, os.listdir(path_fp))
    print("For footprint " + str(path_fp[-7:]) + ", there are " + str(len(list(L4))) + " Landsat 4, " + str(len(list(L5))) + " Landsat 5, " + str(len(list(L7))) + " Landsat 7 and " + str(len(list(L8))) + " Landsat 8 scenes.")
    #returns:
    #For footprint 228_077, there are 0 Landsat 4, 309 Landsat 5, 282 Landsat 7 and 82 Landsat 8 scenes.
    #For footprint 228_078, there are 0 Landsat 4, 310 Landsat 5, 280 Landsat 7 and 81 Landsat 8 scenes.
    #...


#create path list for folders irrespective of parent folder by concatenating path of parent folders with the folder
    #application here: create a complete path list to each scene irrespective of footprint (list of lists)
    #foldername_sc_list --> list of foldernames (ex. scenes) from all parent folders (ex. footprints)
    #dir_list_sc --> desired output: list of all path to the folders (ex. scenes)
    #dir_list_fp --> list of parent folders (ex. footprints)
foldername_sc_list =[]
dir_list_sc = []
for path_fp in dir_list_fp:
    for foldername_sc in os.listdir(path_fp):
        dir_list_sc.append(path_fp + "/" + foldername_sc)   #path and folder concatenated by '/'
print (dir_list_sc)
    #returns:
    #['D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 2 - IDE, debugger, first scripts/Assignment01_data/Part01_Landsat/228_077/LC082280772013042501T1',
    # 'D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 2 - IDE, debugger, first scripts/Assignment01_data/Part01_Landsat/228_077/LC082280772013051101T1',
    # ...,
    # 'D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 2 - IDE, debugger, first scripts/Assignment01_data/Part01_Landsat/228_078/LT052280782011102901T1',
    # 'D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 2 - IDE, debugger, first scripts/Assignment01_data/Part01_Landsat/228_079/LC082280792013051101T1',
    # ...]

#extract a file list from a number of subfolders within a number of different parent folders in the working directory
    #fp_sc_list --> desired output list of files from all subfolders (here scenes)
    #dir_list_fp --> directory list of parent folders (here footprints)
    #foldername_fp_list --> list of parent folder names (here footprints)
fp_sc_list = []
for path_fp in dir_list_fp:
    for foldername_fp in foldername_fp_list:
        foldername_fp =[]
        foldername_fp.append(os.listdir(path_fp))
    fp_sc_list.append(foldername_fp[0]) #the 0 is only to get rid of double brackets
print(fp_sc_list)
print(len(fp_sc_list))
    #returns: To be continued...

#check for missing files in list of folder directories/paths based on the maximum number of files present in any of those folders
    #check maximum number of files per scene directory
        #dir_list_L4 --> list of Landsat 4 scene directories/paths
no_file_L4 = []
for scene_dir in dir_list_L4:
    no_file_L4.append(len(os.listdir(scene_dir)))
print("The maximum number of files in a Landsat 4 scene is " + str(max(no_file_L4)) + " and the minimum is " + str(min(no_file_L4)) + ".")
        #returns:
        # The maximum number of files in a Landsat 4 scene is 21 and the minimum is 20.
    #count the number of scenes with files missing
no_corrupt_sc_L4 = (sum(i < (max(no_file_L4)) for i in no_file_L4))
print("There are " + str(no_corrupt_sc_L4) + " Landsat 4 scene(s) with files missing.")
        #returns:
        # There are 1 Landsat 4 scene(s) with files missing.



#print keys and values in dictionary
dict = {"A":"Hello","B":"Hey","C":"Hi","D":"What's up?"}
for key in dict:
    print(key)
    print(dict[key])
    #returns:
    #A
    #Hello
    #B
    #Hey
    #C
    #Hi
    #D
    #What's up?

#working with regular expressions
mylist = ["dog", "cat", "wildcat", "thundercat", "cow", "hooo"]
r = re.compile(".*cat")
newlist = filter(r.match, mylist)
print (list(newlist))
    #returns:
    # ['cat', 'wildcat', 'thundercat']

# ####################################### unsorted FUNCTIONS ########################################################## #

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

def CalculateSHDI2Array(slices,cat_list,windows_size, message_string):
    counter = 0
    shdi_list =[]
    for i in slices: #if loop directly in function above, then error
        counter += 1
        print(message_string)
        print('\nSlice #',counter,':')
        shdi = calculateSHDI(cat_list,slices[i])
        shdi_list.append(shdi) #save shdi values in list
    # divide shdi_list into chucks of certain length
    shdi_chunks = list(chunks(shdi_list, (1000 - windows_size + 1)))  # list of lists with values
    print('SHDI Lists in chunks created with chunk length of ', len(shdi_chunks), '.')
    # convert shdi_chunks into an array
    shdi_arr = np.asarray(shdi_chunks)
    print('The SHDI array has a shape of:', shdi_arr.shape)
    print('The SHDI array has the data type: ', shdi_arr.dtype)
    return shdi_arr

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

def FromSlicetoRaster(slices,cat_list,windows_size, message_string,outfile_name,originfile_path):
    # calculate shdi for each slice and write into an array
    shdi_arr = CalculateSHDI2Array(slices, cat_list, windows_size, message_string)
    # insert smaller array into a larger zeros array
    arr = insertArray(shdi_arr, windows_size)
    print('The smaller arrays of size', shdi_arr.shape, 'was inserted into the larger array of size',arr.shape, '.')
    # convert array to raster and write to disc
    Array2Raster(outfile_name, originfile_path, 0, 0, arr, gdal.GDT_Float64)


def reprojectSHP2Lambert(file_path, outfile_name): #tb tested
    ds = gpd.read_file(file_path)
    ds_lambert = ds.to_crs({'init': 'EPSG:3035'})
    ds_lambert.to_file(wd + outfile_name)
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds_pr = driver.Open(wd + outfile_name, 0)
    ds_pr = ds_pr.GetLayer()
    return ds_pr

def reprojectSHP2WGS84(file_path, outfile_name):#tb tested
    ds = gpd.read_file(file_path)
    ds_lambert = ds.to_crs({'init': 'EPSG:4326'})
    ds_lambert.to_file(wd + outfile_name)
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds_pr = driver.Open(wd + outfile_name, 0)
    ds_pr = ds_pr.GetLayer()
    return ds_pr

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
# ####################################### unsorted TEMPLATES ########################################################## #
'''
mylist=fp_sc_list[0]
print (mylist)

# only works for one letter
def countStringStart(mylist):
    count = 0
    for item in mylist:
        if item[0].startswith('L'):
            count +=1
    return count
print(countStringStart(mylist))
'''

#count scenes per footprint
#for i in range(len(fp_sc_list)):
#        no= len(fp_sc_list[i])
#        print(no)

#s[:4] + '-' + s[4:] #insert a char into a string
#x.extend(y+z)#merging multiple lists at once, by adding each element, so it doesn't become a list of lists

'''
def remove_duplicates():
    t = ['a', 'b', 'c', 'd']
    t2 = ['a', 'c', 'd']
    for t in t2:
        t.append(t.remove())
    return t 
'''
''' #Splitting a Path into All of Its Parts, not tested but might be useful
import os, sys
def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts
    '''