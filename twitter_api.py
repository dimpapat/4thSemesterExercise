import tweepy
import configparser
import pandas as pd

# read config file

config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

# authentication

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# user tweets
user = 'FT'
limit = 100


#tweets = api.home_timeline()
tweets = api.user_timeline(screen_name=user, count=limit, tweet_mode='extended')

#columns = ['Time', 'User', 'Tweet']
#data = []
#for tweet in tweets:
#    data.append([tweet.created_at, tweet.user.screen_name, tweet.text])
#print(data)


# create DataFrame
columns = ['User', 'Tweet']
data = []

for tweet in tweets:
   data.append([tweet.user.screen_name, tweet.full_text])

df = pd.DataFrame(data, columns=columns)

df.to_csv('fttweets.csv')
print(df)