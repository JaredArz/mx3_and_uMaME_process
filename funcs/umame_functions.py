#umame data processing functions.
#Jared Arzate, 2023

import re
import numpy as np
import generic_functions as gf
from pathlib import Path

# this function will parse out the string (file label) ) prefixing the number corresponding to each file
# this is for get_cell_data() so that it can increment the files number then reconstruct a valid file name
#
#inputs:  none
#returns: file label
def parse_filename_umame():
    print("enter the name of the first data file in the sequence (output_foo_bar_000.txt)")
    print("will fail if \"foo_bar\" has zeroes in it :)")
    starting_file_name=input()

    #match everything until the substring 0 is encountered
    _ = re.match('.+?(?=0)', starting_file_name)                                    
    label = _.group()

    return label

#get xyz data for single cell, that is, go through output files in dir and get first line
def get_switch_data_umame(label,path):
    #run until there is not a file corresponding to the current file number
    #this will be triggered by a FileNotFoundError exception
    file_number = 0 #will be incremented to access all files
    cell_data_each_file = []
    print("parsing file contents...")
    print("function assumes were looking at first column for mx.")
    while(True):
        #assumes your inputting the file name correctly...
        file_number_to_append = str(file_number)
        while len(file_number_to_append) < 7: file_number_to_append = '0' + file_number_to_append
        file_name = label + file_number_to_append + ".txt" 
        file_path = path / file_name
        if (file_path.exists() is False):
            print("file contents collected")
            return(cell_data_each_file)
        else:
            #hardcoded 0 index assuming mx is column 0
            column = gf.get_column_from_file(file_path,0)
            mx_cells = []
            for elem in enumerate(column):
                elem_index = elem[0]
                elem = elem[1]
                if elem_index == 0:
                    #skip first row since that is text
                    continue
                mx = float(elem)
                mx_cells.append(mx)
            cell_data_each_file.append(mx_cells)
            #next file, if exists
            file_number += 1 
