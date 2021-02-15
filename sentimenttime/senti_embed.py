def get_sa_lex(sa_lib='syuzhet'):
    """
    Read in sentiment analysis lexicon specificed by sa_lib
    into appropriate global variable
    1. syuzhet_lex_dt[word] = <value>

    Args:
        sa_lib (str, optional): [description]. Defaults to 'syuzhet'.
    """
    
    if (sa_lib == 'syuzhet'):
        with open(SYUZHET_FN, newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames='word')
            for i, row in enumerate(reader):
                # print(f"reading syuzhet row {i} with row: {row}")
                syuzhet_dt[row['o']] = row['r']
            print(f"just read in {len(syuzhet_dt.keys())} words into syuzhet_dt of type {type(syuzhet_dt)}")
    else:
        print("ERROR: Only read syuzhet_dict for now")
        
    print(f"exit get_sa_lex() with {len(syuzhet_dt.keys())} entries in syuzhet_dt")
    return syuzhet_dt
    

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


def sent2lex_sa(text, lang='en', sa_lib='syuzhet'):
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

    # print(f"in sent2lex with text of type {type(text)}")
    
    # Remove all not alphanumeric and whitespace characters
    text = re.sub(r'[^\w\s]', '', text) 
    
    # Check valid input types
    # if (~isinstance(text, str)):  # (type(text) == str):  #  (~isinstance(text, str)):
    #     print(f"ERROR: sent2lex_sa() only takes type str not type {type(text)}: {text}")
        
    # Check for empty/null strings
    text = text.strip().lower()
    if (len(text) < 1):
        print("ERROR: sent2lex_sa() given empty/null string")
    
    # Preprocess text (e.g. lowercase, etc)
    text = clean_text(text)
    # print(f"In sent2lex_sa with text= {text}")
    
    sent_sa_fl = 0.0
    
    if (sa_lib == 'syuzhet'):
        for a_word in text.split():
            # print(f"looking up the word: {a_word}")
            # print(syuzhet_dt['harry'])
            try:
                word_sa_fl = float(syuzhet_dt[a_word])
                sent_sa_fl = sent_sa_fl + word_sa_fl
                # print(f"{a_word} has a sentiment value of {word_sa_fl}")
            except TypeError: # KeyError:
                # a_word is not in lexicon so it adds 0 to the sentence sa sum
                print(f"TypeError: cannot convert {syuzhet_dt[a_word]} to float")
                continue
            except KeyError:
                # print(f"KeyError: missing key {a_word} in defaultdict syuzhet_dt")
                continue
            except:
                e = sys.exc_info()[0]
                print(f"ERROR {e}: sent2lex_sa() cannot catch a_word indexing into syuzhet_dt error")
        
        # print(f"Leaving sent2lex_sa() with sentence sa value = {str(sent_sa_fl)}")
        return sent_sa_fl
            
        
    if (sa_lib == 'bing'):
        # Simple lexical approach
        emo_ls = word2emo('todo', sa_lib=sa_lib)
    
    if (sa_lib == 'afinn'):
        # Multidim sentiment analysis
        emo_ls = word2emo('todo', sa_lib=sa_lib)

    else:
        print(f"ERROR: {sa_lib} is not a valid sentiment analysis library.")
         
    return emo_ls


def sent2vader_sa(text, lang='en'):
    """
    Given a text string, calculate the sentiment based
    upon the VADER sentiment analysis program.

    Args:
        text ([type], optional): [description]. Defaults to sent_str.
        lang (str, optional): [description]. Defaults to 'en'.
    """
    
    # Remove all not alphanumeric and whitespace characters
    text = re.sub(r'[^\w\s]', '', text) 

    # Check for empty/null strings
    text = text.strip().lower()
    if (len(text) < 1):
        print("ERROR: sent2vader_sa() given empty/null string")
        return 0.0
        
    text = clean_text(text)
    # print(f"In sent2lex_sa with text= {text}")

    # Preprocess text (e.g. lowercase, etc)
    # text = clean_text(text)
    # print(f"In sent2lex_sa with text= {text}")
        
    try:
        sent_sa_fl = analyzer.polarity_scores(text)
        # print(f"Leaving sent2lex_sa() with sentence sa value = {str(sent_sa_fl)}")
        return sent_sa_fl['compound']
    except:
        e = sys.exc_info()[0]
        print(f"ERROR {e}: sent2lex_sa() cannot catch a_word indexing into syuzhet_dt error")
        return 0.0
    


def sent2stan_sa(text, lang='en'):
    """
    Given a text string, calculate the sentiment based
    upon the Stanford Staza (CoreNLP) library

    Args:
        text ([type], optional): [description]. Defaults to sent_str.
        lang (str, optional): [description]. Defaults to 'en'.
    """
    
    return text

    
def sent2bert_sa(text, lang='en'):
    """
    Given a text string, calculate the sentiment based
    upon the BERT language model.

    Args:
        text ([type], optional): [description]. Defaults to sent_str.
        lang (str, optional): [description]. Defaults to 'en'.
    """
    
    return text


    
def sent2nrc_sa(text, lang='en'):
    """
    Given a text string, calculate the sentiment based 
    upon the NRC lexicon

    Args:
        text ([type], optional): [description]. Defaults to sent_str.
        lang (str, optional): [description]. Defaults to 'en'.
        info (str, optional): [description]. Defaults to 'sa'.

    Returns:
        [type]: [description]
    """

    return text


def sent2nrc_emo(text, lang='en'):
    """
    Given a text string, calculate the emotional 
    aspects based upon the NRC lexicon

    Args:
        text ([type], optional): [description]. Defaults to sent_str.
        lang (str, optional): [description]. Defaults to 'en'.
    """
    
    return text


def sent2liwc(text, lang='en'):
    """
    Given a text string, calculate the psycholinguistic
    aspects based upon the LIWC lexicon (license required)

    Args:
        text ([type], optional): [description]. Defaults to sent_str.
        lang (str, optional): [description]. Defaults to 'en'.
    """
    

def corpus2lex_sa(sents_ls, lang='en', sa_lib='syuzhet'):
    """
    Given a corpus in the form of a list of strings/sentences,
    calculate a the sentiment of each string/sentence and 
    return a list of float, one for each sentence

    Args:
        text ([type]): [description]
        lang (str, optional): [description]. Defaults to 'en'.
        sa_lib (str, optional): [description]. Defaults to 'syuzhet'.

    Returns:
        [type]: [description]
    """
    
    corpus_sa_ls = []
    
    if (sa_lib == 'syuzhet'):
        for a_sent in sents_ls:
            if (len(a_sent.strip()) > 0):
                corpus_sa_ls.append(sent2lex_sa(a_sent, sa_lib='syuzhet'))
            else:
                corpus_sa_ls.append(0.0)
                
        return corpus_sa_ls
    else:
        print("ERROR: only have syuzhet implement now")
    
    