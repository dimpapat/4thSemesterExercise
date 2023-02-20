import json

import numpy as np
import pandas as pd
import nltk

nltk.download("wordnet")

from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from collections import Counter
from nltk.corpus import stopwords


lemmatizer = WordNetLemmatizer()


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


nltk.download('averaged_perceptron_tagger')

stop_words = set(stopwords.words('english'))



# sentence = "testint my data".split()

df = pd.read_csv('fttweets.csv')

sentence = df.loc[:, ["Tweet"]].to_string().split()


word_and_tags = nltk.pos_tag(sentence)

numOfStopWords = 0
current_idx = 0
word2idx = {}

for word, tag in word_and_tags:
    lemma = lemmatizer.lemmatize(word, pos=get_wordnet_pos(tag))
    #print(lemma, end="\n")
    if lemma not in stop_words:
        #print(lemma, end="\n")
        if lemma not in word2idx:
            word2idx[lemma] = current_idx
            current_idx += 1
    else:
        numOfStopWords += 1

print(numOfStopWords)
print("here")
#print(word2idx)



#print(word_and_tags)



counts = Counter(tag for word, tag in word_and_tags)

total = sum(counts.values())

a = dict((word, float(count) / total) for word, count in counts.items())

print(a)
import json

f = open("fttweets.txt", "a")
f.write(json.dumps(a))
f.close()




