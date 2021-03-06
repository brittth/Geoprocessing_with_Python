# ####################################### LOAD REQUIRED LIBRARIES ############################################# #
'''
import ogr
import baumiTools as bt
'''
import time
import os
import re

# ####################################### SET TIME-COUNT ###################################################### #

starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")

# ####################################### FOLDER PATHS & global variables ##################################### #

footprints = "D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 2 - IDE, debugger, first scripts/Assignment01_data/Part01_Landsat/"
GIS_path = "D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 2 - IDE, debugger, first scripts/Assignment01_data/Part02_GIS-Files"
output_path = "D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 2 - IDE, debugger, first scripts/"

# ####################################### PROCESSING ########################################################## #

# EXERCISE I - 1)
print("QUESTION 1\n")
#create empty lists for names of and paths to each of the footprint folders
foldername_fp_list =[]
dir_list_fp = []

#search through the footprint directory and write footprint folders into the footprint paths list
    #find file names in a directory, regardless of type
for foldername_fp in os.listdir(footprints):#for current directory, use: ('.')
    foldername_fp_list.append(foldername_fp)
    dir_list_fp.append(footprints + foldername_fp)
#print(foldername_fp_list) #list of footprint folder names
#print(dir_list_fp) #list of footprint paths (path_fp)

#count scenes per sensor for each footprint
for path_fp in dir_list_fp:
    L4 = filter((re.compile("^LT04")).match, os.listdir(path_fp))
    L5 = filter((re.compile("^LT05")).match, os.listdir(path_fp))
    L7 = filter((re.compile("^LE07")).match, os.listdir(path_fp))
    L8 = filter((re.compile("^LC08")).match, os.listdir(path_fp))
    print("For footprint " + str(path_fp[-7:]) + ", there are " + str(len(list(L4))) + " Landsat 4, " + str(len(list(L5))) + " Landsat 5, " + str(len(list(L7))) + " Landsat 7 and " + str(len(list(L8))) + " Landsat 8 scenes.")



# EXERCISE I - 2) - a)
print("\nQUESTION 2\n")
#create a complete path list to each scene irrespective of footprint (list of lists)
foldername_sc_list =[]
dir_list_sc = []
for path_fp in dir_list_fp:
    for foldername_sc in os.listdir(path_fp):
        dir_list_sc.append(path_fp + "/" + foldername_sc)
#print (dir_list_sc)

#separate the scene path list into different lists according to their sensor
def AssignSceneToSensor (directory_list, search_term, output_list_name):
    for scene_directory in directory_list:
        if search_term in scene_directory:
            output_list_name.append(scene_directory)

dir_list_L4 = []
AssignSceneToSensor(dir_list_sc, "LT04", dir_list_L4)
dir_list_L5 = []
AssignSceneToSensor(dir_list_sc, "LT05", dir_list_L5)
dir_list_L7 = []
AssignSceneToSensor(dir_list_sc, "LE07", dir_list_L7)
dir_list_L8 = []
AssignSceneToSensor(dir_list_sc, "LC08", dir_list_L8)

#check maximum number of files per scene directory
no_file_L4 = []
no_file_L5 = []
no_file_L7 = []
no_file_L8 = []
for scene_dir in dir_list_L4:
    no_file_L4.append(len(os.listdir(scene_dir)))
#print("The maximum number of files in a Landsat 4 scene is " + str(max(no_file_L4)) + " and the minimum is " + str(min(no_file_L4)) + ".") #files missing somewhere
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
no_corrupt_sc_L4 = (sum(i < (max(no_file_L4)) for i in no_file_L4))
print("There are " + str(no_corrupt_sc_L4) + " Landsat 4 scene(s) with files missing.")
no_corrupt_sc_L5 = (sum(i < (max(no_file_L5)) for i in no_file_L5))
print("There are " + str(no_corrupt_sc_L5) + " Landsat 5 scene(s) with files missing.")
no_corrupt_sc_L7 = (sum(i < (max(no_file_L7)) for i in no_file_L7))
print("There are " + str(no_corrupt_sc_L7) + " Landsat 7 scene(s) with files missing.")
no_corrupt_sc_L8 = (sum(i < (max(no_file_L8)) for i in no_file_L8))
print("There are " + str(no_corrupt_sc_L8) + " Landsat 8 scene(s) with files missing.")



# EXERCISE I - 2) - b)
print("\nQUESTION 3\n")
#create a file list for each sensor to compare with actual files present

#create lists for sensor typical file endings
#print((os.listdir(dir_list_L4[1])[1])[40:]) #check were relevant string ending starts --> 40
def GetLandsatFileSuffixes(directory_list, output_list_name):
    for scene in directory_list:
        for file in os.listdir(scene):
            output_list_name.append((file[40:]))

file_endings_L4 = [] #empty text_file to write the file ending list
GetLandsatFileSuffixes(dir_list_L4, file_endings_L4)
file_endings_L4 = set(file_endings_L4)
#print(file_endings_L4) #file list for L4
#print((len(file_endings_L4))==(max(no_file_L4)))#check by comparing with maximum number of files per scene for L4 --> TRUE

file_endings_L5 = []
GetLandsatFileSuffixes(dir_list_L5, file_endings_L5)
file_endings_L5 = set(file_endings_L5)
#print(file_endings_L5) #file list for L5
#print((len(file_endings_L5))==(max(no_file_L5)))#check by comparing with maximum number of files per scene for L5 --> TRUE

file_endings_L7 = []
GetLandsatFileSuffixes(dir_list_L7, file_endings_L7)
file_endings_L7 = set(file_endings_L7)
#print(file_endings_L7) #file list for L7
#print((len(file_endings_L7))==(max(no_file_L7)))#check by comparing with maximum number of files per scene for L7 --> TRUE

file_endings_L8 = []
GetLandsatFileSuffixes(dir_list_L8, file_endings_L8)
file_endings_L8 = set(file_endings_L8)
#print(file_endings_L8) #file list for L8
#print((len(list(file_endings_L8)))==(max(no_file_L8)))#check by comparing with maximum number of files per scene for L8 --> TRUE


#create template files list for each sensor and lists of actual files present
def CreateLandsatFilesTemplate(directory_list,file_suffix_list,output_list_name_exfiles,output_list_name_potfiles,):
    for scene_path in directory_list:
        files_scene = (os.listdir(scene_path))      #list of actual files present per scene
        scene_name = files_scene[1][:40]            #gather the prefix for the endings
        output_list_name_exfiles.extend(files_scene) #with each iteration add existing file to file list
        for ending in file_suffix_list:
            output_list_name_potfiles.append(((str(scene_name))+ ending))#creates template list of all files that should exist

files_L4=[] #for template list
actual_files_L4 = [] #for actually existing files
CreateLandsatFilesTemplate(dir_list_L4,file_endings_L4,actual_files_L4,files_L4)

files_L5=[]
actual_files_L5 = []
CreateLandsatFilesTemplate(dir_list_L5,file_endings_L5,actual_files_L5,files_L5)

files_L7=[]
actual_files_L7 = []
CreateLandsatFilesTemplate(dir_list_L7,file_endings_L7,actual_files_L7,files_L7)

files_L8=[]
actual_files_L8 = []
CreateLandsatFilesTemplate(dir_list_L8,file_endings_L8,actual_files_L8,files_L8)


# check difference between template and actual file lists
text_file_filename = [] #empty list for corrupt files
text_file = [] #empty list for corrupt file paths
diff4 = lambda files_L4,actual_files_L4: [x for x in files_L4 if x not in actual_files_L4]
diff5 = lambda files_L5,actual_files_L5: [x for x in files_L5 if x not in actual_files_L5]
diff7 = lambda files_L7,actual_files_L7: [x for x in files_L7 if x not in actual_files_L7]
diff8 = lambda files_L8,actual_files_L8: [x for x in files_L8 if x not in actual_files_L8]

text_file_filename.extend(diff4(files_L4,actual_files_L4)+ diff5(files_L5,actual_files_L5)+ diff7(files_L7,actual_files_L7)+ diff8(files_L8,actual_files_L8))

for element in text_file_filename: #reconstructing path name (footprint/scene/file) from the file name
    dir_name = element.replace("_","") #no underscore in directory name
    dir_name = dir_name.replace("L1TP", "") #product identification should not go into directory name
    dir_name = dir_name[:30] #shorter directory name
    dir_name = dir_name.replace(dir_name[18:27], "")#shorter directory name
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
print("\nQUESTION 4\n")
#separate vector from raster data
GIS_files = os.listdir(GIS_path)

#find typical endings knowing only shp for vector and tif for raster
vector_files_shp =[]            #file names with endings
vector_files_shp_names =[]      #file names without endings
vector_endings = []

raster_files =[]            #file names with endings
raster_files_names =[]      #file names without endings
raster_endings = []

for file in GIS_files:              #for each GIS file
    if ".shp" in file:              #look for the ones containing ".shp"
        vector_files_shp_names.append(file.split(".")[0]) #list only vector file names (of those where the shp exists) without ending

for file in vector_files_shp_names: #find the elements of vector_files_shp in GIS_files to get other file endings
    for long_file in GIS_files:
        if file in long_file:
            vector_files_shp.append(long_file.split(".")) #split strings at "."

for list in vector_files_shp:   #merge multi-part-endings
    list.pop(0)# remove first element on each list, i.e. file name
    vector_endings.append("." +'.'.join(list))
print("Each vector layer should be made up by the following file types: " + str(set(vector_endings)))

vector_endings_matt = ['.shp', '.shx', '.dbf', '.prj']
print("Matthias: Each vector layer should be made up by the following file types: " + str(vector_endings_matt))

    #THE SAME FOR RASTER
for file in GIS_files:              #for each GIS file
    if ".tif" in file:              #look for the ones containing ".shp"
        raster_files_names.append(file.split(".")[0]) #list only raster file names (of those where the tif exists) without ending

for file in raster_files_names: #find the elements of raster_files in GIS_files to get other file endings
    for long_file in GIS_files:
        if file in long_file:
            raster_files.append(long_file.split(".")) #split strings at "."

for list in raster_files:   #merge multi-part-endings
    list.pop(0)# remove first element on each list, i.e. file name
    raster_endings.append("." +'.'.join(list))
print("\nEach raster layer should be made up by the following file types: " + str(set(raster_endings)))

#list all vector files and all raster files
vector_existing_files = []
vector_existing_files_name = []
vector_layers = []          #unique layer names

raster_existing_files = []
raster_existing_files_name = []
raster_layers = []          #unique layer names

for ending in set(vector_endings):  #write all files with the typical vector file endings into list, clip ending to create unique layer name list
    for file in GIS_files:
        if ending in file:
            vector_existing_files.append(file)
            if ".tif.vat.dbf" in file:  # avoid counting ".tif.vat.dbf" (raster ending) as ".dbf" (vector ending)
                vector_existing_files.remove(file)
for file in vector_existing_files:
    vector_existing_files_name.append(file.split(".")[0])

vector_existing_files = set(vector_existing_files) #get rid of duplicates due to multi-part-endings
vector_layers = set(vector_existing_files_name)
#print("Vector layers: " + str(vector_layers))
print("\nThere are " + str(len(vector_layers)) + " vector layer(s) in this folder.")

for ending in set(raster_endings):  #write all files with the typical raster file endings into list, clip ending tocreate unique layer name list
    for file in GIS_files:
        if ending in file:
            raster_existing_files.append(file)
            raster_existing_files_name.append(file.split(".")[0])
raster_existing_files = set(raster_existing_files)#get rid of duplicates due to multi-part-endings
raster_layers = set(raster_existing_files_name)
#print("Raster layers: " + str(raster_layers))
print("There are " + str(len(raster_layers)) + " raster layer(s) in this folder.")



# EXERCISE II - 2)
print("\nQUESTION 5 & QUESTION 6")
# compare number of existing files to the number of files that should exist
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

vector_files = []  # complete list of vector files that should exist
diff_v_list=[] #list of missing files
diff_v_list_name = [] #list of incomplete layers
CompareExFilesToPotFiles(vector_layers,vector_endings,diff_v_list,diff_v_list_name,vector_existing_files,vector_files)

#for Matthias shp-endings
vector_endings_matt = ['.shp', '.shx', '.dbf', '.prj']
vector_files_matt = [] #complete list of vector files that should exist
diff_v_list_matt = []  # list of missing files
diff_v_list_name_matt = []  # list of incomplete layers
#CompareExFilesToPotFiles(vector_layers,vector_endings_matt,diff_v_list_matt,diff_v_list_name_matt,vector_existing_files,vector_files_matt)
for layer in vector_layers:
    for ending in set(vector_endings_matt):
        vector_files_matt.append(layer + ending)
diff_v_matt = lambda vector_files_matt, vector_existing_files: [x for x in vector_files_matt if x not in vector_existing_files]
diff_v_list_matt.extend(diff_v_matt(vector_files_matt, vector_existing_files))  # missing files written into list
for file in diff_v_list_matt:
    diff_v_list_name_matt.append(file.split(".")[0])  # endings removed to only get the layers
diff_v_list_name_matt = set(diff_v_list_name_matt)  # reduced to unique layer names
# "set()" for removing duplicates from multiple identification of multi-part-endings
print("\nMatthias: There are " + str(len(diff_v_list_name_matt)) + " vector layer(s) with file(s) missing.")
print("Matthias: The incomplete vector layers are: " + str(diff_v_list_name_matt))

raster_files = []  # complete list of vector files that should exist
diff_r_list=[] #list of missing files
diff_r_list_name = [] #list of incomplete layers
CompareExFilesToPotFiles(raster_layers,raster_endings,diff_r_list,diff_r_list_name,raster_existing_files,raster_files)



#print("\nQUESTION 6 \n")
#print("The incomplete vector layers are: " + str(diff_v_list_name))
#print("\nMatthias: The incomplete vector layers are: " + str(diff_v_list_name_matt))
#print("\nThe incomplete raster layers are: " + str(diff_r_list_name))

#write the incomplete  into a txt file
outF1 = open("text_file1.txt", "w") #create new txt file
for line in diff_v_list_name: # write list into txt file
  outF1.write(line)
  outF1.write("\n")
outF1.close()

#for Matthias shp-endings
outF1_matt = open("text_file1_matt.txt", "w") #create new txt file
for line in diff_v_list_name_matt: # write list into txt file
  outF1_matt.write(line)
  outF1_matt.write("\n")
outF1_matt.close()

# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #

print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")