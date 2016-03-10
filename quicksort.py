#Quicksorting algorithm to create ranking list
#
#Created by Kevin Bernat 3/8/2016
#Modified from http://interactivepython.org/runestone/static/pythonds/SortSearch/TheQuickSort.html

import statistics
from random import randint


def median_of_three(l):

    median_value = statistics.median([l[0],l[int(len(l)/2)],l[-1]])
    return median_value


def quick_sort(l,left_index,right_index):
    if left_index < right_index:
        current_left = 0
        current_right = len(l)-1
        pivot = new_partition(l,left_index,right_index,current_left,current_right)

        #left partition
        quick_sort(l,left_index,pivot-1)
        #right partition
        quick_sort(l,pivot+1,right_index)

    return l    

def swap(l,index1,index2):

    temp = l[index1]
    l[index1] = l[index2]
    l[index2] = temp

def new_partition(l,left_index,right_index,current_left,current_right):

    pivot = l[left_index]

    current_left = left_index + 1
    current_right = right_index
    #print(left_index)
    #random = randint(0,right_index)
    #pivot = l[random]

    while current_left <= current_right and l[current_left] <= pivot: 
        current_left += 1

    while l[current_right] >= pivot and current_right >= current_left:
        current_right -= 1

    if current_right < current_left: #split point found!
        swap(l,left_index, current_right)
        return current_right

    else:
        # perform swap with left and right
        swap(l,current_left, current_right)
        return new_partition(l, left_index, right_index, current_left+1,current_right-1)



