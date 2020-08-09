#!/usr/bin/env python3
# coding: utf-8

# In[139]:


import re
import io
import praw
import math
import requests
import statistics
import pytesseract
import pandas as pd
import datetime as dt
from PIL import Image
from IPython.display import display

CLIENTID = '###'
CLIENT_SECRET = '###'
USER_AGENT = '###'
USERNAME = '###'
PASSWORD = '###'

SUBREDDIT = 'wallstreetbets'
SUBFLAIR = 'gain' 
TIME_FILTER = 'week'
FILE_NAME = 'wsbGainRecord'


def get_date(created):
    
    return dt.datetime.fromtimestamp(created)


class Flair_Data:
    # connect to reddit

    def __init__(self,subreddit):
        
        self.reddit = praw.Reddit(client_id=CLIENTID,
                    client_secret=CLIENT_SECRET,
                    user_agent=USER_AGENT,
                    username=USERNAME,
                    password=PASSWORD)

        # access the subreddit

        self.subreddit = self.reddit.subreddit(SUBREDDIT)
        self.data = {}
        self.data_record = pd.DataFrame()


    def search_sub(self,subflair,timeframe):
        self.flair_search=self.subreddit.search(f"flair:{SUBFLAIR}",time_filter=TIME_FILTER)

        self.topics_dict = { "title":[],
                "id":[], "url":[],
                "created":[],
                "Value Change":[],
                "Heading Values":[],
                "Image Values":[],
                "Body Values":[],
                "body":[],
                "Format Match":[]}

        for self.submission in self.flair_search:
            self.topics_dict["title"].append(self.submission.title)
            self.topics_dict["id"].append(self.submission.id)
            self.topics_dict["url"].append(self.submission.url)
            self.topics_dict["created"].append(self.submission.created)
            self.topics_dict["Value Change"].append(0)
            self.topics_dict["Heading Values"].append(0)
            self.topics_dict["Image Values"].append(0)
            self.topics_dict["Body Values"].append(0)
            self.topics_dict["body"].append(self.submission.selftext)
            self.topics_dict["Format Match"].append(0)
        
        self.data = self.topics_dict
        self.data = pd.DataFrame(self.data)
        self._timestamp = self.data["created"].apply(get_date)
        self.data = self.data.assign(timestamp = self._timestamp)
        print(self.data)


    def open_CSV(self):
        try:
            open_record = pd.read_csv(f'/####/####/{FILE_NAME}.txt')
            self.data_record = open_record
        except:
            pass

    def write_record(self):

        frames = [self.data, self.data_record]
        if self.data_record.empty:
            new_record = self.data
        else:
            new_record = pd.concat(frames, sort=False, axis=0, join='inner')
        new_record.drop_duplicates(subset ="id", keep = 'first', inplace = True)
        print(new_record)
        new_record.to_csv(f'/####/######/{FILE_NAME}.txt')



gainResults = Flair_Data(SUBREDDIT)
gainResults.search_sub(SUBFLAIR,TIME_FILTER)
gainResults.open_CSV()
gainResults.write_record()







