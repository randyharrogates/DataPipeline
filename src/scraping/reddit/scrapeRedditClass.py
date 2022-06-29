
from email.mime import base
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import praw
import datetime as dt
from sqlalchemy import create_engine
import io
import os
import base64
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 


passwords = pd.read_csv(parentdir + '/encrypt.csv')
redditClientId = passwords['redditClientId'][0]
redditPassword= passwords['redditPassword'][0]
redditClientSecret= passwords['redditClientSecret'][0]
postgrespw = ['postgrespw'][0]




ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# custom scrape_subreddit object that will group all the functions and scrape a subreddit
class Scrape_subreddit:
    def __init__(self, reddit, subred, tag, no_of_results):
        self.name = subred
        self.dataframe = None
        self.subreddit = reddit.subreddit(subred)
        self.tag = tag
        self.no_of_results = no_of_results
        self.topics_dict = {"title": [],
                            "score": [],
                            "id": [], 
                            "comms_num": [],
                            "created": [],
                            "body": []}

    def scrape_data(self):
        for submission in self.subreddit.search(self.tag, limit=self.no_of_results):
            self.topics_dict["title"].append(submission.title)
            self.topics_dict["score"].append(submission.score)
            self.topics_dict["id"].append(submission.id)
            self.topics_dict["comms_num"].append(submission.num_comments)
            self.topics_dict["created"].append(submission.created)
            self.topics_dict["body"].append(submission.selftext)
        return self.topics_dict

    def get_dataframe(self):
        self.dataframe = pd.DataFrame(self.scrape_data())
        self.temp_timestamp = self.dataframe["created"].apply(
            lambda x: dt.datetime.fromtimestamp(x))
        self.dataframe = self.dataframe.assign(timestamp=self.temp_timestamp)
        self.dataframe['year'] = self.dataframe['timestamp'].apply(
            lambda x: x.year)
        self.dataframe['month'] = self.dataframe['timestamp'].apply(
            lambda x: x.month)
        self.dataframe['day'] = self.dataframe['timestamp'].apply(
            lambda x: x.day)
        self.dataframe['time'] = self.dataframe['timestamp'].apply(
            lambda x: x.time())
        self.dataframe.drop(['timestamp'], axis=1, inplace=True)
        self.dataframe = self.dataframe.drop_duplicates(
            subset='title', keep="first")
        
        self.dataframe['body'] = self.dataframe['body'].replace(r'\n+', ' ', regex=True)
        self.dataframe['body'] = self.dataframe['title'].replace(r'\n+', ' ', regex=True)
       
        return self.dataframe

   


def writeToCSV(df):
    df.to_csv('/home/randyubuntu/git/DataPipeline/src/scraping/dataFiles' + '/mergedReddit.csv', sep='|', index=False,encoding='utf-8')
    
def saveToDb(df, title):
    #to save to postgres directly
    engine = create_engine(f'postgresql://postgres:{base64.b64decode(postgrespw).decode("utf-8")}@localhost:5432/test')
    df.to_sql(title, engine, if_exists='replace',index=False)

def scrape(reddit,subreddit,tag,limit):
    reddit = reddit
    scrape = Scrape_subreddit(reddit,subreddit,tag,limit)
    getDataFrame = scrape.get_dataframe()
    return getDataFrame

def scrapeMultipleData(subreddit,tagList,limit,**kwargs):
    # Creating a reddit crawler object - your own user name and password
    
    reddit = praw.Reddit(client_id=base64.b64decode(redditClientId).decode("utf-8"),
                        redditClientSecret=base64.b64decode(redditClientSecret).decode("utf-8"),
                        user_agent='jamiescrapes',
                        username='JamieRan112',
                        password=base64.b64decode(redditPassword).decode("utf-8"))
    
    print(reddit.user.me())
    
    dfList = []
    for tag in tagList:
        partDf = scrape(reddit,subreddit,tag,limit)
        dfList.append(partDf)
        print(f'Dataframe for {tag} created')
    finalDf = pd.concat(dfList)
    writeToCSV(finalDf)
    saveToDb(finalDf, 'reddit_raw')
    print(f'CSV file for reddit created {finalDf.head()}')
    return True



