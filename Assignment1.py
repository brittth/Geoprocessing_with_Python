# ####################################### LOAD REQUIRED LIBRARIES ############################################# #
'''
import time
import ogr
import baumiTools as bt
'''
import os
import fnmatch
# ####################################### SET TIME-COUNT ###################################################### #
'''
starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")
'''
# ####################################### FOLDER PATHS & global variables ##################################### #
'''
SHP = "L:/_SHARED_DATA/CL_MB/tc_sc/_Version02_300m/points_300m_clip.shp"
outputFile = "L:/_SHARED_DATA/CL_MB/tc_sc/_Version02_300m/points_300m_clip_summary.shp"
buff_m = 100
'''
footprints = "D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 2 - IDE, debugger, first scripts/Assignment01_data/Part01_Landsat/"
# ####################################### PROCESSING ########################################################## #
#create empty lists for names of and paths to each of the footprint folders
foldername_fp_list =[]
dir_list_fp = []

#search through the footprint directory and write them into the footprint paths list
    #find file names in a directory, regardless of type
for foldername_fp in os.listdir(footprints):#for current directory, use: ('.')
    foldername_fp_list.append(foldername_fp)
    dir_list_fp.append(footprints + foldername_fp)
print(foldername_fp_list)
print(dir_list_fp) #list of footprint paths (path_fp)

#create empty list for lists of scenes within each footprint
fp_sc_list = []

#extract a file list from each footprint folder and write it into the empty list of lists
for path_fp in dir_list_fp:
    for foldername_fp in foldername_fp_list:
        foldername_fp =[]
        foldername_fp.append(os.listdir(path_fp))
    fp_sc_list.append(foldername_fp[0]) #the 0 is only to get rid of double brackets
print(fp_sc_list)
print(len(fp_sc_list))

#count scenes per footprint
for i in range(len(fp_sc_list)):
    #if fnmatch.fnmatch(i, 'LC08*'):
        no= len(fp_sc_list[i])
        print(no)

#count scenes per sensor for each footprint
#for i in range(len(fp_sc_list)):
#    noLC08 = {}
#    noLE07 = {}
#    noLT05 = {}





''' #DYSFUNCIONAL
# find number of subdirectories in a directory, folders only

for x in os.listdir(ass1_footprints):
    if os.path.isdir(x):
        ass1_dir_list = [ass1_footprints + x]
    else: continue
    print(ass1_dir_list)
'''


'''
ass1_footprints_LC08 = []
for row in ds_v1:
    print(row.index)
    row = row.replace("\n","")
    cleanList.append(row)
print(cleanList)

for name in correctedNames:
    if name.count(" ") > 2:
        print(name)
'''
# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #
'''
print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")
'''