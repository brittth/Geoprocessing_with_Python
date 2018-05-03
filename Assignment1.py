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
output_path = "D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 2 - IDE, debugger, first scripts/"
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
no_file_L5 = []
no_file_L7 = []
no_file_L8 = []
for scene_dir in dir_list_L5:
    no_file_L5.append(len(os.listdir(scene_dir)))
#print("The maximum number of files in a Landsat 5 scene is " + str(max(no_file_L5)) + " and the minimum is " + str(min(no_file_L5)) + ".") #no files missing anywhere
for scene_dir in dir_list_L7:
    no_file_L7.append(len(os.listdir(scene_dir)))
#print("The maximum number of files in a Landsat 7 scene is " + str(max(no_file_L7)) + " and the minimum is " + str(min(no_file_L7)) + ".") #files missing somewhere
for scene_dir in dir_list_L8:
    no_file_L8.append(len(os.listdir(scene_dir)))
#print("The maximum number of files in a Landsat 8 scene is " + str(max(no_file_L8)) + " and the minimum is " + str(min(no_file_L8)) + ".") #files missing somewhere

#count the number of scenes with files missing
no_corrupt_sc_L7 = (sum(i < (max(no_file_L7)) for i in no_file_L7))
#print("There are " + str(no_corrupt_sc_L7) + " Landsat 7 scene(s) with files missing.")
no_corrupt_sc_L8 = (sum(i < (max(no_file_L8)) for i in no_file_L8))
#print("There are " + str(no_corrupt_sc_L8) + " Landsat 8 scene(s) with files missing.")


# EXERCISE I - 2) - a)
#create a file list for each sensor to compare with actual files present
#print((os.listdir(dir_list_L5[1])[1])[40:]) #check were relevant string ending starts --> 40
#print((os.listdir(dir_list_L7[1])[1])[40:])
#print((os.listdir(dir_list_L8[1])[1])[40:])
file_endings_L5 = [] #empty text_file to write the file list
file_endings_L7 = []
file_endings_L8 = []
for scene in dir_list_L5:
    #print((os.listdir(scene)))
    for file in os.listdir(scene):
        file_endings_L5.append((file[40:]))
file_endings_L5 = set(file_endings_L5)
#print(file_endings_L5) #file list for L5
#print((len(file_endings_L5))==(max(no_file_L5)))#check by comparing with maximum number of files per scene for L5 --> TRUE
for scene in dir_list_L7:
    #print((os.listdir(scene)))
    for file in os.listdir(scene):
        file_endings_L7.append((file[40:]))
file_endings_L7 = set(file_endings_L7)
#print(file_endings_L7) #file list for L7
#print((len(file_endings_L7))==(max(no_file_L7)))#check by comparing with maximum number of files per scene for L7 --> TRUE
for scene in dir_list_L8:
    #print((os.listdir(scene)))
    for file in os.listdir(scene):
        file_endings_L8.append((file[40:]))
file_endings_L8 = set(file_endings_L8)
#print(file_endings_L8) #file list for L8
#print((len(list(file_endings_L8)))==(max(no_file_L8)))#check by comparing with maximum number of files per scene for L8 --> TRUE

#create template files list for each sensor and lists of actual files present
files_L5=[] #for template list
files_L7=[]
files_L8=[]
actual_files_L5 = [] #for actually existing files
actual_files_L7 = []
actual_files_L8 = []
for scene_path in dir_list_L5:
    files_scene = (os.listdir(scene_path)) #list of actual files present per scene
    scene_name = files_scene[1][:40] #gather the prefix for the endings
    actual_files_L5 = actual_files_L5 + (files_scene) #store each existing file in a L5 file list, add to list with each iteration
    for ending in file_endings_L5:
        files_L5.append(((str(scene_name))+ ending)) #creates template list of all files that should exist
for scene_path in dir_list_L7:
    files_scene = (os.listdir(scene_path)) #list of actual files present per scene
    scene_name = files_scene[1][:40] #gather the prefix for the endings
    actual_files_L7 = actual_files_L7 + (files_scene) #store each existing file in a L5 file list, add to list with each iteration
    for ending in file_endings_L7:
        files_L7.append(((str(scene_name))+ ending)) #creates template list of all files that should exist
for scene_path in dir_list_L8:
    files_scene = (os.listdir(scene_path)) #list of actual files present per scene
    scene_name = files_scene[1][:40] #gather the prefix for the endings
    actual_files_L8 = actual_files_L8 + (files_scene) #store each existing file in a L5 file list, add to list with each iteration
    for ending in file_endings_L8:
        files_L8.append(((str(scene_name))+ ending)) #creates template list of all files that should exist

# check difference between template and actual file lists
text_file_filename = [] #empty list for corrupt files
text_file = [] #empty list for corrupt file paths
diff5 = lambda files_L5,actual_files_L5: [x for x in files_L5 if x not in actual_files_L5]
diff7 = lambda files_L7,actual_files_L7: [x for x in files_L7 if x not in actual_files_L7]
diff8 = lambda files_L8,actual_files_L8: [x for x in files_L8 if x not in actual_files_L8]

text_file_filename.extend(diff5(files_L5,actual_files_L5)+ diff7(files_L7,actual_files_L7)+ diff8(files_L8,actual_files_L8))

for element in text_file_filename: #reconstructing path name (footprint/scene/file) from the file name
    dir_name = element.replace("_","") #no underscore in directory name
    dir_name = dir_name.replace("L1TP", "") #product identification should not go into directory name
    dir_name = dir_name[:30] #shorter directory name
    dir_name = dir_name.replace(dir_name[18:26], "")#shorter directory name
    footprint_name= dir_name[4:10]
    footprint_name = footprint_name[:3] + "_" + footprint_name[3:]
    element = (footprints + footprint_name + "/" + dir_name + "/" + element) #build element path
    text_file.append(element)
print(text_file)

#write the missing files into a txt file
outF = open("text_file.txt", "w") #create new txt file
for line in text_file: # write list into txt file
  outF.write(line)
  outF.write("\n")
outF.close()



# EXERCISE II - 1)

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