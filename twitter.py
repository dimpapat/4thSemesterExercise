import configparser
import tweepy
import numpy as np
import pandas as pd

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

        #df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        #df['source'] = np.array([tweet.source for tweet in tweets])
        #df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        #df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        print(df)

        return df


twitter_client = TwitterClient("TIME")
twitter_client.save_Tweets(twitter_client.get_Tweets())