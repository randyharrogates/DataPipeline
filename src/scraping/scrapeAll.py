import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import praw
import datetime as dt
from sqlalchemy import create_engine
import io
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

from reddit.scrapeRedditClass import scrapeMultipleData
from twitter.scrapeTwitter import scrapeToCsv

keywords = ['crypto', 'cryptocurrency', 'bitcoin', 'ethereum', 'cardano', 'zilliqa', 'polygon', 'dogecoin', 'solana', 'binance', 'avalanche', 'ripple', 'terra', 'polkadot']
def scrapeAll(keywords):

    scrapeMultipleData('singapore', keywords, 1000)
    scrapeToCsv(keywordList=keywords, start = '2021-12-31', end='2022-12-31', tweet_limit=1000)
