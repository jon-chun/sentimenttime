import glob
import os
import re

from cleantext import clean

re_title_caps = re.compile("^[A-Z]{,5}$")
re_pageno = re.compile("^[0-9(]{,3}$")
re_pageno_mess = re.compile("^[0-9()\s]{,5}$")
re_page_header1 = re.compile("^I[an\s]+M[cE\s]+.*")
re_page_header2 = re.compile("^M[achines\s]+L[ike\s]+.*$")
re_ocr_break = re.compile("^<OCR PAGE BREAK>$")

# Upto 3 lowercase words without starting CAP letter or ending punctuation
# re_few_words = re.compile("^(\w+\s+){,3}")
re_few_words = re.compile("^([a-z]+(\s)*){,3}$")  

lines_del = []
stray_char_ls = []
title_caps_ls = []
pageno_ls = []
pageno_mess_ls = []
page_header1_ls = []
page_header2_ls = []
few_words_ls = []
lines_clean = []
lines_parag_end_ls = []

# open file
with open('machines_like_me_clean.txt', 'r+') as fp_out:
    for i, aline in enumerate(fp_out):
        aline_str = aline.strip()
        
        # FUTURE: split string one embedded sentence ending punctuation (.!?), edge case embedded quotes
        
        if len(aline_str) == 0:
            # Catch empty lines
            print(f'EMPTY LINE [{i}]:')
            lines_del.append([i, aline_str, 'empty line'])

        else:
            
            print(aline_str)
            
'''            
            (len(aline_str) == 1) and not(aline_str.isnumeric()):
            if (aline_str != 'I') or (aline_str.lower() != 'a'):
                stray_char_ls.append([i, aline_str])
                # print(f'STRAY CHAR [{i}]: {aline_str}')
                lines_del.append([i, aline_str, 'stray character'])
                
        elif re.match(re_title_caps, aline_str):
            # Catch ALL CAPS titles
            title_caps_ls.append([i, aline_str])
            # print(f'RE_5CAPS [{i}]: <{aline_str}>')
            lines_del.append([i, aline_str, 'TITLE ALL CAPS'])
            
        elif re.match(re_pageno, aline_str):
            # Catch page numbers
            pageno_ls.append([i, int(aline_str)])
            # print(f'RE_PAGENO: [{aline_str}]')
            lines_del.append([i, aline_str, 'page number (normal)'])
            
        elif re.match(re_pageno_mess, aline_str):
            # Catch mangled page numbers
            pageno_mess_ls.append([i, aline_str])
            lines_del.append([i, aline_str, 'page number (mangled)'])
            
        elif re.match(re_page_header1, aline_str):
            # Catch page header21
            page_header1_ls.append([i, aline_str])
            lines_del.append([i, aline_str, 'page header #1'])
            
        elif re.match(re_page_header2, aline_str):
            # Catch page header22
            page_header2_ls.append([i, aline_str])
            lines_del.append([i, aline_str, 'page header #2'])
        
        elif re.match(re_few_words, aline_str):
            few_words_ls.append([i, aline_str])
            lines_del.append([i, aline_str, 'few ungrammatical words'])
            
        elif re.match(re_ocr_break, aline_str):
            lines_del.append([i, aline_str, 'ocr line break'])
            
        else:
            lines_clean.append(aline_str)

# close the file
fp_out.close()

# Title lines in ALL CAPS
print('Title lines in all CAPS ===========================')
for atitle in title_caps_ls:
    print(f'[{atitle[0]}]: {atitle[1]}')

# Missing page numbers
def find_missing(lst):
    page_first = int(lst[0][1])
    page_last = int(lst[-1][1])
    page_ls = [n[1] for n in lst]
    return [x for x in range(page_first, page_last+1) if x not in page_ls]
'''