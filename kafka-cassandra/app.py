from flask import Flask, request
from datetime import datetime
from kafka import KafkaProducer
from json import dumps

app = Flask(__name__)

"""
允许客户端通过 POST 请求发送用户行为数据（点击和浏览）
将前端上报的用户行为数据及时保存到队列中，供后续消费
"""
# 创建了一个 Kafka 客户端，用于将消息发送到 Kafka 主题

producer = KafkaProducer(
    bootstrap_servers=['192.168.211.131:9092'],     # 指定要连接的 Kafka 代理列表
    value_serializer=lambda x: dumps(x).encode('utf-8')     # 指定用于将 Python 对象序列化为字节数组的函数
)


@app.route("/clicks", methods=['POST'])
def post_clicks():
    # data: { user_id, anime_id }
    data = request.json
    data['happened_at'] = int(datetime.timestamp(datetime.now()))
    print(data)

    producer.send('clicks', value=data)     # 使用 producer 将 data 字典作为值发送到 clicks 主题

    return 'ok'


@app.route("/views", methods=['POST'])
def post_views():
    # data: { user_id, anime_id }
    data = request.json
    data['happened_at'] = int(datetime.timestamp(datetime.now()))
    print(data)

    producer.send('views', value=data)

    return 'ok'



if __name__ == "__main__":
    
    app.run(host='0.0.0.0', port=5004, debug=True)
