from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import col, collect_list, udf
from collections import defaultdict
from pyspark.sql.session import SparkSession
import numpy as np
import dill
import os.path

from recall.config import config

rng = np.random.default_rng()


def build_seq(rating_df: DataFrame, spark: SparkSession):
    """
    进行随机游走生成样本数据

    Args:
        rating_df (DataFrame): 包含用户评分数据的DataFrame
        spark (SparkSession): Spark会话对象

    Returns:
        DataFrame: 包含随机游走生成样本数据的DataFrame
    """
    entrance_items = None
    entrance_probs = None
    transfer_probs = None

    # 检查是否存在预先训练好的模型文件
    if os.path.isfile('output/entrance_items.dill'):
        with open('output/entrance_items.dill', 'rb') as f:
            entrance_items = dill.load(f)
        with open('output/entrance_probs.dill', 'rb') as f:
            entrance_probs = dill.load(f)
        with open('output/transfer_probs.dill', 'rb') as f:
            transfer_probs = dill.load(f)
        print("load model from output")

    else:
        # 过滤评分大于7的数据
        rating_df = rating_df.where('rating>7')

        # 1. 按用户ID分组，收集每个用户的动漫ID列表
        watch_seq_df = rating_df.groupBy('user_id').agg(
            collect_list(col('anime_id').cast('string')).alias('anime_ids')
        )

        # 2. 构建动漫矩阵
        watch_seq = watch_seq_df.collect()
        watch_seq = [s['anime_ids'] for s in watch_seq]
        matrix = defaultdict(lambda: defaultdict(int))
        for i in range(len(watch_seq)):
            if i % 1000 == 0:
                print(f'Adding sequence {i}')
            seq = watch_seq[i]
            add_seq_to_matrix(seq, matrix)

        # 3. 构建转移概率矩阵
        transfer_probs = {k: get_transfer_probs(v) for k, v in matrix.items()}
        print(f'Transfer probabilities built. {len(transfer_probs)} entrances')

        # 4. 构建入口概率
        counts = {k: sum(neighbors.values()) for k, neighbors in matrix.items()}
        entrance_items = list(transfer_probs.keys())
        total_count = sum(counts.values())
        entrance_probs = [counts[k] / total_count for k in entrance_items]
        print('Entrance probabilities built.')

        # 保存模型到文件
        with open('output/entrance_items.dill', 'wb') as f:
            dill.dump(entrance_items, f)
        with open('output/entrance_probs.dill', 'wb') as f:
            dill.dump(entrance_probs, f)
        with open('output/transfer_probs.dill', 'wb') as f:
            dill.dump(transfer_probs, f)
        print("save model to output")

    # 5. 随机游走生成样本数据
    n = config['deepwalk']['sample_count']
    length = config['deepwalk']['sample_length']
    samples = []
    for i in range(n):
        if i % 1000 == 0:
            print(f'Random walk done {i}')
        s = one_random_walk(length, entrance_items, entrance_probs, transfer_probs)
        samples.append(s)
    print(f'Random walk generated {n} samples.')

    return spark.createDataFrame([[row] for row in samples], ['anime_ids']) # 怀疑导致报错


def add_seq_to_matrix(seq, m):
   """
   将动漫ID序列添加到转移矩阵中

   Args:
       seq (list): 动漫ID列表
       m (defaultdict): 转移矩阵
   """
   for i in range(len(seq)):
       for j in range(i + 1, len(seq)):
           a = seq[i]
           b = seq[j]
           if a == b:  # 如果两个动漫ID相同，则跳过这次循环迭代
               continue
           m[a][b] += 1  # 增加从动漫ID a 到动漫ID b 的转移次数
           m[b][a] += 1  # 增加从动漫ID b 到动漫ID a 的转移次数，实现无向图的对称性


def get_transfer_probs(vs):
   """
   计算转移概率

   Args:
       vs (dict): 转移次数的字典

   Returns:
       dict: 转移概率的字典
   """
   neighbours = vs.keys()
   total_weight = sum(vs.values())
   transfer_probabilities = {neighbor: weight / total_weight for neighbor, weight in vs.items()}

   return transfer_probabilities


def one_random_walk(length, entrance_items, entrance_probs, transfer_probs):
   """
   进行一次随机游走

   Args:
       length (int): 随机游走的长度
       entrance_items (list): 入口节点列表
       entrance_probs (list): 入口节点概率列表
       transfer_probs (dict): 转移概率矩阵

   Returns:
       list: 随机游走生成的节点序列
   """
   # 从入口节点中随机选择一个初始节点
   current_node = rng.choice(entrance_items, p=entrance_probs)
   walk = [current_node]

   for _ in range(length - 1):
       if current_node in transfer_probs:
           neighbors = list(transfer_probs[current_node].keys())
           probs = list(transfer_probs[current_node].values())
           next_node = rng.choice(neighbors, p=probs)
           walk.append(next_node)
           current_node = next_node
       else:
           # 如果当前节点没有转移概率（没有出边），从随机选择一个入口节点
           current_node = rng.choice(entrance_items, p=entrance_probs)
           walk.append(current_node)

   return walk
