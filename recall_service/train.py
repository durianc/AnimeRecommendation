from pyspark.sql.functions import col
from pyspark.sql import SparkSession
from dataset.anime import spark_load_ratings
from model import item2vec
from dataset import embedding
from model.seq import deepwalk_seq

"""
重新训练用户和物品的embedding
"""

def train():
    with SparkSession.builder.appName("recall").getOrCreate() as spark:
        try:
            # 加载评分数据
            rating_df = spark_load_ratings(spark)
            # # 打印 schema
            # rating_df.printSchema()

            # # 查看数据类型和统计信息
            # rating_df.describe("anime_id").show()

            # # 检查是否存在无效的 anime_id
            # invalid_anime_ids = rating_df.filter(col("anime_id").cast("int").isNull())
            # invalid_anime_ids.show()
            print("Rating data loaded successfully.")

            # 构建序列数据
            anime_seq = deepwalk_seq.build_seq(rating_df, spark)
            print("Sample generation done.")

            # -------------------------------------------------------------------
            # 显示anime_seq的schema和前几行，检查数据类型
            anime_seq.printSchema()
            anime_seq.show(5)
            # 检查anime_seq是否为空
            if anime_seq.count() == 0:
                print("anime_seq is empty.")
                return
            else:
                print("anime_seq is not empty.")
            # -------------------------------------------------------------------
            # 训练 item2vec 模型
            (item_emb_df, user_emb_df) = item2vec.train_item2vec(anime_seq, rating_df)
            print("Embedding trained successfully.")

            # 收集物品嵌入
            item_vec = item_emb_df.collect()
            item_emb = {}
            for row in item_vec:
                item_emb[row['word']] = row['vector'].toArray()

            # 保存物品嵌入到 Redis
            embedding.save_item_embedding(item_emb)
            print(f'{len(item_emb)} Item embedding saved to Redis.')

            # 收集用户嵌入
            user_vec = user_emb_df.collect()
            user_emb = {}
            for row in user_vec:
                user_emb[row.user_id] = row.user_emb

            # 保存用户嵌入到 Redis
            embedding.save_user_embedding(user_emb)
            print(f'{len(user_emb)} User embedding saved to Redis.')

            print("item2vec embedding done.")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    train()
