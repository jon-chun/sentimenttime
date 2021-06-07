import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
    
    
def clean_sent(astring):
    # Lowercase
    astring_lower = astring.lower()
    
    astring_final = astring_lower    
    return astring_final

lineno = 0
corpus_lineno_ls = []
corpus_sents_ls = []
sentiment_vader_ls = []
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
            vs_sentiment = analyzer.polarity_scores(sent_clean_str)
            vs_compound = vs_sentiment['compound']
            # print("VADER Sentiment {:-<65} {}".format(sent_clean_str, str(vs)))
            # print(f"VADER Compound Sentiment: {vs_compound}")
            sentiment_vader_ls.append(vs_compound)

with open("mlm_sentiment_vader.csv", "w", newline='', encoding='utf-8') as fp_out:
    writer = csv.writer(fp_out, delimiter=',')
    writer.writerows(zip(corpus_lineno_ls, sentiment_vader_ls, corpus_sents_ls))

        
'''
for asent in corpus_sents_ls:
    senti_int = analyzer.polarity_scores(asent)
    print("{:-<65} {}".format(asent, str(senti_int)))
        
with open("mlm_syuzhet.txt", "w+") as fp_out:
    for i, aline in enumerate(corpus_sents_ls):
        if True: # re_alpha.match(aline):
            pass # fp_out.write(aline.strip() + '\n')
'''