
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import praw
import datetime as dt
from sqlalchemy import create_engine
import io
import os

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

   
def getRedditData(reddit,subreddit,tag,limit):

    data = scrape(reddit, subreddit, tag, limit)
    # print(data)
    writeToCSV(data, tag)
    return data




def writeToCSV(df, tag):
    #to save to postgres directly
    # engine = create_engine('postgresql://postgres:password1@localhost:5432/test')
    # df.to_sql(tag, engine, if_exists='replace',index=False)
    
    
    filepath = os.path.join(ROOT_DIR , 'csvFiles')
    df.to_csv(filepath + '/reddit' + '.csv', sep='|', index=False,header=False,encoding='utf-8')
    
    
    
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
    for tag in tagList:
        getRedditData(reddit,subreddit,tag,limit)
        print( f"Dataframe with subreddit {tag} saved into CSV")
    return True

scrapeMultipleData('singapore', ['bitcoin', 'ethereum', 'cardano', 'zilliqa', 'polygon', 'affyn'], 500)
