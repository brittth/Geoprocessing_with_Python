# ####################################### LOAD REQUIRED LIBRARIES ############################################# #
'''
import time
import ogr
import baumiTools as bt
'''
import os
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
ass1_footprints = "D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 2 - IDE, debugger, first scripts/Assignment01_data/Part01_Landsat/"
# ####################################### PROCESSING ########################################################## #
#find file names in a directory, regardless of type

    #create empty list for paths to each of the footprint folders
ass1_dir_list_fp = []

    #search through the footprint directory and write them into the footprint paths list
for foldername_fp in os.listdir(ass1_footprints):#for current directory, use: ('.')
    ass1_dir_list_fp.append(ass1_footprints + foldername_fp)
print(ass1_dir_list_fp)

    #create empty list for lists of scenes within each footprint
print(len(ass1_dir_list_fp)) #count footprint folders
ass1_fp_sc_list = [[] for i in range(9)] #create an empty list of lists to later list scenes per footprint
print (ass1_fp_sc_list) #test

    #extract a file list from each footprint folder and write it into the empty list of lists

list_of_Folders_with_Files = ass1_dir_list_fp

for i in range(len(list_of_Folders_with_Files)):
    list = os.listdir(list_of_Folders_with_Files[i])
    ass1_fp_sc_list[i] = list
    #print(ass1_fp_sc_list[i])
    #ass1_fp_sc_list[i] = list
    #print(list)


#for path_fp in ass1_dir_list_fp:
    #for i in range(0,len(ass1_fp_sc_list)):
       # print(ass1_fp_sc_list[i])
       # print(i)
        #print(os.listdir(path_fp))


        #print(os.listdir(path_fp))
    #print(ass1_fp_sc_list)

print (ass1_fp_sc_list)
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