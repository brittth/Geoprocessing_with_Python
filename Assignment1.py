# ####################################### LOAD REQUIRED LIBRARIES ############################################# #
'''
import time
import ogr
import baumiTools as bt
'''
import os
import re
import glob

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

#count scenes per sensor for each footprint
for path_fp in dir_list_fp:
    #print(os.listdir(path_fp))
    ls5 = re.compile("^LT05")
    ls7 = re.compile("^LE07")
    ls8 = re.compile("^LC08")
    L5 = filter(ls5.match, os.listdir(path_fp))
    L7 = filter(ls7.match, os.listdir(path_fp))
    L8 = filter(ls8.match, os.listdir(path_fp))
    #print("For footprint " + str(path_fp[-7:]) + ", there are " + str(len(list(L5))) + " Landsat 5, " + str(len(list(L7))) + " Landsat 7 and " + str(len(list(L8))) + " Landsat 8 scenes.")



# EXERCISE I - 2) - a)
#create a complete path list to each scene irrespective of footprint (list of lists)
foldername_sc_list =[]
dir_list_sc = []
for path_fp in dir_list_fp:
    for foldername_sc in os.listdir(path_fp):
        dir_list_sc.append(path_fp + "/" + foldername_sc)
#print (dir_list_sc)

#separate the scene path list into different lists depending according to their sensor
dir_list_L5 = []
dir_list_L7 = []
dir_list_L8 = []
for scene_dir in dir_list_sc:
    if "LT05" in scene_dir:
        dir_list_L5.append(scene_dir)
    if "LE07" in scene_dir:
        dir_list_L7.append(scene_dir)
    if "LC08" in scene_dir:
        dir_list_L8.append(scene_dir)
#print(dir_list_L5)
#print(dir_list_L7)
#print(dir_list_L8)

#check maximum number of files per scene directory
no_files_L5 = []
no_files_L7 = []
no_files_L8 = []
for scene_dir in dir_list_L5:
    no_files_L5.append(len(os.listdir(scene_dir)))
print("The maximum number of files in a Landsat 5 scene is " + str(max(no_files_L5)) + " and the minimum is " + str(min(no_files_L5)) + ".") #no files missing anywhere
for scene_dir in dir_list_L7:
    no_files_L7.append(len(os.listdir(scene_dir)))
print("The maximum number of files in a Landsat 7 scene is " + str(max(no_files_L7)) + " and the minimum is " + str(min(no_files_L7)) + ".") #files missing somewhere
for scene_dir in dir_list_L8:
    no_files_L8.append(len(os.listdir(scene_dir)))
print("The maximum number of files in a Landsat 8 scene is " + str(max(no_files_L8)) + " and the minimum is " + str(min(no_files_L8)) + ".") #files missing somewhere

#count the number of scenes with files missing
no_corrupt_sc_L7 = (sum(i < (max(no_files_L7)) for i in no_files_L7))
print("There are " + str(no_corrupt_sc_L7) + " Landsat 7 scene(s) with files missing.")
no_corrupt_sc_L8 = (sum(i < (max(no_files_L8)) for i in no_files_L8))
print("There are " + str(no_corrupt_sc_L8) + " Landsat 8 scene(s) with files missing.")


'''
dir_to_search = '/some/path/to/images/' #dir_list_sc
files_in_dir = glob.glob("{}{}".format(dir_to_search,'*.jpg'))
list_of_files = ['1.jpg','2.jpg','3.jpg']
missing_files = [x for x in list_of_files if x not in files_in_dir]
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