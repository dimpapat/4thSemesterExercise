
    def count_stopwords_with_lemmatization(self):
        idx = 0
        stats = []
        for tweet in self.tweets:
            row = tweet[1].split()
            word_and_tags = nltk.pos_tag(row)
            print(word_and_tags)
            count = 0
            idx += 1
            for word, tag in word_and_tags:
                lemma = lemmatizer.lemmatize(word, pos=CleanTweet.get_wordnet_pos(tag))
                print(lemma, end="\n")
                if lemma in stop_words:
                    count += 1
            print("To count einai : ", count, end='\n')
            stats.insert(idx, count)
        print(stats)


#    def count_stopwords(self):
#        count = 0
#        tweets = self.tweets

        #tweets.slice(1,2)
#        for tweet in tweets:
#            print(tweet[1])
#            count = 0
#            st = ",".join(str(x) for x in tweet[1])
#            st.replace(" ", "")
#            st.replace('\n', "")
#            st.replace('\"', "")
#            st.strip()
#            st.split()
            #print(st)
            #for word in st.split():
             #   if word in stop_words:
              #      count += 1
            #print("Found", count, end='\n')


