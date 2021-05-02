import gzip
from datetime import datetime

import jsonlines
import pandas as pd


def parse_twitter_datetime(dt: str):
    return datetime.strptime(dt, '%a %b %d %H:%M:%S +0000 %Y')


def read_jsonl_gz(path):
    with jsonlines.Reader(gzip.open(path)) as reader:
        raw_politician_tweets = list(reader)

    tweet_df = pd.DataFrame(data={
        'tweet': [t['full_text'] for t in raw_politician_tweets],
        'author': [t['user']['screen_name'] for t in raw_politician_tweets],
        'date': [parse_twitter_datetime(t['created_at']) for t in raw_politician_tweets],
        'id': [t['id'] for t in raw_politician_tweets]
    })
    tweet_df.set_index('id')

    return tweet_df
