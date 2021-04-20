import json
import os
from datetime import datetime
from typing import List

import jsonlines
from dotenv import load_dotenv
from twarc import Twarc


def parse_twitter_datetime(dt: str):
    return datetime.strptime(dt, '%a %b %d %H:%M:%S +0000 %Y')


def get_politicians(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)


def read_timelines(after_date: datetime, handles: List[str]):
    consumer_key = os.environ.get('consumer_key')
    consumer_secret = os.environ.get('consumer_secret')
    access_token_key = os.environ.get('access_token_key')
    access_token_secret = os.environ.get('access_token_secret')
    twarc = Twarc(consumer_key, consumer_secret, access_token_key, access_token_secret)

    for handle in handles:
        print(f'Scanning twitter handle @{handle}')
        for tweet in twarc.timeline(screen_name=handle):
            created_at = parse_twitter_datetime(tweet['created_at'])
            print(f'Found tweet created at @{created_at}')
            yield tweet
            if created_at <= after_date:
                break


def main():
    politicians = get_politicians('../data/politicians.json')
    handles = [handle['handle'] for p in politicians for handle in p['twitters']]

    with jsonlines.open('../data/tweetdata.jsonl', 'w') as writer:
        earliest_date = datetime(2021, 3, 15)
        for tweet in read_timelines(earliest_date, handles):
            writer.write(tweet)


if __name__ == '__main__':
    load_dotenv()
    main()
