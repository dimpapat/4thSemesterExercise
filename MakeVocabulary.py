def makeVocabulary():
    current_idx = 0
    word2idx = {}
    for doc in documents:
        tokens = word_tokenize(doc)
        for token in tokens:
            if token not in word2idx:
                word2idx[token] = current_idx
                current_idx += 1
