import glob
import os
import re

import numpy as np
from scipy import stats
from scipy.cluster.vq import kmeans
from sklearn.cluster import KMeans
from sklearn import svm

from cleantext import clean

re_title_caps = re.compile("^[A-Z]{,5}$")
re_pageno = re.compile("^[0-9(]{,3}$")
re_pageno_mess = re.compile("^[0-9()\s]{,5}$")
re_page_header1 = re.compile("^I[an\s]+M[cE\s]+.*")
re_page_header2 = re.compile("^M[achines\s]+L[ike\s]+.*$")
re_ocr_break = re.compile("^<OCR PAGE BREAK>$")
re_hyphen_end = re.compile("^.*[^-][-]$")
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
with open('machines_like_me_all.txt', 'r+') as fp_out:
    for i, aline in enumerate(fp_out):
        aline_str = aline.strip()
        
        # FUTURE: split string one embedded sentence ending punctuation (.!?), edge case embedded quotes
        
        if len(aline_str) == 0:
            # Catch empty lines
            print(f'EMPTY LINE [{i}]:')
            lines_del.append([i, aline_str, 'empty line'])

        elif (len(aline_str) == 1) and not(aline_str.isnumeric()):
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

print('Missing page numbers ===========================')
# print(f'PAGENO_LS: [{pageno_ls}]')
pageno_miss_ls = find_missing(pageno_ls)
print(f'PAGENO_MISS_LS: [{pageno_miss_ls}]')

print('Mangled page numbers ===========================')
for aline in pageno_mess_ls:
    print(f'[{aline[0]}]: {aline[1]}')

# Page Headers1
print('Page Headers1 ===========================')
for aline in page_header1_ls:
    print(f'[{aline[0]}]: {aline[1]}')
    
# Page Headers2
print('Page Headers1 ===========================')
for aline in page_header2_ls:
    print(f'[{aline[0]}]: {aline[1]}')

# Stranded few words
print('Stranded Few Words ===========================')
for aline in few_words_ls:
    print(f'[{aline[0]}]: {aline[1]}')
    
# Stray character
print('Stray Character ===========================')
for aline in stray_char_ls:
    print(f'[{aline[0]}]: {aline[1]}')
    
    
# All lines to delete
print('SUMMARY: All lines to delete ======================================================')
for aline in enumerate(lines_del):
    print(f'Deletion #{aline[0]}: {aline[1]}')
    

# Statistics on column no of ending period (.)
line_endperiod_len_dt = {}
for i,aline in enumerate(lines_clean):
    if aline.endswith(('.', '."', '?', '?"', '!', '!"')): # or aline.endswith('."'):
        aline_len = len(aline)
        line_endperiod_len_dt[i] = aline_len
        # print(f'Clean line #{i} len={aline_len}: {aline}')



line_endperiod_len_ls = list(line_endperiod_len_dt.values())
line_endperiod_len_np = np.array(line_endperiod_len_ls)
endper_stats = stats.describe(line_endperiod_len_np)
print(endper_stats)

# https://gist.github.com/tammoippen/4474e838e969bf177155231ebba52386 
def crappyhist(a, bins=50, width=140):
    h, b = np.histogram(a, bins)

    for i in range (0, bins):
        print('{:12.5f}  | {:{width}s} {}'.format(
            b[i], 
            '#'*int(width*h[i]/np.amax(h)), 
            h[i], 
            width=width))
    print('{:12.5f}  |'.format(b[bins]))
    
crappyhist(line_endperiod_len_ls)

'''
# 1D Clustering into 2 groups with scipycluster.vq
# alt to scikit: https://github.com/dstein64/kmeans1d 

y = [float(val) for val in line_endperiod_len_ls] # [1,1,5,6,1,5,10,22,23,23,50,51,51,52,100,112,130,500,512,600,12000,12230]
x = range(len(y))
m = np.matrix([x, y]).transpose()
kclust = kmeans(m, 2)
print(kclust)
cluster_indices = kclust[0][:, 0]
print(cluster_indices)
'''

print('=====')

# 1D Clustering into 2 groups with sklearn.cluster
# https://gist.github.com/lobrien/0f95b690644a862fb4dadb73afb7753b 
data = np.array(line_endperiod_len_ls)
kmeans = KMeans(n_clusters=2).fit(data.reshape(-1,1))
kmeans.predict(data.reshape(-1,1))

print(kmeans.cluster_centers_)
decision_raw = abs(kmeans.cluster_centers_[0]-kmeans.cluster_centers_[1])
print(f'DECISION BOUNDARY: {decision_raw}')

# FUTURE: AutoML to find opt value
decision_margin = 20
decision_cut = decision_raw + decision_margin
print(f'DECISION BOUNDARY+MARGIN: {decision_cut}')

'''
# SVM Classifier 
# https://pythonprogramming.net/linear-svc-example-scikit-learn-svm-python/
# 
clf = svm.SVC(kernel='linear', C = 1.0)
# clf.fit(data) need 2d

# Hierarchical Clustering with sklearn
# https://stackabuse.com/hierarchical-clustering-with-python-and-scikit-learn
from sklearn.cluster import AgglomerativeClustering

cluster = AgglomerativeClustering(n_clusters=2, affinity='euclidean', linkage='ward')
lines_parag_end_ls = cluster.fit_predict(data.reshape(-1,1))
print(type(cluster.labels_))
print(cluster.labels_.shape)
print(len(lines_parag_end_ls))
print(len(lines_clean))
'''

'''
for i, aline in enumerate(lines_parag_end_ls):
    if aline == 0:
        print(f'PARAG ENDING LINE: {lines_clean[i]}')
    elif aline == 1:
        print(f'[NO]  PARAG ENDING LINE: {lines_clean[i]}')
    else:
        print('ERROR ----')    
        
for key, value in line_endperiod_len_dt.items():
    if aline == 0:
        print(f'PARAG ENDING LINE: {lines_clean[i]}')
    elif aline == 1:
        print(f'[NO]  PARAG ENDING LINE: {lines_clean[i]}')
    else:
        print('ERROR ----')    
'''




# Deterimine if line is end of a paragramph
lines_parag_end_ls = []
for i,aline in enumerate(lines_clean):
    if aline.endswith(('.', '."', '?', '?"', '!', '!"')): # ('.') or aline.endswith('."'):
        if len(aline) > decision_cut:
            # print(f'NOT-PARAG ENDING SENT #{i}: {aline}')
            lines_parag_end_ls.append(0)
        else:
            # print(f'    PARAG ENDING SENT #{i}: {aline}')      
            lines_parag_end_ls.append(1)
    else:
        lines_parag_end_ls.append(0)
        
        
# Rewrite file, filtering out bad lines
cur_line_ls = []
j=0
with open('machines_like_me_clean.txt', 'w+') as fp_out:
    for i,aline in enumerate(lines_clean):
        if lines_parag_end_ls[i] == 0:
            # Merge hyphenated words at end of line
            if re.match(re_hyphen_end, str(aline)):
                # print(f'line #{i} ends with hyphen: {aline}')
                cur_line_ls.append(aline[:-1])
                # print(f'     cur_line: {cur_line_ls}')
            else:
                out_line = ' '.join(cur_line_ls) + aline
                # print(f'WRITING OUT #{j}: {out_line}')
                fp_out.write(out_line)
                cur_line_ls = []
                j += 1
        elif lines_parag_end_ls[i] == 1:
            fp_out.write(aline + '\n\n')
        else:
            print('ERROR: lines_parag_end_ls is not 0/1')
            
'''
# Merge hyphenated words at end of lines
lines_dehyphenated_ls = []
for i, aline in enumerate(lines_clean):
    if aline.endswith('-'):
        # the end of the word is at the start of next line
        end = lines_clean[i+1].split()[0]
        # we remove the - and append the end of the word
        lines_dehyphenated_ls[i] = lines_clean[:-1] + end
        # and remove the end of the word and possibly the 
        # following space from the next line
        lines[num+1] = lines[num+1][len(end)+1:]

text = '\n'.join(lines)
'''