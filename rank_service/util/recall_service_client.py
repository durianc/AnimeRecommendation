import requests
from config import config

def get_recall(user_id):
    
    if user_id is not None:
        url = f"{config['recall_endpoint']}/recall/{user_id}"  # 将 user_id 作为路径的一部分
        res = requests.get(url)  # 发送GET请求
        return res.json()  # 返回JSON响应
    else:
        raise ValueError("user_id cannot be None")  # 如果 user_id 是 None，抛出异常
