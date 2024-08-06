import requests
from api.config import config

def get_anime(user_id):
    if user_id is not None:
        url = f"{config['rank_endpoint']}/rank/{user_id}"  # 直接在URL中填入user_id
        res = requests.get(url)  # 发送GET请求
        res.raise_for_status()  # 检查请求是否成功
        return res.json()  # 返回JSON响应
    else:
        raise ValueError("user_id cannot be None")  # 如果user_id为空，抛出异常

def get_similar_anime(anime_id):
    if anime_id is not None:
        url = f"{config['recall_endpoint']}/sim/{anime_id}"  # 直接在URL中填入anime_id
        res = requests.get(url)  # 发送GET请求
        res.raise_for_status()  # 检查请求是否成功
        return res.json()  # 返回JSON响应
    else:
        raise ValueError("anime_id cannot be None")  # 如果anime_id为空，抛出异常
