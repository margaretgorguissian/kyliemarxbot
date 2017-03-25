from apscheduler.schedulers.background import BackgroundScheduler
from os import system
from time import sleep
from datetime import datetime

from api import getAPI
from tweetGenerator import KylieTweetGenerator

print("tweetScheduler.py Loaded @ {}".format(datetime.now()))

TWITTER_NAME = "KylieJenner"
TWEET_WINDOW = True
FOLLOWERS = []

try:
    print("Attempting to Load/Get New Tweet Set")
    try:
        # Load Existing Tweet Set if We Already Have One
        GENERATOR = KylieTweetGenerator(TWITTER_NAME + "Tweets")
        print("Tweet Generator Created @ {}".format(datetime.now()))
    except:
        # Gather New Tweet Set
        print("Getting Most Current Tweets @ {}".format(datetime.now()))
        system("python getTweetsFromUser.py " + TWITTER_NAME)
        print("Tweet Set Collected @ {}".format(datetime.now()))
        GENERATOR = KylieTweetGenerator(TWITTER_NAME + "Tweets")
        print("Tweet Generator Created @ {}".format(datetime.now()))
    API = getAPI()
    print("Bot Ready To Post.")
    print("Test Tweet:  {}".format(GENERATOR.generateKylieTweet()))
except:
    print("Setup Failed @ {}".format(datetime.now()))
    print("Exiting tweetScheduler.py")
    quit()

def updateTweets():
    try:
        system("python getTweetsFromUser.py " + TWITTER_NAME)
        newGen = KylieTweetGenerator(TWITTER_NAME + "Tweets")
        print("Tweet Set Updated @ {}".format(datetime.now()))
        GENERATOR = newGen
    except:
        print("Tweet Set Update Failed @ {}".format(datetime.now()))

def postTweet():
    tweet = cleanTweet(GENERATOR.generateKylieTweet())
    try:
        if rateLimitNotExceeded():
            API.update_status(tweet)
            print("Tweet Posted @ {}".format(datetime.now()))
            print("--- {}".format(tweet))
    except:
         print("Tweet Posting Failed @ {}".format(datetime.now()))

def friendFollowers():
    print("Getting Followers List @ {}".format(datetime.now()))
    if rateLimitNotExceeded():
        followers = API.followers()
        if followers:
            for follower in followers:
                if follower.id not in FOLLOWERS:
                    if rateLimitNotExceeded():
                        print("Creating Friendship with User: {}".format(follower.id))
                        API.create_friendship(follower.id)
                        FOLLOWERS.append(follower.id)

def rateLimitNotExceeded():
    status = API.rate_limit_status()['resources']['application']['/application/rate_limit_status']['remaining']
    if status > 0:
        print("Rate Limit Status: API Under Rate Limit ({}) @ {}".format(status, datetime.now()))
    else:
        print("Rate Limit Status: Rate Limit Exceeded @ {}".format(datetime.now()))
    return status > 0

def cleanTweet(tweet):
    if tweet.count('"') == 1:
        tweet.replace('"', '')
    if "@" in tweet:
        tweet.replace("@","")
    if "amp;" in tweet:
        tweet.replace("amp;", "")
    return tweet

tweetScheduler = BackgroundScheduler()
tweetScheduler.add_job(postTweet, 'interval', minutes=5, id='postTweet')
tweetScheduler.add_job(updateTweets, 'cron', hour=23, minute=45, id='updateTweets')
tweetScheduler.add_job(friendFollowers, 'cron', hour=00, id='friendFollowers')
tweetScheduler.start()

while True:
    sleep(60)
