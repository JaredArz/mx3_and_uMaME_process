
import re
from pathlib import Path

############################### switch stuff. dont touch, kinda jank ###############################

# this function will read all the ovf files present in an user-input defined directory
# and extract the total run times and all the cell data from each
#
# inputs:  data label
# returns: two parallel arrays corresponding to each file number — run times and cell data
def get_switch_data_mx3(label,path):
    ####################### ovf parser ######################### 
    #run until there is not a file corresponding to the current file number
    #this will be triggered by a FileNotFoundError exception
    file_number = 0 #will be incremented to access all files
    cell_data_each_file = []
    print("parsing file contents...")
    while(True):
        #format file name (foobar000000.ovf), try opening file"
        file_number_to_append = str(file_number)
        while len(file_number_to_append) < 6: file_number_to_append = '0' + file_number_to_append
        file_name = label + file_number_to_append + ".ovf" 
        file_to_open = data_folder / file_name
        if(file_to_open.exists() is False):
            print("file contents collected")
            return(cell_data_each_file)
        else:
            ovf_file = open(file_to_open)
            #go line by line and pick out the desired data points
            cell_data = []
            for line in ovf_file:
                #matches if line is not commented (cell data lines)
                if not(re.match("^#", line)):
                    cell_data.append(line)
            #compile cell data for this file to list
            cell_data_each_file.append(cell_data)
            ovf_file.close()
            #next file, if exists
            file_number += 1 


############################### end switch  ##########################################


# this function will parse out the string prefixing the file number, deemed the data label,
# because parse_file_contents() will increment the file number then need to reconstruct a valid file name
#
#inputs:  none
#returns: data label
def parse_filename_mx3():
    print("enter the name of the first data file in the sequence (foobar000000.ovf)")
    starting_file_name = input()
    
  #match everything until the substring 000000 is encountered
    _ = re.match('.+?(?=000000)', starting_file_name)                                    
    label = _.group()

    return label
