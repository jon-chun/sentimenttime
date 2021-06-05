import glob
import os
import re
import string

# SymSpellpy

import contractions
import pkg_resources
from symspellpy import SymSpell, Verbosity
import symspellpy 

sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt")
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

# from cleantext import clean

re_1They = re.compile("^.*1 hey.*$")
re_1The = re.compile("^.*1 he.*}$")
re_1I = re.compile("^.* 1 .*")

"""
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
"""

def ocr_correct(string, replacements, ignore_case=False):
    """
    Given a string and a replacement map, it returns the replaced string.

    :param str string: string to execute replacements on
    :param dict replacements: replacement dictionary {value to find: value to replace}
    :param bool ignore_case: whether the match should be case insensitive
    :rtype: str

    Source:  multireplace() from https://gist.github.com/bgusach/a967e0587d6e01e889fd1d776c5f3729
    Discuss: https://stackoverflow.com/questions/6116978/how-to-replace-multiple-substrings-of-a-string 
    """
    # If case insensitive, we need to normalize the old string so that later a replacement
    # can be found. For instance with {"HEY": "lol"} we should match and find a replacement for "hey",
    # "HEY", "hEy", etc.
    if ignore_case:
        def normalize_old(s):
            return s.lower()

        re_mode = re.IGNORECASE

    else:
        def normalize_old(s):
            return s

        re_mode = 0

    replacements = {normalize_old(key): val for key, val in replacements.items()}
    
    # Place longer ones first to keep shorter substrings from matching where the longer ones should take place
    # For instance given the replacements {"ab": "AB", "abc": "ABC"} against the string "hey abc", it should produce
    # "hey ABC" and not "hey ABc"
    rep_sorted = sorted(replacements, key=len, reverse=True)
    rep_escaped = map(re.escape, rep_sorted)
    
    # Create a big OR regex that matches any of the substrings to replace
    pattern = re.compile("|".join(rep_escaped), re_mode)
    
    # For each match, look up the new string in the replacements, being the key the normalized old string
    return pattern.sub(lambda match: replacements[normalize_old(match.group(0))], string)


# open file
err_ct = 0
err_var_ct = 0
with open("machines_like_me_clean.txt", "r+") as fp_in:
    for i, aline in enumerate(fp_in):
        # Strip leading/trailing whitespace
        aline_str = aline.strip()
        
        # Correct common OCR errors (Longer/more specific match rule first)
        ocr_errors_dt = {" 1* inally "  : " Finally ",
                         " winter s "   : " winter's ",
                         " 1 here's "   : " There's ",
                         " didn t " : " did not",
                         " T here " : " There ",
                         " I here " : " There ",
                         " 1 hird " : " Third ",
                         " wwhile " : " wwhile ",
                         "wwhile "  : "While ",
                         " I irst"  : " First",
                         " 1 hey "  : " They ",
                         " 1 his "  : " This ",
                         " W hat "  : " What ",
                         " 1 he "   : " The ", 
                         " I he "   : " The ",
                         " J he "   : " The ",
                         " cenI "   : " Then I ",
                         "d'you "   : "do you ",
                         "pered "   : "Whispered ",
                         " I m "    : " I'm ",
                         " 1 m "    : " I'm ",
                         " 1 d "    : " I'd ",
                         "hile "    : "While ",
                         "\ou "     : "You ",
                         " und "    : " and ",
                         " I V "    : " IV ",
                         " 1 V "    : " IV ",
                         ". ur "    : ". Your ",
                         ". 1 "     : ". I ",
                         " ur "     : " Your ",
                         " 1 "      : " I ",
                         " T "      : " I ",
                         " n "      : " In ",
                         " V "      : " by ",
                         "1 "       : "I "} 
        aline_ocr_str = ocr_correct(aline_str, ocr_errors_dt)
        
        # Expand contractions
        aline_exp_str = contractions.fix(aline_ocr_str)
        
        # Lowercase
        
        # aline_exp_str.translate(str.maketrans("", "", string.punctuation))
        aline_clean_str = aline_exp_str # re.sub(r"[^\w\s]", " ", aline_exp_str)

        if (i>=2000) and (i<3000):
            # Process each line one at a time
            # print(f"BEFORE ALINE #{i}: {aline_str}")
            words_ls = aline_clean_str.lower().split()
            for aword in words_ls:
                # Process each word within a line one at a time
                
                # Strip out punctuation
                aword_nopunct = re.sub(r"[^\w\s]", "", aword).strip()
                # aword_nopunct = aword.translate(str.maketrans('', '', string.punctuation))
                # input_term = aword.translate(str.maketrans('', '', string.punctuation))
                input_term = aword_nopunct
                
                # Spell Check 
                suggestions = sym_spell.lookup(input_term, Verbosity.CLOSEST, max_edit_distance=1)
                # print(f"{aword}: {suggestions}")
                for suggestion in suggestions:
                    #Consider each spell correction in order of priority
                    err_ct += 1
                    asuggestion = suggestion
                    edit_word, edit_dist, edit_no = str(asuggestion).split(",")
                    if int(edit_dist) > 0:
                        err_var_ct += 1
                        print(f"   Line #{i} INCORRECT {aword} => {edit_word}, EDIT_DIST: {edit_dist}, EDIT_NO: {edit_no}")
                        # print(f"     SUGGESTIONS")
                    else:
                        # print(f"CORRECT: {edit_word}")
                        pass
                    
            # print(f"AFTER ALINE #{i}: {aline_clean_str}")    
        # print(f"LINE #{i}: {aline}")
        
    print(f'Total Error Count: {err_ct}, Total Error Variation Count: {err_var_ct}')
    