#Group I: Random Sampling
    #1) Get one PA
    #2) transform to EPSG 3035
    #3) Get extent of PA
    #4) Random Point within extent based on starting point (multitude of 30m)
    #5) Check if point within borders of PA (not extent)
    #6) Check if point has min x meters distance to nearest border
    #7) Check if x-coord. >= 90m
    #       else check if |y-coord| >= 90m
    #   --> both false, start again
    #   --> one TRUE save list1
    # while loop stopping at 50 entries

#Group II: Building the pixels
    # 9 Boxes by adding ad subtracting from given center points
    # add ID field for each 9 pixels and for each 9-pixel-box

#Group III: Coordinate system and shapefiles
    # EPSG 3035 because it is in meters