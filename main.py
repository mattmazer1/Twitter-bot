import tweepy, keys, datetime, schedule, time, multiprocessing
from datetime import timedelta, timezone
from tweepy import TweepyException

auth = tweepy.OAuth1UserHandler(keys.API_KEY, keys.API_SECRET_KEY)
auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

hashtags = '#web3 OR #nft OR #ethereum OR #solana OR #defi OR #metaverse OR #crypto OR web3 OR blockchain' 

tweets = tweepy.Cursor(api.search_tweets, q=hashtags, count=10, tweet_mode="extended", result_type="popular").items(10)

user = 'jack' 

jack = api.user_timeline(screen_name = user, count=1)

image = api.media_upload(filename='./Images/meme.jpg') 

mention = tweepy.Cursor(api.mentions_timeline).items()

def fetchPosts():
    try:
        for tweet in tweets:
            if tweet.created_at > datetime.datetime.now(timezone.utc) - timedelta(hours=24):
             tweetID = dict(tweet._json)["id"]
             tweetText = dict(tweet._json)["full_text"]
             api.retweet(tweetID)
             print("ID:" + str(tweetID))
             print("Text:" + str(tweetText))
    except tweepy.errors.TweepyException as e:
            print(e)


def replyToUser():
    try:
        for tweet in jack:
            api.update_status("@" + user + " Always bullish 🚀🚀", in_reply_to_status_id = tweet.id)
    except tweepy.errors.TweepyException as e:
        print(e)


def replyWithMeme():
    try:
        for mentions in mention:
            name = mentions.user.screen_name
            print(mentions.text)
            api.update_status("@" + name + " ", in_reply_to_status_id = mentions.id, media_ids= 
            [image.media_id_string])
    except tweepy.errors.TweepyException as e:
        print(e)


def fetchWeb3():
    schedule.every().day.at("08:00").do(fetchPosts)
    while True:
        schedule.run_pending()
        time.sleep(1)

def checkUser():
    while True:
        replyToUser()
        time.sleep(60) 

def checkMention():
    while True:
        replyWithMeme()
        time.sleep(60)       


if __name__ == "__main__":
    process1 = multiprocessing.Process(target=fetchWeb3)
    process2 = multiprocessing.Process(target=checkUser)
    process3 = multiprocessing.Process(target=checkMention)
    
    process1.start()
    process2.start()
    process3.start()
