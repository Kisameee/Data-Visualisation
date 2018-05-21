#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Do some report pn our datas
"""


import pandas as pd
import numpy as np


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
              'ratings_disabled': bool, 'video_error_or_removed': bool, 'description': str, 'category': str}
cols_converters = {'views': _int_converters, 'likes': _int_converters, 'dislikes': _int_converters}
youtube_csv = pd.read_csv('./ressources/FRvideos.csv', engine='c', memory_map=True,
                          low_memory=True, dtype=cols_types, na_values=[''], verbose=True,
                          parse_dates=['trending_date', 'publish_time'], date_parser=_dateparse,
                          converters=cols_converters)
youtube_csv = youtube_csv[youtube_csv['trending_date'] != pd.datetime.strptime('1979-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')]
youtube_csv = youtube_csv[youtube_csv['publish_time'] != pd.datetime.strptime('1979-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')]
youtube_csv['publish_trending'] = youtube_csv['trending_date'] - youtube_csv['publish_time']
print('mean', str(youtube_csv['publish_trending'].mean()))
print('min', str(youtube_csv['publish_trending'].min()))
print('max', str(youtube_csv['publish_trending'].max()))
