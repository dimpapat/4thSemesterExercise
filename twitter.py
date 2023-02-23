import array
import configparser
import tweepy
import numpy as np
import pandas as pd
import nltk
import matplotlib.pyplot as plt

from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from collections import Counter
from nltk.corpus import stopwords
from datetime import datetime
from nltk import word_tokenize
from dateutil.parser import parse

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
    array_of_twitter_objects = []
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
            #data = list(csv_reader)
            #return data
            #array = np.array(data)
            #return array

            for row in csv_reader:
                #print(row[4])
                obj = Tweet(row[2], row[1], row[4])
                self.array_of_twitter_objects.append(obj)
                #print(obj.get_date_of_tweet())

        return self.array_of_twitter_objects


class Tweet():

    def __init__(self, id, text, created_at):
        self.id = id
        self.text = text
        self.created_at = created_at

    def get_text_of_tweet(self):
        return self.text

    def get_date_of_tweet(self):
        #2023-02-15 15:03:00+00:00
        new_datetime = datetime.strftime(datetime.strptime(self.created_at, '%Y-%m-%d %H:%M:%S+%z'), '%Y-%m-%d %H:%M:%S')
        return new_datetime


class AnalyzeTweet():

    def __init__(self, tweet):
       self.tweet = Tweet(tweet.id, tweet.text, tweet.created_at)

    def length_of_tweet(self):
        nmb = 0
        c = self.tweet
        nmb = len(c.text)
        return nmb


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
            lemma = lemmatizer.lemmatize(word, pos=AnalyzeTweet.get_wordnet_pos(tag))
            lemmatized_msg.append(lemma)
        return lemmatized_msg

    def count_stopwords(self, msg, lemmatized):
        if lemmatized == True:
            new_sentence = self.lemmatize_sentence(msg)
        else:
            new_sentence = msg
        count = 0
        for word in new_sentence:
            if word in stop_words:
                count += 1
        #print("To count einai : ", count, end='\n')
        return count


    def date_of_tweet(self, msg):
        print(msg.slice(2))


    def count_parts_of_speech(self, msg, lemmatized):
        if lemmatized == True:
            new_sentence = self.lemmatize_sentence(msg)
        else:
            new_sentence = msg
        count = 0
        word_and_tags = nltk.pos_tag(new_sentence)
        counts = Counter(tag for word, tag in word_and_tags)
        total = sum(counts.values())
        a = dict((word, float(count) / total) for word, count in counts.items())
        print(a)

    def make_report_of_tweet_len(self, data):
        # frequencies data

        # setting the ranges and no. of intervals
        range = (50, 350)
        bins = 10

        # plotting a histogram
        plt.hist(data, bins, range, color='green',
                 histtype='bar', rwidth=0.8)

        # x-axis label
        plt.xlabel('Mean number of letters')
        # frequency label
        plt.ylabel('Number of Tweets')
        # plot title
        plt.title('My histogram')

        # function to show the plot
        plt.show()

    def make_report_of_tweet_stopwords(self, data):
        # frequencies data

        # setting the ranges and no. of intervals
        range = (0, 35)
        bins = 100

        # plotting a histogram
        plt.hist(data, bins, range, color='green',
                 histtype='bar', rwidth=0.8)

        # x-axis label
        plt.xlabel('Number of Stopwords')
        # frequency label
        plt.ylabel('Number of Tweets')
        # plot title
        plt.title('My histogram')

        # function to show the plot
        plt.show()


twitter_client = TwitterClient("TIME")
myTweets = twitter_client.readFromFileTweets("test.csv")
mo = []
for tweet in myTweets:
    c1 = Tweet(tweet.id, tweet.text, tweet.created_at)
    c2 = AnalyzeTweet(c1)
    #c2.count_parts_of_speech(c1.text, True)
    #print(c2.length_of_tweet())
    #mo.append(c2.length_of_tweet())
    #print(mo)
    #print(c1.get_text_of_tweet().split())
    mo.append(c2.count_stopwords(c1.get_text_of_tweet(), True))
    print(mo)
c2.make_report_of_tweet_stopwords(mo)


#report = createTwitterStatistics(myTweets)
#report.mesos_oros_of_tweets(myTweets)
#print(myTweets)
#tweet_by_tweet = AnalyzeTweet(myTweets)
#tweet_by_tweet.count_stopwords_with_lemmatization()
#print(tweet_by_tweet.len_of_tweet("We are the same Tesing their mice funcrtion"))
#tweet_by_tweet.date_of_tweet()