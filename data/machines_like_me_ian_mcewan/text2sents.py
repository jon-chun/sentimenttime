
import re

re_alpha = re.compile('[a-zA-Z]+')


import spacy
nlp = spacy.load('en_core_web_sm') # or whatever model you have installed
# raw_text = 'Hello, world. Here are two sentences.'
# doc = nlp(raw_text)
# sentences = [sent.string.strip() for sent in doc.sents]

corpus_sents_ls = []

with open("mlm_final_hand.txt", "r+") as fp_in:
    for i, aline in enumerate(fp_in):
        # Strip leading/trailing whitespace
        aline_str = aline.strip()
        if len(aline_str) == 0:
            pass
        else:
            # print(f'Line #{i}: {aline_str}')
            doc = nlp(aline_str)
            sentences_ls = [sent.string.strip() for sent in doc.sents]
            # print(f'  SpaCy SentParse: {sentences_ls}')
            corpus_sents_ls.extend(sentences_ls)
        
with open("mlm_sentences.txt", "w+") as fp_out:
    for i, aline in enumerate(corpus_sents_ls):
        if re_alpha.match(aline):
            fp_out.write(aline.strip() + '\n')