# CompareExFilesToPotFiles --> compare number of existing files to the number of files that should exist
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