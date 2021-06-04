# Concate Each File separated with a <OCR BREAK> marker
'''
import glob

files = glob.glob('.\FN*.txt')

print(f'FILES: {files} \n TYPE: {type(files)}')

import os
dir_name = '.'
# Get list of all files in a given directory sorted by name
list_of_files = sorted( filter( lambda x: os.path.isfile(os.path.join(dir_name, x)),
                        os.listdir(dir_name) ) )
for file_name in list_of_files:
    print(file_name)
'''
    
import glob
import os

from cleantext import clean

pages_all = []

dir_name = './'
# Get list of all files in a given directory sorted by name
list_of_files = sorted(filter(os.path.isfile, glob.glob(dir_name + 'FN-*.txt') ) )
# Iterate over sorted list of files and print the file paths 
# one by one.
for file_path in list_of_files:
    with open(file_path, 'r') as fp_in:
        file_str = fp_in.read()
        # print(f'FILE_STR: {file_lines_ls}')
        file_str += '\n<OCR PAGE BREAK>\n'
        pages_all.append(file_str)
    # print(file_path) 

  
# open file
with open('machines_like_me_all.txt', 'w+') as fp_out:
      
    # write elements of list
    for apage in pages_all:
       fp_out.write(f'{clean(apage, lower=False)}\n')
      
    print("File written successfully")
  
  
# close the file
fp_out.close()


# append lines with a few words 
# Remove all Headers/Page Numbers after <OCR BREAK>s
#   May be misspelt 'Ian McEw a n' 
#   Is page number always on line #2 (no)!

# If last line ends with hyphen '-', then join and delete <OCR BREAK>

# If last line ends without a sentence ending punctuation [.!?], then join and delete <OCR BREAK>


# Check if end of line/begin of next line are word fragments 
#   Page 2 Co/rny, 

# Insert (2)\nl Paragraph breaks where

