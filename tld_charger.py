import json
import threading
import tkinter as tk
import uuid
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

client = mqtt.Client(client_id=str(uuid.uuid4()), clean_session=False)


def generate_timestamp():
    # 获取当前的 UTC 时间
    now_utc = datetime.now(timezone.utc)

    # 格式化时间为 yyyyMMddTHHmmssZ
    return now_utc.strftime('%Y%m%dT%H%M%SZ')


def on_connect(client, userdata, flags, rc):
    topics = []
    # topics.append(('from/v1/chargesystem/chargerstatus/notify/#', 0))  # 充电桩状态
    # topics.append(('from/v1/chargesystem/command/response/#', 0))  # 充电开始/结束
    # topics.append(('from/v1/chargesystem/chargerinform/notify/#', 0))  # 充电执行结果
    # topics.append(('from/v1/chargesystem/soc/notify/#', 0))  # 充电电量告知
    # topics.append(('from/v1/chargesystem/alignment/response/#', 0))  # 充电对位
    # client.subscribe(topics)


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
    print(topic, payload)


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
        "timestamp": generate_timestamp()
    }


def pub_charger_status(device_id, charger_status):
    data = {
        "header": header(device_id),
        "chargerStatus": charger_status,
    }

    resp = client.publish(f"from/v1/chargesystem/chargerstatus/notify/{device_id}", json.dumps(data))
    print(f"发布充电状态---->{resp}---->{data}")


def pub_charger_inform(device_id, charger_info):
    data = {
        "header": header(device_id),
        "chargerInform": charger_info
    }
    resp = client.publish(f"from/v1/chargesystem/chargerinform/notify/{device_id}", json.dumps(data))
    print(f"充电系统插枪、拔枪状态通知---->{resp}---->{data}")


client.on_connect = on_connect
client.on_message = dispatch_message
client.connect(host="10.11.1.51", port=1888, keepalive=10)  # 需要改 host和port


def create_gui():
    root = tk.Tk()
    root.title("MQTT Publisher")

    # Device ID Entry
    device_id_var = tk.StringVar(value="03")
    tk.Label(root, text="Device ID:").grid(row=0, column=0)
    device_id_entry = tk.Entry(root, textvariable=device_id_var)
    device_id_entry.grid(row=0, column=1)

    # charger status Entry
    tk.Label(root, text="充电状态变更 (0: 空闲； 1: 工作； 2: 故障)").grid(row=1, column=0)
    charger_status = tk.Entry(root)
    charger_status.grid(row=1, column=1)

    # charger_info
    tk.Label(root, text="充电系统插枪、拔枪状态通知 \n"
    "0: 故障; 1: 插抢到位; 2: 充电完成; 3: 停止充电; 4: 插抢失败; 5: 拔枪失败; 6: 开始插抢").grid(row=2, column=0)
    charger_info = tk.Entry(root)
    charger_info.grid(row=2, column=1)

    # Add some blank rows
    for i in range(3, 5):
        tk.Label(root, text="").grid(row=i, column=0, columnspan=2)


    # Buttons for publishing
    tk.Button(root, text="充电状态变更", command=lambda: pub_charger_status(device_id_entry.get(), charger_status.get())).grid(
        row=5, column=0)

    tk.Button(root, text="充电系统插枪、拔枪状态通知",
              command=lambda: pub_charger_inform(device_id_entry.get(), charger_info.get(), )).grid(row=5, column=1)


    root.mainloop()


if __name__ == "__main__":
    create_gui()
