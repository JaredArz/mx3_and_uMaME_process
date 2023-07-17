import os
import sys
import defs
sys.path.append(defs.in_dir)
sys.path.append(defs.out_dir)
import re
from pathlib import Path
import numpy as np

def handle_run_arg():
    try:
        sys.argv[1]
    except(IndexError):
        print("please rerun script with either -mx3 or -umame flag, exiting.")
        exit()
    mu_arg = sys.argv[1]
    if (sys.argv[1] != "-mx3" and sys.argv[1] != "-umame"):
        print("invalid flag, exiting.")
        exit()
    return mu_arg

def write_out(w_dir, w_file, x,y,z, indeces) -> None:
    w_dir = Path(defs.out_dir) / w_dir
    w_file = w_file + "_np.txt"
    if not os.path.exists(w_dir):
        os.makedirs(w_dir)
    w_path = w_dir/w_file
    f = open(w_path, "a")
    _ = (x,y,z)
    for i in range(len(indeces)):
        f.write("#"+ "columns: " + str(indeces) + "\n")
        np.savetxt(f, _[i], fmt='%.18e', delimiter=' ', newline = '\n')
        #f.write(str(i) + " = " + np.savetxt(f,data[i], fmt='%.18e', delimiter=' ', newline = '\n') + "\n")
    f.close()

def get_input():
    print("enter name of file dir")
    r_dir = input()
    _ = Path(defs.in_dir) 
    r_path = _/r_dir
    print("enter output dir: ")
    w_dir = input()
    print("enter output file: ")
    w_file = input()
    return r_path,r_dir,w_dir,w_file 



# parses columns of tables one at a time
#
# inputs: file_name, dir, and column of data to retrieve
# returns: column of table data
def get_column_from_file(path_to_open,column_num):
    column = []
    with open(path_to_open) as table_file:
        for line in enumerate(table_file):
            line_index = line[0]
            line = line[1]
            line.rstrip()
            row = line.split()
            if line_index == 0:
                continue
            column.append(row[column_num])
    return(column)


# return number of cells switched from positive to negative magnetization in the x direction
#
# inputs: cell data for each file
# returns: number cells switched each file
def get_num_switches(cell_data_files):
    switches_each_file = []
    for cell_data in cell_data_files:
        switches = 0
        for mx in cell_data:
            if (float(mx) < 0):
                switches += 1
        switches_each_file.append(switches)
    return(switches_each_file)


def order_data(unordered_data,major,minor) -> np.ndarray:
    ordered = []
    select = lambda i,j : unordered_data[i + j*minor]
    for i in range(minor):
        current = []
        for j in range(major):
            current.append( select(i,j) )
        ordered.append(current)
    return np.array(ordered)

def list_to_float(arr):
    try: 
        return ([float(elem) for elem in arr])
    except(TypeError):
        return ( [[float(elem) for elem in nested_arr ] for nested_arr in arr ] )
