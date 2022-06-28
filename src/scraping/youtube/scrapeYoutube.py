import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
# from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
import pandas as pd



def search_keywords(items, response_count):
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
    doc_name = "compilation of videos per keyword" + str(response_count) + ".csv"
    channel_df.to_csv(doc_name, index=False)
    return channel_df

def list_of_channels():
    api_key=""
    api_service_name = "youtube"
    api_version = "v3"
    
    # Get credentials and create an API client
    youtube = build(api_service_name, api_version, developerKey=api_key)

    channel_df = pd.DataFrame(columns=['id','title', 'channelID'])
    request = youtube.videoCategories().list(part="snippet",regionCode="SG")

    response = request.execute()
    items = response['items']
    ids = []
    titles = []
    channel_ids=[]
    for item in items:
        ids.append(item['id'])
        titles.append(item['snippet']['title'])
    ids_df = pd.DataFrame({'id':ids})
    titles_df = pd.DataFrame({'title':titles})
    channel_df = pd.concat([ids_df, titles_df], axis=1)
    return channel_df


def scrapeWithKeywords():
    api_key=""
    api_service_name = "youtube"
    api_version = "v3"

    # Get credentials and create an API client
    youtube = build(api_service_name, api_version, developerKey=api_key)
    kw_list= pd.read_csv("keywords.csv")
    kw_list = kw_list['keywords'].to_list()
    kw_list =[k for k in kw_list if str(k) != 'nan']
    response_count=0
    for kw in kw_list:
        response_count+=1
        request = youtube.search().list(part="snippet", q=kw, type='video', 
                                        publishedAfter='2020-01-01T00:00:00Z', maxResults=50)

        response = request.execute()
        items = response['items']
        
        search_keywords(items, response_count)
        
        
def add_boolean_keywords(new_df,col_check,keywords):
    #initialize new columns
    contains_keywords=[]
    count=0
    for ind, val in new_df.iterrows():
        count+=1
        
        boolean_kw = False
        for col in col_check:
            for kw in keywords:
                if str(kw).lower() in str(val[col]).lower():
                    boolean_kw = True
        contains_keywords.append(boolean_kw)
    return contains_keywords

        
def scrapeAll():
    for i in range(1,len(kw_list)):
        filename = "compilation of videos per keyword" + str(i) + ".csv"
        file = pd.read_csv(filename)
        mental_health_keywords = ['depression', 'mental', 'illness', 'unalive', 'social', 'anxiety', 'loneliness', 'stress', 'lonely', 'isolation', 'suicide', 
                                'abuse', 'death', 'post', 'traumatic', 'stress', 'disorder', 'no', 'motivation', 'therapy', 'trauma', 'counselling', 'mood', 
                                'disorder', 'mood', 'swings', 'mental', 'health', 'angst', 'emotion', 'phobia', 'addiction', 'stigma', 'self-harm', 'neurosis', 
                                'abuse', 'disorder', 'dependence', 'socialize', 'help', 'dead', 'melancholia', 'dysthemia', 'tired', 'trapped', 'paranoia', 
                                'overwhelmed', 'irritable', 'bipolar', 'psychologist', 'well-being', 'imh', 'sos', 'counsellor', 'toxic']

        covid_list = add_boolean_keywords(file,['title','description'],['covid', 'coronavirus', 'covid-19', 'pandemic'])
        sg_list = add_boolean_keywords(file,['title','description'],['singapore', 'singaporean','sg'])
        mental_health_list = add_boolean_keywords(file,['title','description'],mental_health_keywords)
        relevant_list = [covid_list[i] and sg_list[i] and mental_health_list[i] for i in range(len(covid_list))]

        contain_covid_df= pd.DataFrame({'contains_covid':covid_list})
        contain_sg_df= pd.DataFrame({'contain_sg':sg_list})
        contain_mental_health_df = pd.DataFrame({'contain_mental_health':mental_health_list})
        relevant_df = pd.DataFrame({'relevant':relevant_list})
        file = pd.concat([file,contain_covid_df, contain_sg_df, contain_mental_health_df, relevant_df], axis=1)
        file.to_csv(filename, index=False)