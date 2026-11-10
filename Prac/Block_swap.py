# Python3 code for above implementation

# Wrapper over the recursive function leftRotateRec()
# It left rotates arr by d.


''' UTILITY FUNCTIONS '''
''' function to print an array '''


def printArray(arr, size):
    for i in range(size):
        print(arr[i], end=" ")
    print()


'''
 * This function swaps d elements starting at 
 * index fi with d elements starting at index si
 '''


def swap(arr, fi, si, d):
    for i in range(d):
        temp = arr[fi + i]
        arr[fi + i] = arr[si + i]
        arr[si + i] = temp


def leftRotate(arr, d, n):
    if(d == 0 or d == n):
        return
    i = d
    j = n - d
    while (i != j):

        if(i < j):  # A is shorter
            swap(arr, d - i, d + j - i, i)
            j -= i

        else:  # B is shorter
            swap(arr, d - i, d, j)
            i -= j

    swap(arr, d - i, d, i)


    # Driver Code
if __name__ == '__main__':
    arr = [1, 2, 3, 4, 5, 6, 7]
    leftRotate(arr, 3, 7)
    printArray(arr, 7)