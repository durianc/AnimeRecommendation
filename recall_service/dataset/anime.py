from posixpath import join
from os.path import join
import pandas as pd
from pyspark.sql.session import SparkSession

from functools import lru_cache
from recall.config import config


@lru_cache()
def load_dataset():
    anime_df = pd.read_csv(
        config['dataset_path']+'anime.csv', index_col='anime_id')
    rating_df = pd.read_csv(config['dataset_path']+'rating.csv')

    return (anime_df, rating_df)


@lru_cache
def spark_load_ratings(spark: SparkSession):
    return spark.read.csv(join(config['dataset_path'], 'rating.csv'), header=True, inferSchema=True)
