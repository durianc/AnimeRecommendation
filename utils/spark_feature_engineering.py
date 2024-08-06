#!/usr/bin/env python
# coding: utf-8

import pyspark
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, trim, mean, col, lit, collect_list, max, expr
from pyspark.ml.feature import StringIndexer, MinMaxScaler, VectorAssembler
from pyspark.ml import Pipeline
from pyspark.sql.types import ArrayType, IntegerType
from pyspark.sql.functions import udf
import numpy as np

# 初始化SparkSession
spark = SparkSession.builder.appName("feat-eng").getOrCreate()

# 读取anime数据集
anime_df = spark.read.csv('../data/anime.csv', header=True, inferSchema=True)
anime_df.printSchema()

"""
处理动漫数据集中关于“类型（genres）”的字段，并将其转换为多热编码格式
得到每个动漫的anime_id以及其对应的genre_indexes列表
"""
# 多热编码genres
# 分割genre字符串并去除空白
# split--将genre列中的字符串按逗号分割成数组
# explode(...)--将数组中的每个元素转换为单独的行，结果是每种类型作为独立的genre_item
# trim()--去除genre_item中的空白字符
genre_df = anime_df.withColumn('genre_item', explode(split(col('genre'), '[,]'))).withColumn('genre_item', trim(col('genre_item')))

# 显示前10行数据
genre_df.select(['anime_id', 'genre_item']).show(10)    # 只选择anime_id和genre_item两列

# 使用StringIndexer对genre进行索引
# StringIndexer: 用于将字符串类型的分类变量转换为数值类型的索引
# fit: 计算出每种类型的索引映射关系
string_indexer = StringIndexer(inputCol='genre_item', outputCol='genre_index')
genre_indexed_df = string_indexer.fit(genre_df).transform(genre_df).withColumn('genre_index', col('genre_index').cast('int'))

# 显示索引后的genre数据
genre_indexed_df[['anime_id', 'genre_item', 'genre_index']].show(10)

# 聚合anime_id，收集genre_index列表(变成一个动漫ID对应一个genre的列表，列表中是int类型表示的类型)
# groupBy('anime_id'): 按anime_id分组
# agg(...): 收集每个anime_id对应的所有genre_index，将其存储为列表genre_indexes
pre_multihot_df = genre_indexed_df.groupBy('anime_id').agg(collect_list('genre_index').alias('genre_indexes'))

# 显示聚合后的数据
pre_multihot_df.show(10)

"""
将之前处理的动漫类型索引列表转换为多热编码数组
eg: [1,3,4] 转为[0,1,0,1,1...]
"""

max_genre_index = genre_indexed_df.agg(max(col('genre_index'))).head()['max(genre_index)']
# 定义UDF，将genre_index列表转换为多热编码数组
# UDF: 用户自定义函数
print("max_genre_index:", max_genre_index)
# 输入类型指定为列表，返回类型为整型数组
@udf(returnType=ArrayType(IntegerType()))
def multihot_list(l, max_index):
    fill = np.zeros(max_index + 1, dtype=np.int32)
    for i in l:
        fill[i] = 1
    return fill.tolist()

# 应用UDF转换为多热编码
# 将genre_indexes列和最大索引值传入，生成多热编码数组
multihot_df = pre_multihot_df.withColumn('genre_multihot', multihot_list(col('genre_indexes'), lit(max_genre_index)))

# 显示多热编码结果
multihot_df.printSchema()
multihot_df.show(10)
print("---------------------------------------------------------------------------------------------------------")
"""
读取评分数据集，计算每个动漫的平均评分，并对平均评分进行特征缩放
"""

# 读取rating数据集并过滤出有效评分
rating_df = spark.read.csv('../data/rating.csv', header=True, inferSchema=True).filter(col('rating') > 0)

# 计算平均评分
# 按照anime_id分组，对每个组计算rating的平均值，并将结果命名为ave_rating
ave_rating_df = rating_df.groupBy('anime_id').agg(mean('rating').alias('ave_rating'))

# 显示平均评分结果
ave_rating_df.show(10)

# 特征向量化和Min-Max缩放
# 定义MinMaxScaler和VectorAssembler进行特征缩放
vec_assembler = VectorAssembler(inputCols=['ave_rating'], outputCol='ave_rating_vec')
ave_rating_scaler = MinMaxScaler(inputCol='ave_rating_vec', outputCol='ave_rating_scaled')
pipeline = Pipeline(stages=[vec_assembler, ave_rating_scaler])  # 创建一个Pipeline，将特征转换和缩放过程组合在一起

"""
Pipeline将多个数据转换和模型训练步骤组合在一起，形成一个可重复使用的工作流. 一旦定义，Pipeline 可以自动处理数据流
有序的步骤集合，每个步骤称为 Stage（可以是一个数据转换（如特征提取、数据预处理等）或一个机器学习模型（如分类器、回归模型等））
"""
# 应用Pipeline进行特征缩放
rating_scaled_df = pipeline.fit(ave_rating_df).transform(ave_rating_df)

# 显示缩放后的特征
rating_scaled_df.printSchema()
rating_scaled_df.show(10)

# 定义UDF，将缩放后的向量转换为单个float值
@udf(returnType='float')
def unwrap_list(rating):
    return rating.toArray().tolist()[0]

# 应用UDF转换为单个float值
rating_scaled_df = rating_scaled_df.withColumn('ave_rating_minmax', unwrap_list(col('ave_rating_scaled')))

# 显示转换后的结果
rating_scaled_df.show(10)

# 选择需要的列
rating_result_df = rating_scaled_df.select(['anime_id', 'ave_rating_minmax'])

# 将anime_df和rating_result_df进行连接
result_df = anime_df.join(rating_result_df, on='anime_id')

# 显示连接后的数据
result_df.printSchema()
result_df.show(10)

# 保存结果到CSV文件
# 将所有数据合并成一个单独的 CSV 文件
result_df.coalesce(1).write.mode('overwrite').format('csv').option('header', True).save('feature_engineering_result.csv')
