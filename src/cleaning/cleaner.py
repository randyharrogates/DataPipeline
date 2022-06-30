import pandas as pd
import numpy as np
import os
from os import environ
import base64
import sys
import inspect
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
print(parentdir)

passwords = pd.read_csv(parentdir + '/scraping/encrypt.csv')
postgrespw = passwords['postgrespw'][0]
print(passwords.head())
print(postgrespw)
print(f'postgresql://postgres:{base64.b64decode(postgrespw).decode("utf-8")}@localhost:5432/test')
DB_URI = f'postgresql://postgres:{base64.b64decode(postgrespw).decode("utf-8")}@localhost:5432/test'

#Purpose of this two functions is to make them more dynamic

def loadDataframe(table):
    df = pd.read_sql(table, DB_URI)
    return df
    
    
def loadDataframesIntoList(tables):
    db_uri = environ.get(DB_URI)
    engine=db.create_engine(DB_URI)
    
    dfList = []
    for table in tables:        
        df = loadDataframe(table)
        dfList.append(df)
    return dfList

tables = ['reddit_raw', 'twitter_raw', 'youtube_raw']
redditDf = loadDataframesIntoList(tables)[0]
twitterDf = loadDataframesIntoList(tables)[1]
youtubeDf = loadDataframesIntoList(tables)[2]


#clean data to get title, content, year
def cleanReddit(df):
    
    df= df[['title', 'body', 'year']]
    df['year'] = df['year'].astype('int64')
    print(df['year'].dtypes)
    print(df.head())
    df['title'] = df['title'].astype(str).replace('[^a-zA-Z]', ' ', regex=True)
    df['title'] = df['title'].str.strip()
    df['body'] = df['body'].astype(str).replace('[^a-zA-Z]', ' ', regex=True)
    df['body'] = df['body'].str.strip()
    print(df.head())
    
    
def cleanTwitter(df):
    #remove other languages
    df = df.loc[df['lang'] == 'en' ]
    df = df[['content', 'date']]
    df = df.rename({'content':'body', 'date':'year'}, axis = 1)
    print(df.head())
    
    #Add title column
    df = df.reindex(columns=['title'] + df.columns.tolist())
    print(df.head())
    
    #change eyar to right format
    df['year'] = df['year'].astype(str).str[0:4]
    print(df['year'])
    
    
    
# twitterDf = twitterDf[['content', 'date']]
# youtubeDf = youtubeDf[['title', 'description', 'published_date']]

cleanTwitter(twitterDf)