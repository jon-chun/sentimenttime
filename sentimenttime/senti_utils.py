
import codecs

import string

# Map/translate punctuation to space (only for lexicon methods)
translator = str.maketrans(string.punctuation, ' '*len(string.punctuation)) 

# To tokenize raw text into sentences
import nltk
from nltk.tokenize import sent_tokenize 

# Valid range for #tokens when segmenting text by seg_len
SEG_LEN_MIN = 1
SEG_LEN_MAX = 200



def file2str(fpath):
    """[summary]: read text from file into string

    Returns:
        [string]: string of text read from filepath passed in
    """
    print('IN file2str()')
    
    try:
        with codecs.open(fpath, encoding='utf-8') as fp:
            text = fp.read()
            # print(text)
    except IOError as e:
        print(e)
    except:
        print(f"ERROR [{e}]: Cannot read file [{fpath}]")
    finally:
        print("Finally!")
        
    # print(f'Returning {text}')
    
    return text


def clean_text(text_str, senti_method='lexicon', text_type='prose'):
    """
    Given a text string, return a cleaned string by:
    0. TODO test encoding and language
    a. lowercase (only for lexicon methods) VADER/DNN use: CAPS, !!!, emojis, etc)
    b. map/translate punctuation to space (only for lexicon methods) 
    c. expand contractions
    d. correct/translate slang, misspell, repeated characters (e.g. Tweets)


    Args:
        text_str (str): [description]
    """
    
    # TODO Convert to ASCII (depends on encoding and native language of text)
    # text_clean_str = unidecode(text_str)
    
    # TODO test language of text
    
    # Special text preprocessing for Lexicon methods
    if senti_method == 'lexicon':
        
        # Lowercase if using Lexicon method
        text_clean_str = text_str.lower() 
        
        # Map/translate punctuation to a space if using Lexicon method
        text_clean_str = text_clean_str.translate(translator)

    
    # TODO Expand contractions
    # text_clean_str = contractions.fix(text_clean_str)
    
    # TODO Clean up potentially noisy text (e.g. if Twitters)
    # Remove any numbers, embedded or start/end multiple whitespaces
    text_clean_str = ' '.join([i for i in text_clean_str.split() if (~i.isdigit() & len(i) > 1)])

    return text_clean_str

def clean_segs(text_ls, senti_method='lexicon', text_type='prose'):
    """Given a list of strings, iteratively clean each one in turn

    Args:
        text_ls ([type]): [description]
        senti_method (str, optional): [description]. Defaults to 'lexicon'.
        text_type (str, optional): [description]. Defaults to 'prose'.
    """

    text_clean_ls=[]
    for a_seg in text_ls:
        a_seg_clean = clean_text(a_seg, senti_method='lexicon', text_type='prose')
        text_clean_ls.append(a_seg_clean.strip())
        
    return text_clean_ls
    
def str2segs(text_str, seg_len=0):
    """
    Given one long text string, break it intosegments according to
    seg_len=0: grammatically correct sentences
    seg_len<0: segmented by punctuation in SEG_PUNCT=[.;:-] (default)
    seg_len=n: segment into text fragments n-tokens long
    
    return an ordered list of segments as string types

    Args:
        text_str ([type]): [description]
    """
    
    if seg_len==0:
        # segment text into grammatical sentences
        sents_ls = sent_tokenize(text_str)
        sents_ls = [" ".join(a_sent.split()) for a_sent in sents_ls]
    elif seg_len < 0:
        # TODO segment text into chunks defined by SEG_PUNCT punctuation characters
        pass
    elif ((seg_len > SEG_LEN_MIN) & (seg_len<SEG_LEN_MAX)):
        # TODO segment text into chunks of size seg_len
        pass
    else:
        print(f"ERROR: illegal value for seg_len={seg_len}, valid range {SEG_LEN_MIN}-{SEG_LEN_MAX}")
        
    return sents_ls
    

def str2tokens(text_str):
    """[summary]: tokenize string and return as list of words

    Returns:
        [list]: list of tokens extracted from input string
    """
    print('IN str2tokens()')
    token_ls = text_str.split()
    # print(f'returning {token_ls}')
    return token_ls


def file2segs(fpath, lang='en', fencode=f'utf-8'):
    """
    Read and parse a text file into a list of strings where
    every string is defined by an English sentence tokenizer

    Args:
        filepath (str): path to text file to read in

    Returns:
        (list of str): list of strings, one for each line in input file
    """
    
    corpus_str = file2str('./books/cdikens_christmascarol.txt')
    corpus_ls = str2segs(corpus_str)
    
    return corpus_ls