from typing import Dict, List 
from redis import Redis  
from recall.config import config  

"""
Redis 存储和检索物品和用户的嵌入向量
"""
# 配置Redis连接
redis_config = config['redis']  # 从配置模块获取Redis配置信息
redis = Redis(
    host=redis_config['host'],  # 设置Redis服务器的主机地址
    port=redis_config['port'],  # 设置Redis服务器的端口号
    db=redis_config['db'],  # 设置Redis数据库索引
    password=redis_config['password']  # 设置Redis服务器的密码
)

# 定义Redis key，用于存储物品和用户的嵌入向量
ITEM_EMB_KEY = 'recall:emb:item'
USER_EMB_KEY = 'recall:emb:user'

# 定义一个函数，用于保存物品嵌入向量到Redis
def save_item_embedding(item_emb: Dict[int, List[float]]):
    # 将嵌入向量编码为字符串格式
    encoded_emb = {str(k): stringify_vector(v) for k, v in item_emb.items()}
    # 使用hset命令将编码后的嵌入向量保存到Redis的hash结构中
    redis.hset(ITEM_EMB_KEY, mapping=encoded_emb)

# 定义一个函数，用于保存用户嵌入向量到Redis
def save_user_embedding(user_emb: Dict[int, List[float]]):
    # 类似于保存物品嵌入向量的函数，但是保存的是用户嵌入向量
    encoded_emb = {str(k): stringify_vector(v) for k, v in user_emb.items()}
    redis.hset(USER_EMB_KEY, mapping=encoded_emb)

# 定义一个函数，用于从Redis获取单个项目的嵌入向量
def get_one_item_embedding(item_id: int) -> List[float]:
    # 使用hget命令从Redis的hash结构中获取指定key的嵌入向量
    emb = redis.hget(ITEM_EMB_KEY, str(item_id))
    # 如果没有找到嵌入向量，则返回None
    if emb is None:
        return None
    # 解码并解析嵌入向量字符串
    return parse_vector_string(emb.decode())

# 定义一个函数，用于从Redis获取单个用户的嵌入向量
def get_one_user_embedding(user_id: int) -> List[float]:
    # 类似于get_one_item_embedding函数，但是获取的是用户嵌入向量
    emb = redis.hget(USER_EMB_KEY, user_id)
    if emb is None:
        return None
    return parse_vector_string(emb.decode())

# 定义一个函数，用于获取所有物品的嵌入向量
def get_all_item_embedding() -> Dict[int, List[float]]:
    # 使用hgetall命令从Redis的hash结构中获取所有嵌入向量
    data = redis.hgetall(ITEM_EMB_KEY)
    # 解码并解析嵌入向量字符串，构建字典返回
    res = {int(k.decode()): parse_vector_string(v.decode()) for (k, v) in data.items()}
    return res

# 定义一个函数，用于将嵌入向量列表转换为字符串
def stringify_vector(vec):
    if vec is None:
        return ''
    # 将向量中的每个元素转换为字符串，并用冒号连接
    return ':'.join(list(map(lambda v: str(v), vec)))

# 定义一个函数，用于将嵌入向量字符串解析回列表
def parse_vector_string(s):
    if len(s) == 0:
        return None
    # 将字符串按冒号分割，并转换为浮点数列表
    return [float(x) for x in s.split(':')]