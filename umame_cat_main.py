#written by Jared Arzate
import sys
import os
import defs
sys.path.append(defs.func_dir)
sys.path.append(defs.in_dir)

import generic_functions as gf
import umame_functions   as uf
import numpy as np
from   pathlib import Path


def main():
    print(f"using",defs.out_dir,"as output path.")
    print(f"and",defs.in_dir,"as input path.")

    path,data_dir,output_dir,output_file = gf.get_input()

    ####
    print("enter number of temps")
    num_temps = int(input())
    print("enter number of iterations")
    num_iters = int(input())

    print("\nenter the column indeces to extract.")
    print("as a tuple: ")
    in_str=input()
    indeces = tuple((int(in_str[1]), int(in_str[3]),  int(in_str[5])) )

    label = uf.parse_filename_umame()
    ##### cat all files
    master_x = np.zeros((num_temps,num_iters))
    master_y = np.zeros((num_temps,num_iters))
    master_z = np.zeros((num_temps,num_iters))
    print("parsing file contents...")
    iter_val = 0 #will be incremented to access all files
    temp_val = 0 #will be incremented to access all files
    for i in range(num_temps):
        temp_to_append = str(temp_val)
        while len(temp_to_append) < 7: temp_to_append = '0' + temp_to_append

        for j in range(num_iters):
            #assumes your inputting the file name correctly...
            iter_to_append = str(iter_val)
            while len(iter_to_append) < 5: iter_to_append = '0' + iter_to_append
            file_name = label + temp_to_append + "_" + iter_to_append + ".txt" 
            print(file_name)
            file_path = path / file_name
            master_x[i,j] = np.average(np.genfromtxt(file_path,skip_header=1,usecols=indeces[0]))
            master_y[i,j] = np.average(np.genfromtxt(file_path,skip_header=1,usecols=indeces[1]))
            master_z[i,j] = np.average(np.genfromtxt(file_path,skip_header=1,usecols=indeces[2]))
            #next file, if exists
            iter_val += 1 
        temp_val += 1
        iter_val = 0

    x = np.transpose(gf.order_data(master_x.flatten(),num_temps,num_iters))
    y = np.transpose(gf.order_data(master_y.flatten(),num_temps,num_iters))
    z = np.transpose(gf.order_data(master_z.flatten(),num_temps,num_iters)) 

    gf.write_out(output_dir, output_file, x,y,z,indeces)

if __name__ == "__main__":
    main()
