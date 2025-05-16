import pika
import logging
from google.protobuf.json_format import MessageToDict
from trunk_protos.common.arrive_status_pb2 import ArriveStatus

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RabbitMQClient:
    def __init__(self, host: str = 'localhost', port: int = 5672, username: str = 'guest', password: str = 'guest'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None
        self.channel = None

    def connect(self):
        """建立到 RabbitMQ 的连接"""
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            virtual_host='/prod',
            credentials=credentials
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def declare_exchange(self, exchange_name: str, exchange_type: str = 'topic'):
        """声明交换机"""
        self.channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type,
                                      durable=True)  # durable=True声明持久化存储

    def declare_queue(self, queue_name: str):
        """声明队列"""
        return self.channel.queue_declare(queue=queue_name, durable=True)

    def bind_queue(self, queue_name: str, exchange_name: str, routing_key: str):
        """将队列绑定到交换机"""
        self.channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)

    def start_consuming(self, queue_name: str, routing_key: str, on_message_callback):
        """开始消费消息"""
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=on_message_callback,
            auto_ack=True
        )
        logger.info(f'Starting to consume messages from queue: {queue_name} with routing key: {routing_key}')
        self.channel.start_consuming()

    def close(self):
        """关闭连接"""
        if self.connection and self.connection.is_open:
            self.connection.close()


def on_message(ch, method, properties, body):
    """处理接收到的消息"""
    p = ArriveStatus()
    p.ParseFromString(body)
    data = MessageToDict(p)
    print(type(data))
    print(data)


def main():
    # 配置
    exchange_name = 'fmp.v2.e.topic.cmd'
    queue_name = 'fmp.v2.q.cmd.ad1.YccApp'
    routing_key = 'fmp.v2.k.cmd.yc_arrive_status.ycc.#'

    # 创建 RabbitMQ 客户端
    client = RabbitMQClient(host='10.188.73.108', port=5672, username='trunk', password='Trunk@123')
    client.connect()
    client.declare_exchange(exchange_name, 'topic', )  # 绑定交换机
    client.declare_queue(queue_name)  # 绑定消息队列
    client.bind_queue(queue_name, exchange_name, routing_key)  # 交换机接收到的消息通过路由键转发到指定的消息队列

    # 开始消费消息
    client.start_consuming(queue_name, routing_key, on_message)


if __name__ == '__main__':
    main()
