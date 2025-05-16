import json
import time
import uuid
import paho.mqtt.client as mqtt
import os

from trunk_protos.common.navi_pb2 import Navi
#from instar_protos.frame_pb2 import Frame
#from trunk_protos.common.act_status_pb2 import ActStaFrameus

client = mqtt.Client(client_id=str(uuid.uuid4()), clean_session=False)

file_name = f'oy/from/v2/navi/request/A520.json'
directory = 'json_files'
file_path = os.path.join(directory, file_name)  # 确保路径在不同的操作系统中都能正确处理
os.makedirs(directory, exist_ok=True)

def on_connect(client, userdata, flags, rc):
    # (43.01204467828439, 21.8, 64.61850418534044, 'A525', 'A523', 122, 86, {'x': 566932.1047212966, 'y': 4317884.897210781})
    topics = []
    topics.append(('+/from/v2/navi/request/A520', 0))
    # topics.append(('v2/fms/truck_status_notify', 0))
    # topics.append(('+/from/v2/navi/request/A537', 0))
    # topics.append(('oy/from/v2/navi/request/+', 0))
    # topics.append(('+/from/v2/navi/request/A545', 0))
    # topics.append(('+/port_iot/frame/A533', 0))
    # topics.append(('+/from/v2/navi/request/A523', 0))
    # topics.append(('+/from/v2/navi/request/A527', 0))
    # topics.append(('+/from/v2/navi/request/A534', 0))
    # topics.append(('+/from/v2/navi/request/A529', 0))
    # topics.append(('v1/cdi/trunk_common_stop/request', 0))
    # topics.append(('+/from/v2/navi/request/A555', 0))
    # topics.append(('v2/fms/truck_navi_notify', 0))
    # topics.append(('v2/fms/truck_status_notify', 0))
    # topics.append(('+/from/v2/act_status/notify/A539', 0))
    # topics.append(('v1/cdi/trunk_common_stop/request', 0))
    # topics.append(('oy/from/v2/act_status/notify/A531', 0))
    # topics.append(('oy/from/v2/rtg_status/notify/+', 0))
    client.subscribe(topics)


def dispatch_message(client, userdata, message):
    payload = message.payload
    topic = message.topic
    #print(time.time(), topic, payload)
    # print(topic, payload)

    che_id = topic.split('/')[-1]
    navi = Navi()

    try:
        navi.ParseFromString(payload)
    except Exception as e:
        return
    # print(topic, time.time(), navi)

    points = []
    for point in navi.waypoints:
        points.append(time.time())
        points.append({
            'pos': {'x': point.pos.x, 'y': point.pos.y},
            'heading': point.heading,
            'speeds': {
                'vmax': point.speeds.vmax
            },
            'type': point.type,
            'id': point.id,
            'lane_type': point.lane_type
        })
    # print(time.time(), topic, points)
    print(points)


    # frame = Frame()
    # try:
    #     frame.ogm
    #     frame.ParseFromString(payload)
    # except Exception as e:
    #     pass
    # print(111, frame.ads.planning_traj)
    # if "act_status" in topic:
    #     act_status = ActStatus()
    #     act_status.ParseFromString(payload)
    #     print(topic, act_status)
    # else:
    #     navi = Navi()
    #     navi.ParseFromString(payload)
    #     print(topic, navi)

client.on_connect = on_connect
client.on_message = dispatch_message
client.connect(host="10.188.73.101", port=1883, keepalive=10)

while True:
    client.loop_forever(retry_first_connection=True)
