from typing import Tuple
from pyspark.sql.functions import col, collect_list, udf
from pyspark.sql import SparkSession, DataFrame
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import Word2Vec
import numpy as np
from recall.config import config


def train_item2vec(anime_seq: DataFrame, rating_df: DataFrame) -> Tuple[DataFrame, DataFrame]:
    """
    训练item2vec模型
    :param anime_seq: 电影序列(DataFrame格式, 每行包含一个用户的观影序列)
    :param rating_df: 用户评分(DataFrame格式, 每行包含一个用户对某部电影的评分)
    return: (item_emb_df, user_emb_df)
        - item_emb_df: word(anime_id), vector(embedding), 包含每个电影的向量表示
        - user_emb_df: user_id, user_emb, 包含每个用户的向量表示
    """
    # 从配置中读取模型参数
    model_config = config['item2vec']
    
    # 初始化Word2Vec模型, 并设置参数
    word2vec = Word2Vec(
        vectorSize=model_config['vector_size'], 
        maxIter=model_config['max_iter'], 
        windowSize=model_config['window_size']
    )
    word2vec.setInputCol('anime_ids')
    word2vec.setOutputCol('anime_ids_vec')

    # 使用电影序列数据训练Word2Vec模型
    model = word2vec.fit(anime_seq)
    
    # 获取电影的embedding向量
    item_emb_df = model.getVectors()
    item_vec = model.getVectors().collect()
    
    # 将电影的embedding向量存储到字典中, 便于后续查找
    item_emb = {}
    for item in item_vec:
        item_emb[item.word] = item.vector.toArray()

    @udf(returnType='array<float>')
    def build_user_emb(anime_seq):
        """
        根据用户的观影序列计算用户的embedding向量
        :param anime_seq: 用户的观影序列
        :return: 用户的embedding向量
        """
        # 获取用户观影序列中的电影的embedding向量
        anime_embs = [item_emb[aid] if aid in item_emb else [] for aid in anime_seq]
        # 过滤掉没有embedding向量的电影
        anime_embs = list(filter(lambda l: len(l) > 0, anime_embs))
        # 如果观影序列中有有效的电影向量, 则计算平均值作为用户向量
        if len(anime_embs) > 0:
            ret = np.mean(anime_embs, axis=0).tolist()
        else:
            # 如果没有可用的embedding, 返回全零向量
            ret = [0.0] * model_config['vector_size']
        return ret

    # 根据评分数据计算用户的embedding向量
    user_emb_df = rating_df.where('rating > 7')\
        .groupBy('user_id')\
        .agg(collect_list(col('anime_id').cast('string')).alias('anime_ids'))\
        .withColumn('user_emb', build_user_emb(col('anime_ids')))

    return item_emb_df, user_emb_df
