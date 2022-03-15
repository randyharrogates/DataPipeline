import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import praw
import datetime as dt


# Creating a reddit crawler object - your own user name and password
reddit = praw.Reddit(client_id='cuDitSOXcwUFJxABTQR93Q',
                     client_secret='BN-dhMP04h9hAQB6ZXzfui4ku7faZQ',
                     user_agent='jamiescrapes',
                     username='JamieRan112',
                     password='Harrogates@@112')

print(reddit.user.me())
