import string

import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
from nltk import TweetTokenizer, WordNetLemmatizer


def build_stopword_set():
    nltk.download('stopwords')
    nltk.download('wordnet')

    # Build stopword set
    stop = set()
    stop.update(nltk.corpus.stopwords.words('english'))
    stop.update(nltk.corpus.stopwords.words('spanish'))
    stop.update(string.punctuation)

    # Some twitter-specific ones
    stop.update(['rt', '…', '—', 'u'])
    return stop


def sublist_replacement(original, old, new):
    """Replaces a sublist with another list."""
    output = []

    def is_match(i):
        if len(original) - i < len(old):
            return False
        for j in range(len(old)):
            if original[i + j] != old[j]:
                return False
        return True

    i = 0
    while i < len(original):
        if is_match(i):
            output.extend(new)
            i += len(old)
        else:
            output.append(original[i])
            i += 1

    return output


TOKEN_PERMITTED_CHARS = set('#@')


def is_token(token: str, stopwords):
    return all((
        c.isalnum() or c in TOKEN_PERMITTED_CHARS
        for c in token
    )) and token not in stopwords


def clean_tweet_tokens(token_list):
    token_list = sublist_replacement(token_list, ['covid', '-', '19'], ['covid19'])
    token_list = sublist_replacement(token_list, ['covid', '19'], ['covid19'])
    token_list = sublist_replacement(token_list, ['covid'], ['covid19'])
    token_list = sublist_replacement(token_list, ['bears', 'ears'], ['bears ears'])
    return token_list


tokenizer = TweetTokenizer(strip_handles=True, reduce_len=True)
lemmatizer = WordNetLemmatizer()


def tokenize_tweet(tweet, stopwords):
    tokens = [tok.lower() for tok in tokenizer.tokenize(tweet)]
    tokens = [
        lemmatizer.lemmatize(tok)
        for tok in clean_tweet_tokens(tokens)
        if is_token(tok, stopwords)
    ]
    return tokens


def tokenize_tweets(tweets, stopwords):
    return (
        tokenize_tweet(tweet, stopwords)
        for tweet in tweets
    )


def make_ngrams(ngram_size=1):
    def operator(tokens):
        return list(nltk.ngrams(tokens, ngram_size))

    return operator


def tokenize_tweets_and_flatten(tweets, stop, ngram_size=1):
    tokenized_tweets = map(make_ngrams(ngram_size), tokenize_tweets(tweets, stop))
    return (' '.join(ngram) for tweet in tokenized_tweets for ngram in tweet)


def calculate_word_freqs(series, stop, ngram_size=1):
    all_tokens = np.array(list(
        tokenize_tweets_and_flatten(series, stop, ngram_size=ngram_size)
    ))
    tokens, counts = np.unique(all_tokens, return_counts=True)
    frequencies = pd.DataFrame(
        data={'token': tokens, 'count': counts}
    )
    frequencies.set_index('token', inplace=True)
    frequencies.sort_values('count', inplace=True, ascending=False)
    return frequencies


def plot_frequencies(ax: plt.Axes, freq_series, top_count=30):
    top_n = freq_series.iloc[:top_count]
    ax.barh(top_n.index, top_n)
    ax.invert_yaxis()


def plot_ngrams(ax, tweet_series, stop, ngram_size=1, top_count=50):
    frequency_df = calculate_word_freqs(tweet_series, stop, ngram_size=ngram_size)
    plot_frequencies(ax, frequency_df['count'], top_count=top_count)
