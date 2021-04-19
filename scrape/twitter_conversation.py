import twitter
from pprint import pprint



def main():
    api = twitter.Api(
        consumer_key=os.environ.get('consumer_key'),
        consumer_secret=os.environ.get('consumer_secret'),
        access_token_key=os.environ.get('access_token_key'),
        access_token_secret=os.environ.get('access_token_secret'),
    )

    status = api.GetStatus('1364650157392945152').AsDict()
    pprint(status)
    replies = api.GetReplies(status['id'], 100)
    pprint(replies)


if __name__ == '__main__':
    load_dotenv()
    main()