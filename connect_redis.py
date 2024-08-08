import redis

r = redis.Redis(host='192.168.211.131', port=6379, db=0, password='q24ty@07')

# 测试连接
print("Redis 版本：", r.info()['redis_version'])


