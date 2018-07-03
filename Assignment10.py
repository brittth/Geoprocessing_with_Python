# ####################################### LOAD REQUIRED LIBRARIES ############################################# #

import time
import os
from osgeo import gdal, ogr, osr
import numpy as np
import struct
from joblib import Parallel, delayed
import joblib

# ####################################### SET TIME-COUNT ###################################################### #

starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")

# ####################################### FUNCTIONS ########################################################### #

# ####################################### FOLDER PATHS & global variables ##################################### #

root_folder = "D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 12 - Parallelization/Assignment10_data/"

# ####################################### PROCESSING ########################################################## #
#
#write jobs in list
#worker function already looks at the list elemests of the job list, so only if the joblist is a list of lists do you have to call job[0],...
#execute worker function
if __name__= '__main__':
    output = Parallel(n_jobs=2) (delayed(SumProd_arrays)(i) for i in array_list)

# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #

print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")