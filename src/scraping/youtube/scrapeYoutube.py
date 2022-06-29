import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
# from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
import pandas as pd
import glob
from sqlalchemy import create_engine
import base64

postgrespw = 'cGFzc3dvcmQx'
API_KEY = 'QUl6YVN5Q0J0Rm5LZjBfaWk0VVJDSTJqVk9GbGNEeU1Wd1d1YWlF'


def search_keywords(items, count):
    channel_df = pd.DataFrame()
    ids = []
    titles = []
    channel_ids=[]
    channel_titles=[]
    published_dates=[]
    descriptions=[]
    for item in items:
        print(item)
        ids.append(item['id']['videoId'])
        titles.append(item['snippet']['title'])
        channel_ids.append(item['snippet']['channelId'])
        published_dates.append(item['snippet']['publishedAt'])
        channel_titles.append(item['snippet']['channelTitle'])
        descriptions.append(item['snippet']['description'])
    if channel_df.empty:
        ids_df = pd.DataFrame({'id':ids})
        titles_df = pd.DataFrame({'title':titles})
        channel_id_df = pd.DataFrame({'channel_id': channel_ids})
        channel_title_df = pd.DataFrame({'channel_name': channel_titles})
        published_dates_df = pd.DataFrame({'published_date': published_dates})
        descriptions_df = pd.DataFrame({'description':descriptions})
        channel_df = pd.concat([ids_df, titles_df, channel_id_df, channel_title_df, 
                                published_dates_df, descriptions_df], axis=1)
    else:
        channel_df.append({'id':pd.DataFrame(ids)})
        channel_df.append({'title':pd.DataFrame(titles)})
        channel_df.append({'channel_id':pd.DataFrame(channel_ids)})
        channel_df.append({'channel_name':pd.DataFrame(channel_titles)})
        channel_df.append({'published_date':pd.DataFrame(published_dates)})
        channel_df.append({'description':pd.DataFrame(descriptions)})
    channel_df
    doc_name = "/home/randyubuntu/git/DataPipeline/src/scraping/youtube/csvFiles/" + "vidWithKeyword" + str(count) + ".csv"
    channel_df.to_csv(doc_name, index=False)
    return channel_df


def scrapeWithKeywords(kw_list):
    api_key= base64.b64decode(API_KEY).decode("utf-8")
    api_service_name = "youtube"
    api_version = "v3"
    
    youtube = build(api_service_name, api_version, developerKey=api_key)
    
    count=0
    for kw in kw_list:
        count+=1
        request = youtube.search().list(part="snippet", q=kw, type='video', 
                                        publishedAfter='2020-01-01T00:00:00Z', maxResults=100)

        response = request.execute()
        items = response['items']
        
        search_keywords(items, count)
    
    #combine all csv into one
    df = pd.concat(map(pd.read_csv, glob.glob('/home/randyubuntu/git/DataPipeline/src/scraping/youtube/csvFiles/*.csv')))
    df = df.drop_duplicates()
    df = df.replace(r'\n',' ', regex=True)
    saveToDb(df, 'youtube_raw')
    df.to_csv('/home/randyubuntu/git/DataPipeline/src/scraping/csvFiles' + '/mergedYoutube.csv', index=False)
    return True

def saveToDb(df, title):
    #to save to postgres directly
    engine = create_engine(f'postgresql://postgres:{base64.b64decode(postgrespw).decode("utf-8")}@localhost:5432/test')
    df.to_sql(title, engine, if_exists='replace',index=False)

    
# scrapeAll()