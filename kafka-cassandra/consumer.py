from kafka import KafkaConsumer
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json
import datetime
import logging

# 设置日志配置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Kafka topics
KAFKA_TOPICS = ['clicks', 'views']

# 使用默认密码
auth_provider = PlainTextAuthProvider('cassandra', 'cassandra')

# 创建集群连接
try:
    cluster = Cluster(auth_provider=auth_provider)
    session = cluster.connect()
    logger.info("Cassandra connected")
except Exception as e:
    logger.error(f"Failed to connect to Cassandra: {e}")
    exit(1)

def consume_kafka():
    try:
        consumer = KafkaConsumer(
            *KAFKA_TOPICS,
            bootstrap_servers=['192.168.211.131:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='group-0',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        return consumer
    except Exception as e:
        logger.error(f"Failed to create Kafka consumer: {e}")
        exit(1)

def query_data(topic, user_id):
    query = f"""
    SELECT user_id, anime_id, happened_at
    FROM actions.{topic}
    WHERE user_id = %s
    """
    try:
        rows = session.execute(query, (int(user_id),))  # 确保 user_id 是整数
        return rows
    except Exception as e:
        logger.error(f"Failed to query data: {e}")
        return []

def insert_data(topic, user_id, anime_id, happened_at):
    try:
        session.execute(
            f"""
            INSERT INTO actions.{topic} (user_id, anime_id, happened_at)
            VALUES (%s, %s, %s)
            """,
            (
                int(user_id),  # 确保 user_id 是整数
                int(anime_id),
                datetime.datetime.fromtimestamp(happened_at)
            )
        )
    except Exception as e:
        logger.error(f"Failed to insert data: {e}")


# 消费 Kafka 消息并插入到 Cassandra
consumer = consume_kafka()
try:
    for item in consumer:
        topic = item.topic
        event = item.value
        logger.info(f"Consumed event from topic {topic}: {event}")

        # 插入数据到 Cassandra
        insert_data(topic, event['user_id'], event['anime_id'], event['happened_at'])

        # 查询数据（示例：可以根据需要调用）
        queried_data = query_data(topic, event['user_id'])
        for row in queried_data:
            logger.info(f"Queried Data: user_id={row.user_id}, anime_id={row.anime_id}, happened_at={row.happened_at}")

except KeyboardInterrupt:
    logger.info("Consumption stopped by user.")
finally:
    session.shutdown()
    cluster.shutdown()
    logger.info("Cassandra connection closed.")
