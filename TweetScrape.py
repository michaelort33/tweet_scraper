#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 12:37:38 2019

@author: michael
"""

import tweepy
import pandas as pd
from tqdm import tqdm
import time
import numpy as np

#import os
#os.chdir('/home/michael/Documents/DeeperSignals')


####input your credentials here
consumer_key = 'kmflAhDlFLYvVLzUhUTv5Agbw'
consumer_secret = 'D8Giq3GMjIMaBQN0Qw63tsoHpajA7hNKy2ouo1XeqQP46SP38C'
access_token = '4266439228-U0ySetwuTNEtz3ZGdyPWKVrfIGKY866EMIrzNbN'
access_token_secret = 'CVynCeCX22NtK8iygTHGWjota2JhGTfPgk2CO1MUnPfBK'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True,timeout=1000)

personality = {}
for idx,tweet in enumerate(tweepy.Cursor(api.search,q="#YourPersonalityIn3Words",count=100,
                           lang="en",
                           since="2017-04-03").items()):
    personality[idx]=[tweet.created_at, tweet.text.encode('utf-8'),tweet.author.screen_name]

persons = pd.DataFrame(personality).transpose()

persons.to_csv('persons.csv',index=False)

past_tweets = {}

all_names = persons.loc[:,2]

chunks = int(np.floor(len(all_names)/500))-1
chunk_size=500
idx = 0
for i in range(chunks):
    some_names = all_names.loc[i*chunk_size:(i+1)*500-1,]
    for name in tqdm(some_names):
        status_cursor = tweepy.Cursor(api.user_timeline, screen_name=name, count=200,tweet_mode='extended')
        status_list = status_cursor.iterator.next()
        for each_tweet in range(len(status_list)):
            text=status_list[each_tweet]._json['full_text']
            past_tweets[idx]=[name,text]
            idx += 1
    time.sleep(900)
    
all_history = pd.DataFrame(past_tweets).transpose()
all_history.to_pickle('all.pkl')



