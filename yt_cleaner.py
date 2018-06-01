#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Clean the Youtube CSV data file
"""


import csv
import pandas as pd


def _int_converters(i):
    try:
        y = int(i)
    except ValueError:
        y = 0
    return y


def _dateparse(d):
    try:
        date = pd.datetime.strptime(str(d), '%Y-%m-%d %H:%M:%S')
    except ValueError:
        try:
            date = pd.datetime.strptime(str(d), '%Y-%m-%d')
        except ValueError:
            date = pd.datetime.strptime('1979-01-01', '%Y-%m-%d')
    return date


# video_id,trending_date,title,channel_title,publish_time,tags,views,likes,dislikes,comment_count,comments_disabled,ratings_disabled,video_error_or_removed,description,category
cols_types = {'video_id': str, 'trending_date': str, 'title': str, 'channel_title': str, 'publish_time': str, 'tags': str,
              'views': int, 'likes': int, 'dislikes': int, 'comment_count': float, 'comments_disables': bool,
              'ratings_disabled': bool, 'video_error_or_removed': bool, 'description': str, 'category': 'category'}
cols_converters = {'views': _int_converters, 'likes': _int_converters, 'dislikes': _int_converters}
youtube_csv = pd.read_csv('./ressources/FRvideos.csv', engine='c', memory_map=True,
                          low_memory=True, dtype=cols_types, na_values=[''], converters=cols_converters,
                          parse_dates=['trending_date', 'publish_time'], date_parser=_dateparse)
del(youtube_csv['video_id'])
# del(youtube_csv['thumbnail_link'])
del(youtube_csv['comments_disabled'])
del(youtube_csv['ratings_disabled'])
del(youtube_csv['description'])
# youtube_csv['title'] = youtube_csv['title'].str.replace('"', '').str.replace("'", '')
# youtube_csv['channel_title'] = youtube_csv['channel_title'].str.replace('"', '').str.replace("'", '')
youtube_csv['tags'] = youtube_csv['tags'].str.replace('"', '').str.replace("'", '')
# youtube_csv['video_error_or_removed'] = youtube_csv['video_error_or_removed'].str.replace('"', '').str.replace("'", '')
# youtube_csv['category'] = youtube_csv['category'].str.replace('"', '').str.replace("'", '')
# youtube_csv.to_csv('ressources/cleaned_yt_v2.csv', header=True, index=False, quoting=csv.QUOTE_ALL, sep=';')
youtube_csv.to_csv('ressources/cleaned_yt_v2.csv', header=True, index=False, sep=',', quoting=csv.QUOTE_NONNUMERIC)
