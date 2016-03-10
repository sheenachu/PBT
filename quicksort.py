#Quicksorting algorithm to create ranking list
#
#Created by Kevin Bernat 3/8/2016
#Modified from http://interactivepython.org/runestone/static/pythonds/SortSearch/TheQuickSort.html

import statistics
from random import randint


def median_of_three(first,middle,last):

    #median_value = statistics.median([l[0],l[int(len(l)/2)],l[-1]])
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

    pivot = l[left_index]   

    current_left = left_index + 1
    current_right = right_index

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

if __name__=="__main__":

    l=[]
    for element in range(10):
        l.append(randint(0,100))
    print(l)
    x = quick_sort(l,0,len(l)-1)
    print(x)

    #random = randint(0,right_index)
    #pivot = l[random]
    #print(l[current_left:current_right])

    #if current_left >= current_right:
        #get new pivot


    #    if len(l[current_left:current_right])%2 ==0:
    #        middle = int(len(l[current_left:current_right])/2)
    #    else:
    #        middle = int(len(l[current_left:current_right])/2)

    
    #print(l[current_left],l[middle],l[current_right])
    
        #pivot = median_of_three(l[current_left],l[middle],l[current_right])
    
    #print("full list ",l)

        #swap(l,l.index(pivot),current_left)
    #print(pivot)
    #pivot = l[current_left] 