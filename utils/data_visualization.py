#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt

# 设置数据的基础路径
BASE_PATH = './data'

# 读取CSV文件
anime_df = pd.read_csv(f'{BASE_PATH}/anime_info.csv', index_col='anime_id')
rating_df = pd.read_csv(f'{BASE_PATH}/rating.csv')

# 检查数据格式
print(anime_df.dtypes)
print(rating_df.dtypes)

# 获取不同动漫和用户的数量
uniq_anime_count = rating_df['anime_id'].nunique()
uniq_user_count = rating_df['user_id'].nunique()

# 打印不同动漫和用户的数量
print(f'Unique anime count: {uniq_anime_count}')
print(f'Unique user count: {uniq_user_count}')

# 获取评分数据的总数
total_ratings = rating_df.shape[0]
print(f'Total ratings count: {total_ratings}')

# 检查评分的唯一值数量并绘制评分分布图
uniq_ratings = rating_df['rating'].nunique()
print(f'Unique ratings count: {uniq_ratings}')
rating_df['rating'].plot.hist(bins=2*uniq_ratings + 1)

# 描述有效评分的统计信息
valid_rating_df = rating_df[rating_df['rating'] > 0]
print(valid_rating_df['rating'].describe())

# 3.1 每部动漫的评分数
rating_groupby = valid_rating_df.groupby('anime_id').count()
rating_groupby.plot.hist(bins=100, grid=True, figsize=(12, 8), alpha=0.5)
print(rating_groupby.describe())

# 3.2 每个用户的评分
user_rating_count = valid_rating_df.groupby('user_id').count()
user_rating_count.plot.hist(bins=100, grid=True, figsize=(12, 8), alpha=0.5)
print(user_rating_count.describe())

# 3.3 动漫类型分布
genres = {}
for (index, row) in anime_df.iterrows():
    try:
        anime_genres = [g.strip() for g in row['genre'].split(',')]
        for genre in anime_genres:
            if genre not in genres:
                genres[genre] = 0
            genres[genre] += 1
    except Exception as e:
        print(f"Error processing genre for anime {index}: {e}")

# 绘制动漫类型分布图
fig = plt.figure(figsize=(20, 10))
ax = fig.add_axes([0, 0, 1, 1])
tuples = sorted(genres.items(), key=lambda x: x[1], reverse=True)
labels, values = zip(*tuples)
ax.barh(labels, values)
plt.yticks(rotation=70, fontsize=15)
plt.show()

# 5. 评分数量和评分高低的关系
groupby_df = valid_rating_df.groupby('anime_id').agg({
    'rating': ['count', 'mean']
}).rename(columns={'rating_count': 'count', 'rating_mean': 'mean'})
groupby_df.plot.scatter(x='count', y='mean', grid=True, figsize=(12, 8))