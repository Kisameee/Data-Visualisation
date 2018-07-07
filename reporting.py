#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Do some report on our data
TODO: Cleanup outliers ?
"""


from pprint import pprint
from itertools import chain
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import unidecode


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
            date = pd.np.nan
            # date = pd.datetime.strptime('1979-01-01', '%Y-%m-%d')
    return date


# video_id,trending_date,title,channel_title,publish_time,tags,views,likes,dislikes,comment_count,comments_disabled,ratings_disabled,video_error_or_removed,description,category
cols_types = {'video_id': str, 'trending_date': str, 'title': str, 'channel_title': str, 'publish_time': str, 'tags': str,
              'views': int, 'likes': int, 'dislikes': int, 'comment_count': float, 'comments_disables': bool,
              'ratings_disabled': bool, 'video_error_or_removed': bool, 'description': str, 'category': 'category'}
cols_converters = {'views': _int_converters, 'likes': _int_converters, 'dislikes': _int_converters}
youtube_csv = pd.read_csv('./ressources/FRvideos.csv', engine='c', memory_map=True,
                          low_memory=True, dtype=cols_types, na_values=[''], converters=cols_converters,
                          parse_dates=['trending_date', 'publish_time'], date_parser=_dateparse).dropna()

cols_to_analyze = ['publish_trending', 'views', 'likes', 'dislikes', 'comment_count']
youtube_csv['likes_dislikes'] = youtube_csv['likes'] / youtube_csv['dislikes']
youtube_csv['publish_trending'] = youtube_csv['trending_date'] - youtube_csv['publish_time']
youtube_csv['publish_trending_seconds'] = youtube_csv['publish_trending'].map(lambda d: d.total_seconds())
youtube_csv_by_category = youtube_csv[cols_to_analyze[1:] + ['category', 'publish_trending_seconds', 'likes_dislikes']]\
    .groupby('category')

print('Stats')
for col in cols_to_analyze:
    print('**********', col, '**********')
    print('Mean :', str(youtube_csv[col].mean()))
    print('Median :', str(youtube_csv[col].median()))
    print('Min :', str(youtube_csv[col].min()))
    print('Max :', str(youtube_csv[col].max()))
    print()

print('Stats grouped by category')
for col in cols_to_analyze[1:] + ['publish_trending_seconds', 'likes_dislikes']:
    print('**********', col, '**********')
    print('Mean :', str(youtube_csv_by_category[col].mean()), '\n')
    print('Median :', str(youtube_csv_by_category[col].median()), '\n')
    print('Min :', str(youtube_csv_by_category[col].min()), '\n')
    print('Max :', str(youtube_csv_by_category[col].max()), '\n')
    print('\n')

print('Most using words in title')
# words_counts = Counter(pipe([youtube_csv['title'].str.lower().str.split().dropna(), list, chain.from_iterable]))
words_counts = Counter(chain.from_iterable(list(youtube_csv['title'].str.lower().str.split().dropna()
                                                .apply(lambda word: [unidecode.unidecode(w) for w in word]))))
words_counts = words_counts.most_common()  # [int(len(words_counts) * 0.1):int(len(words_counts) * 0.9)]
pprint(words_counts)

print('Plot 1')
sbc = dict(youtube_csv_by_category['publish_trending_seconds'].median())
bsbc = [vsbc for vsbc in sbc.values()]
plt.figure(1)
plt.bar([l for l in sbc], [(vsbc / 3600) for vsbc in sbc.values()])
# pyplot.pie([vsbc for vsbc in sbc.values()], labels=[l for l in sbc], autopct='%1.1f%%', startangle=90)
plt.legend(('Temps median en heures',))
plt.xticks(rotation=90)
# pyplot.savefig('./plots/temps_median_par_categorie_pour_passer_de_published_a_trending.png')
# stats_by_category = youtube_csv_by_category['publish_trending_seconds'].mean().to_frame(['category', 'pts'])

print('Plot 2')
likes_dislikes_by_categories = dict(youtube_csv_by_category['likes_dislikes'].median())
grouped_ldbc = [ldbc for ldbc in likes_dislikes_by_categories.values()]
plt.figure(2)
plt.bar([el for el in likes_dislikes_by_categories], [el for el in likes_dislikes_by_categories.values()])
# plt.pie(x=[el for el in likes_dislikes_by_categories.values()], autopct='%1.1f%%', startangle=90,
#         labels=[el for el in likes_dislikes_by_categories.keys()])
plt.legend(('Ratios medians likes / dislikes par catégories',))
plt.xticks(rotation=90)

print('Plot 3')
count_by_categories = dict(youtube_csv_by_category['views'].count())
grouped_cbc = [cbc for cbc in count_by_categories.values()]
plt.figure(3)
# plt.bar([el for el in likes_dislikes_by_categories], [el for el in likes_dislikes_by_categories.values()])
plt.pie(x=[el for el in count_by_categories.values()], autopct='%1.1f%%', startangle=90,
        labels=[el for el in count_by_categories.keys()])
plt.legend(('Nombre de vidéos par catégories',))

print('Plotting !')
plt.show()

print('Fun Facts')
print('Most viewed video :', youtube_csv[youtube_csv['views'] == youtube_csv['views'].max()].to_dict()['title'])
print('Most liked video :', youtube_csv[youtube_csv['likes'] == youtube_csv['likes'].max()].to_dict()['title'])
print('Most disliked video :', youtube_csv[youtube_csv['dislikes'] == youtube_csv['dislikes'].max()].to_dict()['title'])
