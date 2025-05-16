# send.py
import pika
import sys

# --- 1. 建立连接 ---
# 连接到本地 RabbitMQ 服务器 (默认端口 5672)
# 如果 RabbitMQ 在不同机器上，请修改 'localhost'
try:
    credentials = pika.PlainCredentials('guest', 'Kinght123')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='127.0.0.1',
            port=5672,
            credentials=credentials
        )
    )
    channel = connection.channel()
except pika.exceptions.AMQPConnectionError as e:
    print(f"无法连接到 RabbitMQ 服务: {e}")
    sys.exit(1)

# --- 2. 声明队列 ---
# 确保名为 'hello_queue' 的队列存在。如果不存在，则创建它。
# 这是一个幂等操作，重复执行是安全的。
channel.queue_declare(queue='hello_queue')

# --- 3. 准备并发送消息 ---
# 从命令行参数获取消息，否则使用默认消息
message = ' '.join(sys.argv[1:]) or "Hello RabbitMQ from Python!"

# 使用默认交换机 (exchange='') 将消息发布到 'hello_queue'
# 默认交换机是一种特殊的直连交换机，它会查找与 routing_key 同名的队列
channel.basic_publish(exchange='',
                      routing_key='hello_queue',  # 指定目标队列名
                      body=message.encode('utf-8'))  # 消息体需要是 bytes 类型

print(f" [x] Sent '{message}'")

# --- 4. 关闭连接 ---
# 清理资源，关闭连接
connection.close()
