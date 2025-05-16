import logging
import logging.config
from functools import wraps
from threading import Thread

import paho.mqtt.client as mqtt
from google.protobuf.json_format import MessageToDict
from trunk_protos.common.act_status_pb2 import ActStatus


def try_exc(f):
    @wraps(f)
    def inner(*args, **kwargs):
        try:
            ret = f(*args, **kwargs)
        except Exception as e:
            logging.exception(e)
            exit()
        else:
            return ret

    return inner


def timer(f):
    @wraps(f)
    def inner(*args, **kwargs):
        t1 = time.time()
        ret = f(*args, **kwargs)
        t2 = time.time()
        print(f'<{f.__name__}> running time: {t2 - t1} s, payload len: {len(args[-1].payload)} bytes')
        return ret

    return inner


class MqttHandler:

    def __init__(self, host, port, username=None, password=None):
        self.host = host
        self.port = int(port)  # port不是int会报错
        self.client = mqtt.Client(client_id='mqtt_test_wyq_local')
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.client.username_pw_set(username, password)

        self.last_x = 0  # 检测点位是否有明显跳变

        for topic, callback_name in MQTT_TOPIC_CALLBACK_MAPPING.items():
            callback = getattr(self, f"{callback_name}")
            self.client.message_callback_add(topic, callback)

    def on_connect(self, client, userdata, flags, rc):
        logging.info('MQTT Handler runing at: {}:{}'.format(self.host, self.port))
        for topic in MQTT_TOPIC_CALLBACK_MAPPING:
            client.subscribe(topic, 0)

    def on_message(self, client, userdata, data):
        logging.warning(data.topic + ' ' + str(data.payload))

    def on_disconnect(self, client, userdata, rc):
        logging.error(f"Connection disconnect of mqtt-broker {self.host}:{self.port}")

    def _thread_main(self):
        try:
            self.client.connect(self.host, self.port, keepalive=30)  # 一般不要用默认60s
            self.client.loop_forever(retry_first_connection=True)  # 没有loop_forever，连接过期断开后，不会发起重连
            print('mqtt thread quit...')
        except Exception as e:
            logging.exception(e)

    def run_forever(self):
        thread = Thread(target=self._thread_main, name='mqtt_handler')
        thread.setDaemon(True)
        thread.start()

    @try_exc
    def act_status_callback(self, client, userdata, data):
        msg = ActStatus()
        msg.ParseFromString(data.payload)
        che_id = msg.header.che_id
        if SUB_CHE_IDS and che_id not in SUB_CHE_IDS:
            return
        print(f'{che_id} <act_status_callback>: '
              f'topic {data.topic}: '
              # f'{MessageToDict(msg, including_default_value_fields=True, preserving_proto_field_name=True)}'
              f'che_id: {che_id} ip: {msg.host}')


    # @timer
    def publish(self, topic, payload):
        info = self.client.publish(topic, payload)
        if info.rc != mqtt.MQTT_ERR_SUCCESS:
            logging.error('MqttHandler publish to {}'.format(topic))
        return info.rc

    def publish_thread(self, topic, payload, thread_name):
        thread = Thread(target=self.publish, args=(topic, payload), name=thread_name)
        thread.setDaemon(True)
        thread.start()

    def close(self):
        self.client.disconnect()
        print('mqtt_handler close...')


if __name__ == '__main__':
    import signal
    import time
    import os

    MQTT_CONFIG = {
        'host': os.environ.get('MQTT_HOST', '10.188.73.108'),
        'port': os.environ.get('MQTT_PORT', 1884),
        'username': 'tect-oy',
        'password': 'tect-oy@Trunk',
    }

    MQTT_TOPIC_CALLBACK_MAPPING = {
        "+/from/v2/act_status/notify/+": "act_status_callback",
    }

    SUB_CHE_IDS = {
    }


    def signal_handler(signal, frame):
        raise KeyboardInterrupt


    try:
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

        mqtt_handler = MqttHandler(**MQTT_CONFIG)
        mqtt_handler.run_forever()
        while True:
            time.sleep(10)
    except (KeyboardInterrupt, InterruptedError):
        logging.error("Manually Interrupted!")
    finally:
        logging.error("matt_handler stopping!")
