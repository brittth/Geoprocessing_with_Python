# ####################################### FUNCTIONS ########################################################## #

#separate the scene path list into different lists according to their sensor
    #directory_list --> list of scene paths
    #search_term --> term that identifies folder as scene of certain sensor (eg. "LT04" for Landsat 4)
    #output_list_name --> name of the PREVIOUSLY CREATED list to which to append the search results
def AssignSceneToSensor (directory_list, search_term, output_list_name):
    for scene_directory in directory_list:
        if search_term in scene_directory:
            output_list_name.append(scene_directory)
    #returns: no print, but saves the result in the given output_list_name
        #application example:
        #dir_list_L4 = []
        #AssignSceneToSensor(dir_list_sc, "LT04", dir_list_L4)

#create lists for Landsat sensor typical file endings
#print((os.listdir(dir_list_L4[1])[1])[40:]) #check were relevant string ending starts --> 40
def GetLandsatFileSuffixes(directory_list, output_list_name):
    for scene in directory_list:                    #takes each scene folder from the directory list
        for file in os.listdir(scene):              #for each file in the scene folder
            output_list_name.append((file[40:]))    #cut off the first 40 characters, as they are the scene name, and write the left over suffixes into the output list
    #returns: no print, but saves the result in the given output_list_name
        #application example (Landsat 4):
            #file_endings_L4 = []  # empty text_file to write the file ending list
            #GetLandsatFileSuffixes(dir_list_L4, file_endings_L4)
            #file_endings_L4 = set(file_endings_L4) #to have each suffix only once in the list
            #print(file_endings_L4) #for illustration
                #returns:
                # {'.xml', '_sr_band5.tif', '_radsat_qa.tif', '_sensor_azimuth_band4.tif', '_GCP.txt', '_VER.jpg', '_solar_azimuth_band4.tif',
                # '_MTL.txt', '_sr_band3.tif', '_solar_zenith_band4.tif', '_sr_band1.tif', '_pixel_qa.tif', '_VER.txt', '_ANG.txt', '_sr_band4.tif',
                # '_sr_atmos_opacity.tif', '_sr_band2.tif', '_sr_band7.tif', '_sensor_zenith_band4.tif', '_bt_band6.tif', '_sr_cloud_qa.tif'}


#create template files list for each sensor and lists of actual files present
    #directory_list
    #file_suffix_list
    #output_list_name_exfiles
    #output_list_name_potfiles
def CreateLandsatFilesTemplate(directory_list,file_suffix_list,output_list_name_exfiles,output_list_name_potfiles,):
    for scene_path in directory_list:
        files_scene = (os.listdir(scene_path))      #list of actual files present per scene
        scene_name = files_scene[1][:40]            #gather the prefix for the endings
        output_list_name_exfiles.extend(files_scene) #with each iteration add existing file to file list
        for ending in file_suffix_list:
            output_list_name_potfiles.append(((str(scene_name))+ ending))#creates template list of all files that should exist
    #returns: no print, but saves the result in the given output_list_name_exfiles and output_list_name_potfiles
        # application example (Landsat 4):
            # files_L4=[] #for template list
            # actual_files_L4 = [] #for actually existing files
            # CreateLandsatFilesTemplate(dir_list_L4,file_endings_L4,actual_files_L4,files_L4)
            # print(len(files_L4))
            # print(len(actual_files_L4))
            # print(actual_files_L4)
                #returns:
                # 252
                # 251
                # ['LT04_L1TP_229077_19830812_20170220_01_T1.xml', 'LT04_L1TP_229077_19830812_20170220_01_T1_ANG.txt',
                # 'LT04_L1TP_229077_19830812_20170220_01_T1_bt_band6.tif', 'LT04_L1TP_229077_19830812_20170220_01_T1_GCP.txt',
                # 'LT04_L1TP_229077_19830812_20170220_01_T1_MTL.txt', 'LT04_L1TP_229077_19830812_20170220_01_T1_pixel_qa.tif',
                # 'LT04_L1TP_229077_19830812_20170220_01_T1_radsat_qa.tif', 'LT04_L1TP_229077_19830812_20170220_01_T1_sensor_azimuth_band4.tif',
                # ...]

# compare number of existing files to the number of files that should exist
    #layer_list --> list of layer names (i.e. without suffixes)
    #suffix_list --> list of data type suffixes (incl. name attachements)
    #missing_files_list --> previously empty list, will be list of missing files
    #incomplete_layers_list --> previously empty list, will be list of incomplete layers
    #existing_files --> list of existing files of the same type (vector/raster)
    #output_list_name--> previously empty list, will be complete list of files of that type (vector/raster) that should exist
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
    #returns: printed sentences with results
        #application example:
            # vector_files = []  # complete list of vector files that should exist
            # diff_v_list=[] #list of missing files
            # diff_v_list_name = [] #list of incomplete layers
            # CompareExFilesToPotFiles(vector_layers,vector_endings,diff_v_list,diff_v_list_name,vector_existing_files,vector_files)
                #returns:
                # There are 8 file(s) missing from 4 vector layer(s).
                # The incomplete vector layers are: {'DEM_Humboldt_aspect', 'Veg_AsRaster_30m', 'DEM_Humboldt', 'DEM_Humboldt_slope'}

# ####################################### TEMPLATES ########################################################## #

#count scenes per sensor for each folder (ex. footprint)
import os #list directories
import re #use regular expressions
    #dir_list_fp is a list of footprint paths (path_fp)
    #folder structure is footprint(ex. 228_077)--> scene(ex. LT052280772011102901T1)
    # for each footprint folder find the number of scenes for each sensor
    # here only sensors: Landsat 4, 5, 7 and 8 have been used
    #"^..." --> substring to be found
for path_fp in dir_list_fp:
    L4 = filter((re.compile("^LT04")).match, os.listdir(path_fp))   #re.compile() to set search term, .match to look for search term, os.lissir(path_fp) represent search location
    L5 = filter((re.compile("^LT05")).match, os.listdir(path_fp))
    L7 = filter((re.compile("^LE07")).match, os.listdir(path_fp))
    L8 = filter((re.compile("^LC08")).match, os.listdir(path_fp))
    print("For footprint " + str(path_fp[-7:]) + ", there are " + str(len(list(L4))) + " Landsat 4, " + str(len(list(L5))) + " Landsat 5, " + str(len(list(L7))) + " Landsat 7 and " + str(len(list(L8))) + " Landsat 8 scenes.")
    #returns:
    #For footprint 228_077, there are 0 Landsat 4, 309 Landsat 5, 282 Landsat 7 and 82 Landsat 8 scenes.
    #For footprint 228_078, there are 0 Landsat 4, 310 Landsat 5, 280 Landsat 7 and 81 Landsat 8 scenes.
    #...


#create path list for folders irrespective of parent folder by concatenating path of parent folders with the folder
    #application here: create a complete path list to each scene irrespective of footprint (list of lists)
    #foldername_sc_list --> list of foldernames (ex. scenes) from all parent folders (ex. footprints)
    #dir_list_sc --> desired output: list of all path to the folders (ex. scenes)
    #dir_list_fp --> list of parent folders (ex. footprints)
foldername_sc_list =[]
dir_list_sc = []
for path_fp in dir_list_fp:
    for foldername_sc in os.listdir(path_fp):
        dir_list_sc.append(path_fp + "/" + foldername_sc)   #path and folder concatenated by '/'
print (dir_list_sc)
    #returns:
    #['D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 2 - IDE, debugger, first scripts/Assignment01_data/Part01_Landsat/228_077/LC082280772013042501T1',
    # 'D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 2 - IDE, debugger, first scripts/Assignment01_data/Part01_Landsat/228_077/LC082280772013051101T1',
    # ...,
    # 'D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 2 - IDE, debugger, first scripts/Assignment01_data/Part01_Landsat/228_078/LT052280782011102901T1',
    # 'D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 2 - IDE, debugger, first scripts/Assignment01_data/Part01_Landsat/228_079/LC082280792013051101T1',
    # ...]


#check for missing files in list of folder directories/paths based on the maximum number of files present in any of those folders
    #check maximum number of files per scene directory
        #dir_list_L4 --> list of Landsat 4 scene directories/paths
no_file_L4 = []
for scene_dir in dir_list_L4:
    no_file_L4.append(len(os.listdir(scene_dir)))
print("The maximum number of files in a Landsat 4 scene is " + str(max(no_file_L4)) + " and the minimum is " + str(min(no_file_L4)) + ".")
        #returns:
        # The maximum number of files in a Landsat 4 scene is 21 and the minimum is 20.
    #count the number of scenes with files missing
no_corrupt_sc_L4 = (sum(i < (max(no_file_L4)) for i in no_file_L4))
print("There are " + str(no_corrupt_sc_L4) + " Landsat 4 scene(s) with files missing.")
        #returns:
        # There are 1 Landsat 4 scene(s) with files missing.



#print keys and values in dictionary
dict = {"A":"Hello","B":"Hey","C":"Hi","D":"What's up?"}
for key in dict:
    print(key)
    print(dict[key])



# ####################################### unsorted TEMPLATES ########################################################## #

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
''' #Splitting a Path into All of Its Parts, not tested but might be useful
import os, sys
def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts
    '''