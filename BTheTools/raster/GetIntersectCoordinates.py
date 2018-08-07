from osgeo import gdal

# GetIntersectCoordinates --> get coordinates of the largest common extent of multiple tif files
    # input: list of input files --> file_list
    # UL --> Upper Left corner
    # LR --> Lower Right corner
def GetIntersectCoordinates(root_folder,file_list):
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