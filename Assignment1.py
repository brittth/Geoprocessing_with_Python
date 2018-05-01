# ####################################### LOAD REQUIRED LIBRARIES ############################################# #
'''
import time
import ogr
import baumiTools as bt
'''
import os
import re

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
# EXERCISE I - 1)
#create empty lists for names of and paths to each of the footprint folders
foldername_fp_list =[]
dir_list_fp = []

#search through the footprint directory and write them into the footprint paths list
    #find file names in a directory, regardless of type
for foldername_fp in os.listdir(footprints):#for current directory, use: ('.')
    foldername_fp_list.append(foldername_fp)
    dir_list_fp.append(footprints + foldername_fp)
#print(foldername_fp_list)
#print(dir_list_fp) #list of footprint paths (path_fp)
'''
#count scenes per sensor for each footprint
for path_fp in dir_list_fp:
    #print(os.listdir(path_fp))
    ls5 = re.compile("^LT05")
    ls7 = re.compile("^LE07")
    ls8 = re.compile("^LC08")
    L5 = filter(ls5.match, os.listdir(path_fp))
    L7 = filter(ls7.match, os.listdir(path_fp))
    L8 = filter(ls8.match, os.listdir(path_fp))
    print("For footprint " + str(path_fp[-7:]) + ", there are " + str(len(list(L5))) + " Landsat 5, " + str(len(list(L7))) + " Landsat 7 and " + str(len(list(L8))) + " Landsat 8 scenes.")
'''


# EXERCISE I - 2) - a)
#create a complete path list to each scene irrespective of footprint (list of lists)
foldername_sc_list =[]
dir_list_sc = []
for path_fp in dir_list_fp:
    for foldername_sc in os.listdir(path_fp):
        dir_list_sc.append(path_fp + "/" + foldername_sc)
#print (dir_list_sc)

#check maximum number of files per scene directory
no_files = []
for scene_dir in dir_list_sc:
    file_list = os.listdir(scene_dir)
    #print (file_list)
    no_files = len(file_list)
    #print(no_files)
    #ls5 = re.compile("^LT05")
    #ls7 = re.compile("^LE07")
    #ls8 = re.compile("^LC08")
    #L5 = filter(ls5.match, scene_dir)
    #L7 = filter(ls7.match, scene_dir)
    #L8 = filter(ls8.match, scene_dir)



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

# ####################################### TEMPLATES ########################################################## #
''' #DYSFUNCIONAL
# find number of subdirectories in a directory, folders only
for x in os.listdir(ass1_footprints):
    if os.path.isdir(x):
        ass1_dir_list = [ass1_footprints + x]
    else: continue
    print(ass1_dir_list)
'''

'''
#create empty list for lists of scenes within each footprint
fp_sc_list = []

#extract a file list from each footprint folder and write it into the empty list
for path_fp in dir_list_fp:
    for foldername_fp in foldername_fp_list:
        foldername_fp =[]
        foldername_fp.append(os.listdir(path_fp))
    fp_sc_list.append(foldername_fp[0]) #the 0 is only to get rid of double brackets
print(fp_sc_list)
print(len(fp_sc_list))
'''

'''
#working template for regular expressions
mylist = ["dog", "cat", "wildcat", "thundercat", "cow", "hooo"]
r = re.compile(".*cat")
newlist = filter(r.match, mylist)
print (list(newlist))
'''

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