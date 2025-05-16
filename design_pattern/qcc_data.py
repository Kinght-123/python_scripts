import json

import paho.mqtt.client as mqtt

# MQTT服务器的地址和端口
MQTT_BROKER = '10.188.73.108'
MQTT_PORT = 1883
# ('ECS/RMG/R302', 0), ('ECS/RMG/R313', 0),('ECS/RMG/R314', 0), ('ECS/RMG/R314', 0), ('ECS/RMG/R306', 0)
MQTT_TOPIC = [('ECS/QC/QC10', 0)]

id = '6'


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode('utf-8'))
    for i in range(len(data['Lane'])):
        if id in data['Lane'][i]["LaneCode"]:
            print(
                f'LaneCode: {data["Lane"][i]["LaneCode"]} - TrkOffsetPos: {data["Lane"][i]["TrkOffsetPos"]} - {data["UptTime"]}')




client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)

client.loop_forever()
