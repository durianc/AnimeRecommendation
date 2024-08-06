from kafka import KafkaConsumer
import json

# 创建 Kafka 消费者
consumer = KafkaConsumer(
    'clicks',             # 订阅的主题名称
    'views',              # 订阅的主题名称
    bootstrap_servers=['192.168.211.131:9092'],  # Kafka 服务器地址
    auto_offset_reset='earliest',   # 从最早的消息开始读取
    enable_auto_commit=True,          # 自动提交偏移量
    group_id='my-group',              # 消费者组
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # 反序列化消息
)

print("等待消费消息...")

for message in consumer:
    # 打印主题、分区、偏移量和消息内容
    print(f"主题: {message.topic}")
    print(f"分区: {message.partition}")
    print(f"偏移量: {message.offset}")
    print(f"消息: {message.value}")
    print("-" * 30)