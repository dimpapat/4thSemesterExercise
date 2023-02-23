
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


import array
import configparser
import tweepy
import numpy as np
import pandas as pd
import nltk

from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from collections import Counter
from nltk.corpus import stopwords

nltk.download('averaged_perceptron_tagger')
lemmatizer = WordNetLemmatizer()


config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

# authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

mybearer_token = config['twitter']['Bearer_Token']

stop_words = set(stopwords.words('english'))

class TwitterAuthenticator():

    def autheniticate_twitter_app(self):
        auth = tweepy.OAuthHandler(api_key, api_key_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth

class TwitterClient():
   #query = 'from:FT -is:retweet'
   #client = tweepy.Client(bearer_token=mybearer_token)

    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().autheniticate_twitter_app()
        #self.twitter_client = tweepy.API(self.auth)
        self.twitter_client = tweepy.Client(bearer_token=mybearer_token)
        self.twitter_user = twitter_user
        self.query = 'from: ' + self.twitter_user + ' -is:retweet'

    def get_Tweets(self, num_tweets=1000):
        tweets = []
        for tweet in tweepy.Paginator(self.twitter_client.search_recent_tweets, query=self.query, tweet_fields=['context_annotations', 'created_at'], max_results=100).flatten(limit=1000):
            tweets.append(tweet)
        return tweets

    def save_Tweets(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        #df['source'] = np.array([tweet.source for tweet in tweets])
        #df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        #df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        df.to_csv('test.csv')

        return df


    def readFromFileTweets(self, filename):
        #df = pd.read_csv(filename)
        #print(df)
        from csv import reader

        with open(filename, 'r',  encoding="utf8") as read_obj:
            csv_reader = reader(read_obj)
            data = list(csv_reader)
            return data
            #array = np.array(data)
            #return array

            #for row in csv_reader:
            #    print(row)



class AnalyzeTweet():

    def __init__(self, tweets):
       self.tweets = tweets

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

    def lemmatize_sentence(self, msg):
        sentence = msg.split()
        lemmatized_msg = []
        word_and_tags = nltk.pos_tag(sentence)
        for word, tag in word_and_tags:
            lemma = lemmatizer.lemmatize(word, pos=CleanTweet.get_wordnet_pos(tag))
            lemmatized_msg.append(lemma)
        return lemmatized_msg

    def count_stopwords(self, msg, lemmatized):
        if lemmatized == True:
            new_sentence = self.lemmatize_sentence(msg)
        else:
            new_sentence = msg
        count = 0
        words = new_sentence.split()
        for word in words:
            if word in stop_words:
                count += 1
        #print("To count einai : ", count, end='\n')
        return count


    def len_of_tweet(self, msg):
        number = len(msg)
        print(number)
        return number

    def date_of_tweet(self, msg):





twitter_client = TwitterClient("TIME")
myTweets = twitter_client.readFromFileTweets("test.csv")
#print(myTweets)
tweet_by_tweet = AnalyzeTweet(myTweets)
#tweet_by_tweet.count_stopwords_with_lemmatization()
print(tweet_by_tweet.len_of_tweet("We are the same Tesing their mice funcrtion"))