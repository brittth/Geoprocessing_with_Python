from osgeo import gdal

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