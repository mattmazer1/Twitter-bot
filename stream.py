import tweepy, keys, time
from tweepy import TweepyException

client = tweepy.Client(keys.BEARER_TOKEN, keys.API_KEY, keys.API_SECRET_KEY, keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)
auth = tweepy.OAuth1UserHandler(keys.API_KEY, keys.API_SECRET_KEY, keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

user = 12
userTweet = api.user_timeline(user_id = user, count=10)

class MyStream(tweepy.StreamingClient):

    def on_connect(self):
        print("Connected")

    def on_tweet(self, tweet):
        try: 
            if tweet.referenced_tweets == None and tweet.author_id == user:
                print(tweet.text)
                time.sleep(0.5)
        except tweepy.errors.TweepyException as e:
            print(e)
        
stream = MyStream(bearer_token=keys.BEARER_TOKEN)

try:
     for tweet in userTweet:
        stream.add_rules(tweepy.StreamRule('from:jack'))
        api.update_status("@" + user + "Always bullish 🚀🚀", in_reply_to_status_id = tweet.id)
except tweepy.errors.TweepyException as e:
        print(e)

stream.filter(tweet_fields=["referenced_tweets"])


