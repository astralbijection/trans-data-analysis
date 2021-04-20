import json
import os
from datetime import datetime
from pprint import pprint
from typing import List
import requests
import jsonlines
import twarc
import tweepy
import twitter
from dotenv import load_dotenv
from requests_oauthlib import OAuth1Session
from twarc import Twarc


def parse_twitter_datetime(dt: str):
    return datetime.strptime(dt, '%a %b %d %H:%M:%S +0000 %Y')


def get_politicians(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)


def read_timelines(after_date: datetime, handles: List[str], with_replies=False):
    consumer_key = os.environ.get('CONSUMER_KEY')
    consumer_secret = os.environ.get('CONSUMER_SECRET')
    access_token_key = os.environ.get('ACCESS_TOKEN')
    access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')
    bearer_token = os.environ.get('BEARER_TOKEN')

    tw = twarc.Twarc(consumer_key, consumer_secret, access_token_key, access_token_secret, bearer_token)

    for tweet in tw.search('Dawkins'):
        yield tweet

        created_at = parse_twitter_datetime(tweet['created_at'])
        print(f'Found tweet {tweet["id"]} created at {created_at}')

        if created_at <= after_date:
            break


def store_tweets(tweets):
    with jsonlines.open('../data/tweetdata.jsonl', 'w') as writer:
        for tweet in tweets:
            writer.write(tweet)


def main():
    politicians = get_politicians('../data/politicians.json')
    handles = [handle['handle'] for p in politicians for handle in p['twitters']]

    earliest_date = datetime(2021, 4, 9)
    tweets = read_timelines(earliest_date, handles, with_replies=True)
    store_tweets(tweets)


if __name__ == '__main__':
    load_dotenv()
    main()
