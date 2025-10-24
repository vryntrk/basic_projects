def bubble_sort(array):
    for _ in range(len(array)):
        for i in range(len(array)-1):
            if array[i] > array[i+1]:
                array[i], array[i+1] = array[i+1], array[i]

    return array


number_list = [7, 3, 8, 2, 0, 4, 1, 6, 9, 5]
print("Original List: ", number_list)

sorted_list = bubble_sort(number_list)
print("Sorted List: ", sorted_list)
