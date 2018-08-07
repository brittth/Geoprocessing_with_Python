import os

#CreateLandsatFilesTemplate --> create template files list for each sensor and lists of actual files present
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