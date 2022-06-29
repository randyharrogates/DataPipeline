import pandas as pd 
from sqlalchemy import create_engine
import snscrape.modules.twitter as sntwitter
import itertools
import os
import glob
from pathlib import Path
import base64

postgrespw = 'cGFzc3dvcmQx'
print(base64.b64encode(postgrespw.encode("utf-8")))

def search_by_keywords(keyword, start, end, tweet_limit):
    '''
    This is to search for tweets based on keywords, with location preset to Singapore. 
    Keywords: can be string or list 
    Date format: YYYY-MM-DD
    '''
    loc = '1.290270, 103.851959, 30km'
    scraped_tweets = sntwitter.TwitterSearchScraper(f'{keyword} geocode:"{loc}" since:{start} until:{end}').get_items()
    sliced_scraped_tweets = itertools.islice(scraped_tweets, tweet_limit)
    
    tweets_df = pd.DataFrame(sliced_scraped_tweets)
    tweets_df.to_csv(f'/home/randyubuntu/git/DataPipeline/src/scraping/twitter/csvFiles/{keyword}.csv', index=False)
    return sliced_scraped_tweets

def scrapeToCsv(keywordList, start, end, tweet_limit):
    for keyword in keywordList:
        search_by_keywords(keyword, start, end, tweet_limit)
        #combine the csv
    tweets = pd.concat(map(pd.read_csv, glob.glob('/home/randyubuntu/git/DataPipeline/src/scraping/twitter/csvFiles/*.csv')))
    tweets = tweets.drop_duplicates()
    tweets = tweets.replace(r'\n',' ', regex=True)
    print(tweets.head(10))
    tweets.to_csv('/home/randyubuntu/git/DataPipeline/src/scraping/csvFiles' + '/mergedTwitter.csv', index=False)
    saveToDb(tweets, 'twitter_raw')
    return True
    
def saveToDb(df, title):
    #to save to postgres directly
    engine = create_engine(f'postgresql://postgres:{base64.b64decode(postgrespw).decode("utf-8")}@localhost:5432/test')
    df.to_sql(title, engine, if_exists='replace',index=False)
    



