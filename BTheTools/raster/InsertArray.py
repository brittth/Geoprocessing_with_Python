import numpy as np

def InsertArray(insertion_array, window_size):
    arr = np.zeros(1000*1000).reshape(1000,1000)
    arr[int((window_size-1)/2):int(((window_size-1)/2)+(1000-window_size+1)), int((window_size-1)/2):int(((window_size-1)/2)+(1000-window_size+1))] = insertion_array
    return arr