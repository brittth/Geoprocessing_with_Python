#Group I: Random Sampling
    #1) Get one PA
    #2) transform to UTM
    #3) Get extent of PA
    #4) Random Point within extent based on starting point
    #5) Check if point within borders of PA (not extent)
    #6) Check if point has min x meters distance to nearest border
    #7) Check if x-coord. >= 90m
    #       else check if |y-coord| >= 90m
    #   --> both false, start again
    #   --> one TRUE save list