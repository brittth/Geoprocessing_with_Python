import numpy as np

def CalculateSHDI2Array(slices,cat_list,windows_size, message_string):
    def CalculateSHDI(category_list, slice_arr):
        # write occurrences of all categories into a dictionary
        unique, counts = np.unique(slice_arr, return_counts=True)
        allcat_dict = dict(zip(unique, counts))
        # write occurrences of all RELEVANT categories into a dictionary
        sum_dict = {}
        for cat in category_list:
            if cat in allcat_dict:
                sum_dict.update({cat: allcat_dict[cat]})
        allcat_sum = sum(sum_dict.values())
        # calculate proportion of each RELEVANT category
        result = []
        for cat in cat_list:
            if cat in allcat_dict:
                prop = (allcat_dict[cat] / allcat_sum)
                # print('Proportion of Category ' + str(cat) + ': ' + str(prop))
                # define SHDI function: SHDI = −SUM[m,i=1] (Pi*lnPi)
                value = (prop * np.log(prop))
                result.append(value)
        shdi = (-1) * sum(result)
        print('SHDI: ', shdi)
        return shdi

    def Chunks(l, n):
        # For item i in a range that is a length of l,
        for i in range(0, len(l), n):
            # Create an index range for l of n items:
            yield l[i:i + n]

    counter = 0
    shdi_list =[]
    for i in slices: #if loop directly in function above, then error
        counter += 1
        print(message_string)
        print('\nSlice #',counter,':')
        shdi = CalculateSHDI(cat_list,slices[i])
        shdi_list.append(shdi) #save shdi values in list
    # divide shdi_list into chucks of certain length
    shdi_chunks = list(Chunks(shdi_list, (1000 - windows_size + 1)))  # list of lists with values
    print('SHDI Lists in chunks created with chunk length of ', len(shdi_chunks), '.')
    # convert shdi_chunks into an array
    shdi_arr = np.asarray(shdi_chunks)
    print('The SHDI array has a shape of:', shdi_arr.shape)
    print('The SHDI array has the data type: ', shdi_arr.dtype)
    return shdi_arr