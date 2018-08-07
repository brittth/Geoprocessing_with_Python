from osgeo import gdal

# RasterOverlapToArray --> find and transform the overlap of raster files from a list into arrays stored in an array list
    # input: list of files --> file_list, path to file folder stored as root_folder
    # output: array_list = []
def RasterOverlapToArray(file_path_list):
    UL_x_list = []
    UL_y_list = []
    LR_x_list = []
    LR_y_list = []
    array_list = []
    for file_path in file_path_list:
        ds = gdal.Open(file_path, gdal.GA_ReadOnly)
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
    for file_path in file_path_list:  #convert real-world coordinates (lat/lon) to image coordinates (x,y)
        print(file_path) #for overview in console
        ds = gdal.Open(file_path, gdal.GA_ReadOnly)
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
    return array_list
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