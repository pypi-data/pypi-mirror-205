import os, json
import tweepy
HASHTAG = input('Enter Hashtag: ')
if not HASHTAG.startswith('#'):
   HASHTAG = f'#{HASHTAG}'
def dirr(obj):
   attrs = []
   for attr in list(dir(obj)):
       if not attr.startswith('_'):
           attrs.append(attr)
   return attrs
apify_token = os.getenv('APIFY_TOKEN')                                # APIfy Token
consumer_key = os.getenv('CONSUMER_KEY')                              # Twitter API Key
consumer_secret = os.getenv('CONSUMER_SECRET')                        # Twitter API key secret
bearer_token = os.getenv('BEARER_TOKEN')                              # Twitter Bearer Token
access_token = os.getenv('ACCESS_TOKEN')                              # Twitter Access Token
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')                
auth = tweepy.OAuthHandler(consumer_key, consumer_secret) # Creates an auth handler object
auth.secure = True                                        # Tells twitter that the connection is secure

api = tweepy.API(auth, wait_on_rate_limit=True)           # Creates an api object using the above auth handler object

# Generates a client object to access API V2
client = tweepy.Client(
   bearer_token,
   consumer_key, consumer_secret,
   access_token, access_token_secret
)
cursor = tweepy.Cursor(
   api.search_tweets,
   HASHTAG,
   count=100,
   result_type='recent'
)
tweets = list(cursor.items(50))
print(len(tweets))
print(tweets)