import sys
import os
import defs
sys.path.append(defs.func_dir)
from   pathlib import Path
import numpy as np
from dataclasses import dataclass
import generic_functions as gf

'''
@dataclass
class simulation:
    name       : str
    output_dir : str
    shape      : str
    def __str__(self):
        return self.name

sims = {0 : simulation("test sim", "test","2,2"),
        1 : None
        }
'''
def main():

    print(f"using",defs.out_dir,"as output path.")
    print(f"and",defs.in_dir,"as input path.")

    #FIXME: function use never debugged, may be a few stray bugs in this file teehee
    path, data_dir,file_name,output_dir,output_file = gf.get_input()

    print("reshape using...")
    print("np     : 0")
    print("lambda : 1 ...?")
    usr_n_l = int(input())
    if usr_n_l == '0':
        print("enter length axis 0")
        s1 = int(input())
        print("enter length axis 1")
        s2 = int(input())
    else:
        print("enter major iteration val: ")
        major = int(input())
        print("enter minor iteration val: ")
        minor = int(input())

    print("\nenter the column indeces to extract.")
    print("as a tuple: ")
    in_str=input()
    indeces = tuple((int(in_str[1]), int(in_str[3]),  int(in_str[5])) )

    columns = np.genfromtxt(path, skip_header=1,usecols=indeces)
    
    #FIXME may need to debug shape option
    if usr_n_l == '0':
        x = (columns[:,0])[0:-1].reshape(s1,s2)
        y = (columns[:,1])[0:-1].reshape(s1,s2)
        z = (columns[:,2])[0:-1].reshape(s1,s2)
    else:
        x = np.transpose(gf.order_data(columns[:,0],major,minor))
        y = np.transpose(gf.order_data(columns[:,1],major,minor))
        z = np.transpose(gf.order_data(columns[:,2],major,minor))

    d_path = Path(defs.outdir/output_dir)
    gf.write_out(d_path, output_file,x,y,z,indeces)



if __name__ == "__main__":
    main()
