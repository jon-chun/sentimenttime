import sys
import csv
import re

SYUZHET_FN = './data/syuzhet_dict.csv'

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
        with open(SYUZHET_FN, newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames='word')
            for i, row in enumerate(reader):
                # print(f"reading syuzhet row {i} with row: {row}")
                lexicon_dt[row['o']] = row['r']
            print(f"just read in {len(lexicon_dt.keys())} words into syuzhet_dt of type {type(lexicon_dt)}")
    else:
        print("ERROR: Only read syuzhet_dict for now")
        
    print(f"exit get_sa_lex() with {len(lexicon_dt.keys())} entries in syuzhet_dt")
    return lexicon_dt
    

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


def sent2lex_sa(text, lexicon_dt='default', lang='en'):
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

    if lexicon_dt == 'default':
        lexicon_dt = get_lexicon('./data/syuzhet_dict.csv')

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
    
    print(f"Leaving sent2lex_sa() with sentence sa value = {str(seg_sa_fl)}")
    
    return seg_sa_fl
            
"""
    if (sa_lexicon == 'bing'):
        # Simple lexical approach
        emo_ls = word2emo('todo', sa_lexicon=sa_lib)
    
    if (sa_lexicon == 'afinn'):
        # Multidim sentiment analysis
        emo_ls = word2emo('todo', sa_lexicon=sa_lib)

    else:
        print(f"ERROR: {sa_lexicon} is not a valid sentiment analysis library.")
         
    return emo_ls
"""



def corpus2sa_ls(sents_ls, lang='en', lexicon_dt='default'):
    """
    Given a corpus in the form of a list of strings/sentences,
    calculate a the sentiment of each string/sentence and 
    return a list of float, one for each sentence (time series)

    Args:
        text ([type]): [description]
        lang (str, optional): [description]. Defaults to 'en'.
        sa_lib (str, optional): [description]. Defaults to 'syuzhet'.

    Returns:
        [type]: [description]
    """
    
    corpus_sa_ls = []
    
    if (lexicon_dt == 'default'):
        lexicon_dt = get_lexicon()
        for i, a_sent in enumerate(sents_ls):
            print(f"in corpus2sa_ls processing sent #{i}: {a_sent}")
            if (len(a_sent.strip()) > 0):
                corpus_sa_ls.append(sent2lex_sa(a_sent, lexicon_dt=lexicon_dt))
            else:
                corpus_sa_ls.append(0.0)
                
        # Normalize list of sentiment values from -1.0 to +1.0
        sa_min = min(corpus_sa_ls)
        print(f'The min sa is {sa_min}')
        sa_max = max(corpus_sa_ls)
        print(f'The max sa is {sa_max}')
        
        if (sa_min == sa_max):
            if sa_min > 0:
                corpus_sa_norm_ls = [1.0 for i in range(len(corpus_sa_ls))]
            elif sa_max < 0:
                corpus_sa_norm_ls = [-1.0 for i in range(len(corpus_sa_ls))]
            else:
                corpus_sa_norm_ls = [0.0 for i in range(len(corpus_sa_ls))]
        else:
            sa_range = sa_max - sa_min
            print(f'The range is {sa_range}')
            corpus_sa_norm_ls = [((2*(float(i)-sa_min)/sa_range)-1) for i in corpus_sa_ls]

        return corpus_sa_norm_ls
    else:
        print("ERROR: only have syuzhet implement now")
    
    