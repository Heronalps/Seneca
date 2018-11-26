import math, pdb

# array = [10,9,8,7,6,5,4,3,2,1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,30,40,50,60,70,80,90,100]
temp = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,30,40,50,60,70,80,90,100]
array = list(reversed(temp))
print(array)
start = 0
end = len(array) - 1

while (start < end):
    mid = math.floor((start + end) / 2)
    # pdb.set_trace()
    if mid == 0:
        left = array[mid]
    else:
        left = array[mid - 1]

    if mid == len(array) - 1:
        right = array[mid]
    else:
        right = array[mid + 1]

    if (left < right):
        end = mid - 1
    else:
        start = mid + 1
print(start)
print(end)
print(array[start])