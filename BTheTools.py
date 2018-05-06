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

#print keys and values in dictionary
dict = {"A":"Hello","B":"Hey","C":"Hi","D":"What's up?"}
for key in dict:
    print(key)
    print(dict[key])