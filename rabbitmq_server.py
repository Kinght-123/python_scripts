# receive.py
import pika
import time
import sys

# --- 1. 建立连接 ---
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
# 同样需要声明队列，以防消费者先于生产者启动
# 这确保了消费者尝试连接的队列是存在的
channel.queue_declare(queue='hello_queue')

print(' [*] Waiting for messages. To exit press CTRL+C')


# --- 3. 定义消息处理回调函数 ---
def callback(ch, method, properties, body):
    """当收到消息时，pika库会调用这个函数"""
    print(f" [x] Received '{body.decode('utf-8')}'")

    # 模拟处理任务所需的时间
    # time.sleep(body.count(b'.')) # 可以取消注释来模拟耗时任务

    # --- 关键：发送确认 (Acknowledgement) ---
    # 告诉 RabbitMQ 这条消息已经被成功接收和处理
    # 只有收到确认后，RabbitMQ 才会从队列中删除该消息
    # 如果消费者在处理过程中挂掉而没有发送 ACK，RabbitMQ 会将消息重新发送给其他消费者
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(" [x] Done")


# --- 4. 订阅队列并开始消费 ---
# 指定 'hello_queue' 队列的消息应该由 'callback' 函数处理
# auto_ack=False 表示我们需要手动发送确认，这是推荐的做法，保证消息不丢失
channel.basic_consume(queue='hello_queue',
                      on_message_callback=callback,
                      auto_ack=False)  # 手动确认

# 进入一个无限循环，等待消息并调用回调函数
# 按 CTRL+C 可以中断程序
try:
    channel.start_consuming()
except KeyboardInterrupt:
    print(' Interrupted')
    # 尝试优雅地关闭连接
    try:
        connection.close()
    except Exception as e:
        print(f"关闭连接时出错: {e}")
    sys.exit(0)
