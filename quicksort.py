def quick_sort(array):
    if len(array) <= 1:
        return array
    
    pivot = array[0]
    lower = []
    greater = []

    for x in array:
        if x < pivot:
            lower.append(x)
        elif x > pivot:
            greater.append(x)
    
    return quick_sort(lower) + [pivot] + quick_sort(greater)


number_list = [7, 5, 2, 4, 0, 3, 9, 1, 6, 8]
print("Original List: ", number_list)

sorted_array = quick_sort(number_list)
print("Sorted List: ", sorted_array)