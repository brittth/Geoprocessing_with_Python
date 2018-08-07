import os

#GetLandsatFileSuffixes --> create lists for Landsat sensor typical file endings
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