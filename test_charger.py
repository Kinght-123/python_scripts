import json
import tkinter as tk
import uuid
from datetime import datetime, timezone
import threading

import paho.mqtt.client as mqtt

client = mqtt.Client(client_id=str(uuid.uuid4()), clean_session=False)

device_id = "01"


def generate_time():
    now = datetime.now()
    return f"{now.strftime('%Y-%m-%d-%H:%M:%S')}:{now.strftime('%f')[:3]}"


def on_connect(client, userdata, flags, rc):
    topics = []
    topics.append((f'from/v1/chargesystem/chargerstatus/notify/{device_id}', 0))  # 充电桩状态
    topics.append((f'from/v1/chargesystem/command/response/{device_id}', 0))  # 充电开始/结束
    topics.append((f'from/v1/chargesystem/chargerinform/notify/{device_id}', 0))  # 充电执行结果
    topics.append((f'from/v1/chargesystem/soc/notify/{device_id}', 0))  # 充电电量告知
    topics.append((f'from/v1/chargesystem/alignment/response/{device_id}', 0))  # 充电对位
    client.subscribe(topics)


def dispatch_message(client, userdata, message):
    payload = json.loads(message.payload)
    topic = message.topic

    if "chargerstatus" in topic:
        print("*****收到充电桩状态*****")
    elif "command/response" in topic:
        print("******收到充电开始/结束******")
    elif "chargerinform/notify" in topic:
        print("******收到充电执行结果******")
    elif "soc/notify" in topic:
        print("******收到充电电量告知--只需要订阅即可******")
    elif "alignment/response" in topic:
        print(f"******收到充电对位******")
    print(topic, payload, generate_time())


"""
- to/v1/chargesystem/chargerstatus/notify/{deviceId}  # 充电桩状态
- to/v1/chargesystem/command/request/{deviceId}  # 充电开始/结束
- to/v1/chargesystem/chargerinform/notify/{deviceId}  # 充电执行结果
- to/v1/chargesystem/alignment/request/{deviceId}  # 充电对位
"""


def header(device_id):
    return {
        "transId": str(uuid.uuid4()),
        "deviceId": device_id,
        "timestamp": generate_time()
    }


def pub_charger_status(device_id):
    data = {
        "header": header(device_id),
        "statusCode": "200"
    }

    resp = client.publish(f"to/v1/chargesystem/chargerstatus/notify/{device_id}", json.dumps(data))
    print(f"pub_charger_status---->{resp}---->{data}---->{generate_time()}")


def pub_command(device_id, command=0):
    data = {
        "header": header(device_id),
        "body": {
            "command": command  # 0: 开始插抢；1：开始充电; 2:停止充电
        }
    }
    resp = client.publish(f"to/v1/chargesystem/command/request/{device_id}", json.dumps(data))
    print(f"pub_command---->{resp}---->{data}---->{generate_time()}")


def pub_charger_inform(device_id):
    data = {
        "header": header(device_id),
        "statusCode": "200"
    }
    resp = client.publish(f"to/v1/chargesystem/chargerinform/notify/{device_id}", json.dumps(data))
    print(f"pub_charger_inform---->{resp}---->{data}---->{generate_time()}")


def pub_alignment(device_id, che_id):
    data = {
        "header": header(device_id),
        "body": {
            "vin": che_id
        }
    }
    resp = client.publish(f"to/v1/chargesystem/alignment/request/{device_id}", json.dumps(data))
    print(f"pub_alignment---->{resp}---> {data}---->{generate_time()}")


client.on_connect = on_connect
client.on_message = dispatch_message
client.connect(host="10.188.73.108", port=1883, keepalive=10)  # 需要改 host和port


def create_gui():
    root = tk.Tk()
    root.title("MQTT Publisher")

    # Device ID Entry
    tk.Label(root, text="Device ID:").grid(row=0, column=0)
    device_id_entry = tk.Entry(root)
    device_id_entry.grid(row=0, column=1)

    # Command Entry
    tk.Label(root, text="Command (0:插抢, 1:充电, 2:停止):").grid(row=1, column=0)
    command_entry = tk.Entry(root)
    command_entry.grid(row=1, column=1)

    # Che ID Entry (for alignment)
    tk.Label(root, text="Che ID (for alignment):").grid(row=2, column=0)
    che_id_entry = tk.Entry(root)
    che_id_entry.grid(row=2, column=1)

    # Buttons for publishing
    tk.Button(root, text="Publish Charger Status", command=lambda: pub_charger_status(device_id_entry.get())).grid(
        row=3, column=0)
    tk.Button(root, text="Publish Command",
              command=lambda: pub_command(device_id_entry.get(), int(command_entry.get()))).grid(row=3, column=1)
    tk.Button(root, text="Publish Charger Inform", command=lambda: pub_charger_inform(device_id_entry.get())).grid(
        row=4, column=0)
    tk.Button(root, text="Publish Alignment",
              command=lambda: pub_alignment(device_id_entry.get(), che_id_entry.get())).grid(row=4, column=1)

    root.mainloop()


if __name__ == "__main__":
    threading.Thread(target=create_gui).start()

    while True:
        client.loop_forever(retry_first_connection=True)
