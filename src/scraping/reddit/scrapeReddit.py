import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import praw
import datetime as dt
from sqlalchemy import create_engine
import io
import os

from scrapeRedditClass import Scrape_subreddit

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def writeToCSV(df):
    filepath = os.path.join(ROOT_DIR , 'csvFiles')
    df.to_csv(filepath + '/reddit' + '.csv', sep='|', index=False,header=False,encoding='utf-8')
    
def saveToDb(df, title):
    #to save to postgres directly
    engine = create_engine('postgresql://postgres:password1@localhost:5432/test')
    df.to_sql(title, engine, if_exists='replace',index=False)

def scrape(reddit,subreddit,tag,limit):
    reddit = reddit
    scrape = Scrape_subreddit(reddit,subreddit,tag,limit)
    getDataFrame = scrape.get_dataframe()
    return getDataFrame

def scrapeMultipleData(subreddit,tagList,limit,**kwargs):
    # Creating a reddit crawler object - your own user name and password
    reddit = praw.Reddit(client_id='cuDitSOXcwUFJxABTQR93Q',
                        client_secret='BN-dhMP04h9hAQB6ZXzfui4ku7faZQ',
                        user_agent='jamiescrapes',
                        username='JamieRan112',
                        password='Harrogates@@112')
    
    print(reddit.user.me())
    
    dfList = []
    for tag in tagList:
        partDf = scrape(reddit,subreddit,tag,limit)
        dfList.append(partDf)
        print(f'Dataframe for {tag} created')
    finalDf = pd.concat(dfList)
    writeToCSV(finalDf)
    saveToDb(finalDf, 'reddit')
    print(f'CSV file for reddit created {finalDf.head()}')
    return True

scrapeMultipleData('singapore', ['crypto', 'cryptocurrency', 'bitcoin', 'ethereum', 'cardano', 'zilliqa', 'polygon', 'dogecoin', 'solana', 'binance', 'avalanche', 'ripple', 'terra', 'polkadot'], 500)