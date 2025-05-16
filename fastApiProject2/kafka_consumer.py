from confluent_kafka import Consumer

# 配置消费者参数，包括消费者组ID和从最早消息开始读取
consumer = Consumer({
    'bootstrap.servers': '127.0.0.1:9092',
    'group.id': 'my_group',
    'auto.offset.reset': 'earliest'
})

# 订阅指定的Topic列表
consumer.subscribe(['123'])

# 持续轮询消息
while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print(f"读取消息出错：{msg.error()}")
    else:
        print(f"消费成功：{msg.value().decode('utf-8')}")

# 关闭消费连接
consumer.close()
