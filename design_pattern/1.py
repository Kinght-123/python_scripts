"""
    - 通过mqtt订阅protobuf类型的数据，并解析获取特定的字段
"""

from datetime import datetime
import paho.mqtt.client as mqtt
from trunk_protos.common.act_status_pb2 import ActStatus

# MQTT服务器配置
MQTT_BROKER = '10.188.73.108'  # 替换为你的MQTT服务器地址
MQTT_PORT = 1884  # MQTT服务器端口
MQTT_TOPIC = 'oy/from/v2/act_status/notify/#'  # 订阅的主题
MQTT_USERNAME = 'tect-oy'  # 替换为你的用户名
MQTT_PASSWORD = 'tect-oy@Trunk'  # 替换为你的密码


# MQTT消息回调函数
def on_message(client, userdata, message):
    payload = message.payload
    act_status = ActStatus()
    act_status.ParseFromString(payload)
    print(f'che_id: {act_status.header.che_id}')
    # print(f'act_status:{act_status} type:{type(act_status)}')
    # print(f"Received message '{act_status}' on topic '{message.topic}' with QoS {message.qos}")


# 创建MQTT客户端实例
client = mqtt.Client()

# 设置用户名和密码
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)


# 连接到MQTT服务器
def connect_mqtt():
    client.connect(MQTT_BROKER, MQTT_PORT, 60)


# 启动MQTT客户端循环
def start_mqtt():
    client.on_message = on_message  # 设置消息回调函数
    connect_mqtt()  # 连接到MQTT服务器
    client.subscribe(MQTT_TOPIC)  # 订阅主题
    client.loop_start()  # 启动客户端循环


# 停止MQTT客户端循环
def stop_mqtt():
    client.loop_stop()  # 停止客户端循环
    client.disconnect()  # 断开连接


# 主函数
def main():
    try:
        start_mqtt()  # 启动MQTT服务
        print("MQTT service started. Waiting for messages...")
        while True:
            pass  # 保持服务运行
    except KeyboardInterrupt:
        print("Stopping MQTT service...")
        stop_mqtt()  # 停止MQTT服务
        print("MQTT service stopped.")


if __name__ == "__main__":
    main()
