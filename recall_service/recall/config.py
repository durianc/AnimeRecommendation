import os

config = {
    'dataset_path': '/home/cwy/project/AnimeRecommendation/data/',
    'redis': {
        'host': '192.168.211.131',  # Redis服务器的主机地址
        'port': 6379,         # Redis服务器的端口号，默认为6379
        'db': 0,              # 选择的数据库索引，默认为0
        'password': 'q24ty@07'
    },
    'deepwalk': {
        'sample_count': 25000,
        'sample_length': 10
    },
    'item2vec':{
        'vector_size': 128,
        'max_iter': 10,
        'window_size': 5,
    }
    
}
