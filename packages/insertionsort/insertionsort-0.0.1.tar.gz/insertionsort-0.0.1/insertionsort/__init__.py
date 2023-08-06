# SKONCZONE

import random
import time

class Element:
    def __init__(self,data,priority):
        self.__data = data
        self.__priority = priority

    def __repr__(self):
        text = f"{self.__priority}:{self.__data}"
        return text

    def __lt__(self, other):
        return self.__priority < other.__priority
    
    def __gt__(self,other):
        return self.__priority > other.__priority
    
    def __le__(self,other):
        return self.__priority <= other.__priority

def insertion_sort(table):
    size = len(table)
    tab = table.copy()
    for i in range(1,size):
        curr_value = tab[i]
        j = i - 1
        while j >= 0 and tab[j] > curr_value:
            tab[j+1] = tab[j]
            j -= 1
        tab[j+1] = curr_value
    return tab

def shell_sort(table,h_function = lambda x: x//2):
    size = len(table)
    h = size//2
    tab = table.copy()
    while h > 0:
        for idx in range(h):
            i = idx
            while i < size:
                j = i - h
                curr_elem = tab[i]
                while j >= 0 and tab[j] > curr_elem:
                    tab[j + h] = tab[j]
                    j -= h
                tab[j+h] = curr_elem
                i += h
        h = h_function(h) if h != 1 else -1
    return tab
                    
         
def insertion_stability_test(test):
    to_sort = [Element(el[1],el[0]) for el in test]
    sorted = insertion_sort(to_sort)
    print(sorted)

def shell_stability_test(test):
    to_sort = [Element(el[1],el[0]) for el in test]
    sorted = shell_sort(to_sort)
    print(sorted)
    

    
