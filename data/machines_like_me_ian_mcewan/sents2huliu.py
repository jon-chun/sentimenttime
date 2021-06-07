import sys
import re
import csv

import pandas as pd

import pyreadr

# ALT: !wget raw leixcon files direct from sentimentr repo
#      https://github.com/trinker/lexicon/tree/master/data 
# https://github.com/trinker/lexicon/tree/master/data 

# Convert local lexicon.rda files to python dict
# JOCKERS_RINKER_PATH = './lexicons/hash_sentiment_jockers_rinker.rda'
# jockers_rinker_dt = pyreadr.read_r(JOCKERS_RINKER_PATH)

# done! let's see what we got
# print(jockers_rinker_dt) # let's check what objects we got
# df1 = jockers_rinker_dt["df1"] # extract the pandas data frame for object df1

LEXICON_PATH = './lexicons/hash_sentiment_huliu.csv'
OUT_SENTIMENTS_CSV = "mlm_sentiment_senticnet.csv"

lexicon_dt = {}

def get_lexicon(sa_lexicon='default'):
    """
    Read in sentiment analysis lexicon specificed by sa_lib
    into appropriate global variable
    1. lexicon_dt[word] = <value>

    Args:
        sa_lib (str, optional): [description]. Defaults to 'syuzhet'.
    """
    
    if (sa_lexicon == 'default'):
        lexicon_df = pd.read_csv(LEXICON_PATH)
        lexicon_df.columns = ['index_no', 'word', 'polarity']
        lexicon_df.drop(['index_no'], axis=1, inplace=True)
        lexicon_df.dropna(inplace=True)
        lexicon_dt = lexicon_df.set_index('word').T.to_dict('list')
        # unlist the polarity to type: float
        for key in lexicon_dt:
            lexicon_dt[key] = float(lexicon_dt[key][0])
        
    ### print(f"Exit get_sa_lex() with {len(lexicon_dt.keys())} entries in syuzhet_dt")
    return lexicon_dt

lexicon_dt = get_lexicon()


def word2sa(word_str, sa_lib='syuzhet'):
    """
    Given a single word string and sentiment analysis
    lexical library, return the sentiment value normed
    to -1 to 1

    Args:
        word_str ([type]): [description]
        sa_lib (str, optional): [description]. Defaults to 'syuzhet'.
    """
    
    return word_str


def sent2lex_sa(text, lexicon_path='default', lang='en'):
    """
    Given a sentence in the form of a string:
    1.
    2. Tokenize into individual words
    3. Calculate Sentiment values for each word in context
        a. VADER
        b. BERT
    4. Calculate Sentiment value for entire sentence

    Args:
        sent_str (str: [description]
        lang (str, optional): [description]. Defaults to 'en'.
        sa_lib (str, optional): [description]. Defaults to 'syuzhet'.

    Returns:
        float: sum of sentiment values for each word in sentence
    """

    # TODO test if matching lexicon is loaded for selected sentiment
    #      method, if not, automatically load the appropraite lexicon
    #      from the data file/internet or give instructions on how to

    if lexicon_path == 'default':
        pass
    else:
        lexicon_path = get_lexicon(lexicon_path)

    ### print(f"in sent2lex with text of type {type(text)}, text = {text}")
    
    # Remove all not alphanumeric and whitespace characters
    text = re.sub(r'[^\w\s]', '', text) 
    
    # Check valid input types
    # if (~isinstance(text, str)):  # (type(text) == str):  #  (~isinstance(text, str)):
    #     print(f"ERROR: sent2lex_sa() only takes type str not type {type(text)}: {text}")
        
    # TODO Check for dirty text, auto refer to clean_text
        
    # Check for empty/null strings
    text = text.strip().lower()
    if (len(text) < 1):
        print("ERROR: sent2lex_sa() given empty/null string")
    
    # Preprocess text (e.g. lowercase, etc)
    # text = clean_text(text)
    ### print(f"In sent2lex_sa with text= {text}")
    
    seg_sa_fl = 0.0
    
    # if (sa_lexicon == 'syuzhet'):
    for a_word in text.split():
        ### print(f"looking up the word: {a_word}")
        # print(syuzhet_dt['harry'])
        try:
            word_sa_fl = float(lexicon_dt[a_word])
            seg_sa_fl = seg_sa_fl + word_sa_fl
            print(f"{a_word} has a sentiment value of {word_sa_fl}")
        except TypeError: # KeyError:
            # a_word is not in lexicon so it adds 0 to the sentence sa sum
            print(f"TypeError: cannot convert {lexicon_dt[a_word]} to float")
            continue
        except KeyError:
            # print(f"KeyError: missing key {a_word} in defaultdict syuzhet_dt")
            continue
        except:
            e = sys.exc_info()[0]
            print(f"ERROR {e}: sent2lex_sa() cannot catch a_word indexing into syuzhet_dt error")
    
    ### print(f"Leaving sent2lex_sa() with sentence sa value = {str(seg_sa_fl)}")
    
    return seg_sa_fl

    
def clean_sent(astring):
    # Lowercase
    astring_lower = astring.lower()
    
    astring_final = astring_lower    
    return astring_final

get_lexicon()

lineno = 0
corpus_lineno_ls = []
corpus_sents_ls = []
sentiment_syuzhet_ls = []
with open("mlm_sentences.txt", "r+") as fp_in:
    for i, aline in enumerate(fp_in):
        # Strip leading/trailing whitespace
        aline_str = aline.strip()
        if len(aline_str) == 0:
            pass
        else:
            # Number each sentence
            lineno += 1
            corpus_lineno_ls.append(lineno)
            # Clean each sentence
            sent_clean_str = clean_sent(aline_str)
            # print(f'Adding sent #{i}: {sent_clean_str}')
            corpus_sents_ls.append(sent_clean_str)

            # Evaluate sentiment of each sentence
            sy_sentiment = sent2lex_sa(sent_clean_str)
            # print("VADER Sentiment {:-<65} {}".format(sent_clean_str, str(vs)))
            # print(f"VADER Compound Sentiment: {vs_compound}")
            sentiment_syuzhet_ls.append(sy_sentiment)

with open(OUT_SENTIMENTS_CSV, "w", newline='', encoding='utf-8') as fp_out:
    writer = csv.writer(fp_out, delimiter=',')
    writer.writerows(zip(corpus_lineno_ls, sentiment_syuzhet_ls, corpus_sents_ls))

