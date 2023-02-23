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

mybearer_token = config['twitter']['Bearer_Token']


# user tweets
user = 'FT'
limit = 1000


#tweets = api.home_timeline()
#tweets = api.user_timeline(screen_name=user, count=limit, tweet_mode='extended')
client = tweepy.Client(bearer_token=mybearer_token)

query = 'from:FT -is:retweet'

# Replace with time period of your choice
start_time = '2020-01-01T00:00:00Z'

# Replace with time period of your choice
end_time = '2022-08-01T00:00:00Z'

#tweets = client.search_all_tweets(query=query, tweet_fields=['context_annotations', 'created_at'],
      #                            start_time=start_time,
     #                          end_time=end_time, max_results=100)

tweets = tweepy.Paginator(client.search_recent_tweets, query=query, tweet_fields=['context_annotations', 'created_at'], max_results=100).flatten(limit=1000)

id = 1

#for tweet in tweets.data:
 #   print(tweet.text)
  #  print(tweet.created_at)

columns = ['Time', 'Tweet']
data = []

for tweet in tweets:
    print(id, tweet.text, end='\n')
    id += 1
    data.append([tweet.created_at, tweet.text])
    #if len(tweet.context_annotations) > 0:
     #   print(tweet.context_annotations)

#columns = ['Time', 'User', 'Tweet']
#data = []
#for tweet in tweets:
#    data.append([tweet.created_at, tweet.user.screen_name, tweet.text])
#print(data)


# create DataFrame
#columns = ['User', 'Tweet']
#data = []


df = pd.DataFrame(data, columns=columns)

df.to_csv('test.csv')
print(df)
#for tweet in tweets:
#   data.append([tweet.user.screen_name, tweet.full_text])

#df = pd.DataFrame(data, columns=columns)


#df.to_csv('fttweets.csv')
#print(df)