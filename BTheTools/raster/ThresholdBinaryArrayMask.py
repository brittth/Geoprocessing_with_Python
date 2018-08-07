#ThresholdBinaryArrayMask --> create a binary mask based on a threshold, 1s statement fulfilled, 0s all others
    #input: array, which will be overwritte, so copy if original should be kept
    #       operator --> type as string
    #       threshold --> type as number
def ThresholdBinaryArrayMask(array, operator, threshold):
    if operator == '<':
        array[array < threshold] = 1  # replace all values <1000 with 1
    elif operator == '>':
        array[array > threshold] = 1  # replace all values <1000 with 1
    elif operator == '<=':
        array[array <= threshold] = 1  # replace all values <1000 with 1
    elif operator == '>=':
        array[array >= threshold] = 1  # replace all values <1000 with 1
    elif operator == '==':
        array[array == threshold] = 1  # replace all values <1000 with 1
    elif operator == '!=':
        array[array != threshold] = 1  # replace all values <1000 with 1
    array[array != 1] = 0  # replace all values other than 1 with 0
    #returns: overwrites input array with binary mask
    #application example:
    # arr_dem_mask = arr_dem #to be overwritten
    # ThresholdBinaryArrayMask(arr_dem_mask, "<", 1000)
    # print(arr_mask)
        #returns:
        # [[0.0 0.0 0.0 ... 0.0 0.0 0.0]
        # [0.0 0.0 0.0 ... 0.0 0.0 0.0]
        # [0.0 0.0 0.0 ... 0.0 0.0 1.0]
        # ...
        # [1.0 1.0 1.0 ... 0.0 0.0 0.0]
        # [1.0 1.0 1.0 ... 0.0 0.0 0.0]
        # [1.0 1.0 1.0 ... 0.0 0.0 0.0]]