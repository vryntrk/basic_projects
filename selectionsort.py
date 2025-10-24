def selection_sort(array):
    for i in range(len(array)-1):
        min_index = i
        
        for j in range(i+1, len(array)):
            if array[j] < array[min_index]:
                min_index = j
        array[i], array[min_index] = array[min_index], array[i]
    
    return array


number_list = [0, 6, 4, -8, 5, 1, -7, 9, 3, -2]
print("Original List: ", number_list)

sorted_list = selection_sort(number_list)
print("Sorted List: ", sorted_list)