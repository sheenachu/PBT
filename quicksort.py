#Quicksorting algorithm to create ranking list
#
#Created by Kevin Bernat 3/8/2016
#Modified from http://interactivepython.org/runestone/static/pythonds/SortSearch/TheQuickSort.html
# Median of Three method was implemented independently, using the following
# as a reference: http://stackoverflow.com/questions/24533359/implementing-the-quick-sort-with-median-of-three

import statistics
from random import randint
import sys

#This is used so that the maximum recursion limit is not reached
sys.setrecursionlimit(100000)

def median_of_three(first,middle,last):
    """
    Takes the first element, last element and middle element of a list
    and returns the median value
    """

    median_value = statistics.median([first,middle,last])
    return median_value


def quick_sort(l,left_index,right_index):
    """
    Splits the list based on the partition location from new_partition.
    Recursion stops once the left and right index meet.
    """
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
    """
    Performs an index swap between two numbers in a list l
    """

    temp = l[index1]
    l[index1] = l[index2]
    l[index2] = temp

def new_partition(l,left_index,right_index,current_left,current_right):
    """
    Determines where the new partition in the list should be made. If no 
    split is done, it continues swapping between indices that are out
    of order.
    """
    #start off with the pivot as the first element of the list
    pivot = l[left_index]   
    swapping = True
    if current_left >= current_right:
        #get new pivot
        middle = int(len(l[left_index:right_index])/2)
    
        pivot = median_of_three(l[current_left],l[middle],l[current_right])
        #need to swap the pivot to the beginning of the partitioned list
        swap(l,l.index(pivot),left_index)

    current_left = left_index
    current_right = right_index
    while swapping:

        while current_left <= current_right and l[current_left] <= pivot: 
            current_left += 1

        while l[current_right] >= pivot and current_right >= current_left:
            current_right -= 1

        if current_right < current_left: #split point found!
            swapping = False
            

        else:
            # perform swap with left and right
            swap(l,current_left, current_right)
            return new_partition(l, left_index, right_index, current_left+1,current_right-1)
    
    swap(l,left_index, current_right)
    return current_right

#if __name__=="__main__":

#    l=[]
#    for element in range(10000):
#        l.append(randint(0,100))
#    print(l)
#    x = quick_sort(l,0,len(l)-1)
#    print(x)

