import requests
import tweepy
from dotenv import load_dotenv
import os
from requests_oauthlib import OAuth1Session
import json
import time
# import twitter

# load_dotenv()
# api_key = os.getenv("TWITTER_API_KEY")
# api_secret_key = os.getenv("TWITTER_API_SECRET_KEY")
# access_token = os.getenv("TWITTER_ACCESS_TOKEN")
# access_token_secret = os.getenv("TWITTER_ACCESS_SECRET_TOKEN")
# bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
# consumer_key = os.getenv("TWITTER_API_KEY")
# consumer_secret = os.getenv("TWITTER_API_SECRET_KEY")

def fetch_reddit(query, subreddit):
    url = "https://api.pushshift.io/reddit/search/submission/"
    params = {
        "q": query,
        "size": 100,
        # "sort": "desc",
        # "sort_type": "created_utc",
        # "subreddit": subreddit,
    }
    r = requests.get(url, params=params)
    data = r.json()
    return data["data"]

def fetch_twitter(query, api_key, api_secret_key, access_token, access_token_secret, bearer_token):
    # auth = tweepy.OAuthHandler(api_key, api_secret_key)
    # auth.set_access_token(access_token, access_token_secret)
    # api = tweepy.API(auth)
    # search_results = api.search_recent_tweets(query, count=10)
    # return search_results


    # auth = tweepy.AppAuthHandler(api_key, api_secret_key)
    # api = tweepy.API(auth)
    # search_results = api.search_tweets(query, count=10)
    # return search_results

    # client = tweepy.Client(api_key, api_secret_key, access_token, access_token_secret)
    # client = tweepy.Client(bearer_token=bearer_token)
    # client = tweepy.Client(consumer_key= api_key,consumer_secret= api_secret_key,access_token= access_token,access_token_secret= access_token_secret)
    # tweets = client.search_recent_tweets(query=query, max_results=10)
    # return tweets
    # client = tweepy.Client(consumer_key= api_key,consumer_secret= api_secret_key,access_token= access_token,access_token_secret= access_token_secret)
    # tweets = client.search_recent_tweets(query=query, max_results=10)
    # return tweets
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    tweets = tweepy.Cursor(api.search_30_day, label='test', query=query).items(10)
    # return tweets
    respones = []
    for tweet in tweets:
        print(tweet.created_at, url + tweet.user.screen_name +
                            status + tweet.id_str, tweet.full_text) 
        response.append([tweet.created_at, url + tweet.user.screen_name +
                            status + tweet.id_str, tweet.user.screen_name,
                            tweet.favorite_count, tweet.retweet_count,
                            tweet.full_text])
        tweets.next()
    return response

def t2():
    load_dotenv()
    api_key = os.getenv("TWITTER_API_KEY")
    api_secret_key = os.getenv("TWITTER_API_SECRET_KEY")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_SECRET_TOKEN")
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    consumer_key = os.getenv("TWITTER_API_KEY")
    consumer_secret = os.getenv("TWITTER_API_SECRET_KEY")

    auth = tweepy.OAuth1UserHandler(
        consumer_key=api_key,
        consumer_secret=api_secret_key,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

    api = tweepy.API(auth)

    query = "hello world"

    tweets = []
    cursor = tweepy.Cursor(api.search_tweets, query).items()
    while True:
        try:
            tweet = cursor.next()
            print(tweet.text)
            tweets.append(tweet)

        except Exception as e:
            print(e)
            break
        

    # Print tweets
    for tweet in tweets:
        print(tweet.text)




if __name__ == "__main__":

    # load_dotenv()
    # api_key = os.getenv("TWITTER_API_KEY")
    # api_secret_key = os.getenv("TWITTER_API_SECRET_KEY")
    # access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    # access_token_secret = os.getenv("TWITTER_ACCESS_SECRET_TOKEN")
    # bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    # consumer_key = os.getenv("TWITTER_API_KEY")
    # consumer_secret = os.getenv("TWITTER_API_SECRET_KEY")

    reddit_data = fetch_reddit("bc1qwukmzzjqn5hwsp4uaswc4c53gc0xz5asrv0prx", "bitcoin")
    # twitter_data = fetch_twitter("hello world", api_key, api_secret_key, access_token, access_token_secret, bearer_token)
    # print(reddit_data)
    # print(len(reddit_data))
    # print(twitter_data)
    # print(len(twitter_data))