#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Clean the Youtube CSV data file
"""


import csv
import pandas as pd


youtube_csv = pd.read_csv('./ressources/FRvideos.csv', dtype=str, engine='c', memory_map=True)
del(youtube_csv['video_id'])
# del(youtube_csv['thumbnail_link'])
del(youtube_csv['comments_disabled'])
del(youtube_csv['ratings_disabled'])
del(youtube_csv['description'])
youtube_csv['title'] = youtube_csv['title'].str.replace('"', '').str.replace("'", '')
youtube_csv['channel_title'] = youtube_csv['channel_title'].str.replace('"', '').str.replace("'", '')
youtube_csv['tags'] = youtube_csv['tags'].str.replace('"', '').str.replace("'", '')
youtube_csv['video_error_or_removed'] = youtube_csv['video_error_or_removed'].str.replace('"', '').str.replace("'", '')
youtube_csv['category'] = youtube_csv['category'].str.replace('"', '').str.replace("'", '')

youtube_csv.to_csv('ressources/cleaned_yt.csv', header=False, index=False, quoting=csv.QUOTE_ALL)
