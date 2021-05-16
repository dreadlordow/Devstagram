def merge_sort(arr):
    m = len(arr) // 2
    left = arr[:m]
    right = arr[m:]

    merge_sort(left)
    merge_sort(right)

    sorted()