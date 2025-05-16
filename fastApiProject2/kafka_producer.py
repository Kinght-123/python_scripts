from confluent_kafka import Producer

# 配置Kafka集群的地址以及生产者ID
producer = Producer({
    'bootstrap.servers': '127.0.0.1:9092',
    'client.id': 'my_producer'
})


# 定义函数发送消息并进行错误捕获
def send_message(producer, topic, message):
    try:
        producer.produce(topic, value=message)
        print(f"成功发送消息：{message}")
    except Exception as e:
        print(f"消息发送失败：{e}")


# 发送一条消息到指定Topic
send_message(producer, '123', 'Hello, Kafka!')

# 刷新并关闭生产者，确保所有消息被发送
producer.flush()
