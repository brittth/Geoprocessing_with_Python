#AssignSceneToSensor --> separate the scene path list into different lists according to their sensor
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