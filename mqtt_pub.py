import json
import time
import uuid
from datetime import datetime

import paho.mqtt.client as mqtt
from google.protobuf.json_format import ParseDict
from trunk_protos.common.act_status_pb2 import ActStatus
from trunk_protos.common.navi_pb2 import Navi

client = mqtt.Client(client_id=str(uuid.uuid4()), clean_session=False)

data = [
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.103030812,
            "y": 4317935.245554973,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.2114793959,
            "y": 4317934.757970423,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.3102621876,
            "y": 4317934.2691902295,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.3996964914,
            "y": 4317933.779253647,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.4800996108,
            "y": 4317933.288199921,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.5517888499,
            "y": 4317932.796068303,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.6150815127,
            "y": 4317932.302898042,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.6702949028,
            "y": 4317931.808728391,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.7177463244,
            "y": 4317931.313598595,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.7577530815,
            "y": 4317930.817547908,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.7906324777,
            "y": 4317930.320615579,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.8167018172,
            "y": 4317929.822840859,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.836278404,
            "y": 4317929.324262996,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.8496795415,
            "y": 4317928.82492124,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.8572225341,
            "y": 4317928.32485484,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.8592246857,
            "y": 4317927.82410305,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.8560032996,
            "y": 4317927.322705115,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.8478756807,
            "y": 4317926.820700289,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.8351591321,
            "y": 4317926.318127821,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.8181709584,
            "y": 4317925.81502696,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.7972284628,
            "y": 4317925.311436954,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.7726489496,
            "y": 4317924.807397056,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.7447497228,
            "y": 4317924.302946516,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.7138480863,
            "y": 4317923.798124584,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.680261344,
            "y": 4317923.292970508,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.6443067994,
            "y": 4317922.78752354,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.6063017568,
            "y": 4317922.281822927,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.5665635201,
            "y": 4317921.775907921,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.5254093934,
            "y": 4317921.269817772,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.4831566805,
            "y": 4317920.763591732,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.440122685,
            "y": 4317920.257269047,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.3966247111,
            "y": 4317919.75088897,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.3529800625,
            "y": 4317919.244490747,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.3095060434,
            "y": 4317918.7381136315,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.2665199577,
            "y": 4317918.231796874,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.2243391093,
            "y": 4317917.725579722,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.1832808017,
            "y": 4317917.2195014255,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.1436623394,
            "y": 4317916.713601236,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.1058010261,
            "y": 4317916.207918404,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.0700141656,
            "y": 4317915.702492177,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.0366190618,
            "y": 4317915.1973618055,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.005933019,
            "y": 4317914.692566541,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566828.9782733407,
            "y": 4317914.188145633,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566828.953957331,
            "y": 4317913.684138331,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566828.9333022938,
            "y": 4317913.180583885,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566828.9166255329,
            "y": 4317912.6775215445,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566828.9042443525,
            "y": 4317912.174990559,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566828.8964760562,
            "y": 4317911.673030181,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566828.893637948,
            "y": 4317911.171679658,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566828.8960473319,
            "y": 4317910.670978241,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566828.9040215119,
            "y": 4317910.17096518,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566828.9178777917,
            "y": 4317909.671679724,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566828.9379334754,
            "y": 4317909.173161124,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566828.9645058668,
            "y": 4317908.675448629,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566828.9979122699,
            "y": 4317908.17858149,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.0384699885,
            "y": 4317907.682598956,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.0864963267,
            "y": 4317907.187540279,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.1423085883,
            "y": 4317906.693444706,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.2062240771,
            "y": 4317906.200351488,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.2785600972,
            "y": 4317905.708299875,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.3596339526,
            "y": 4317905.217329118,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.449762947,
            "y": 4317904.727478466,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.5492643844,
            "y": 4317904.23878717,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.342031713073164,
        "id": "",
        "pos": {
            "x": 566829.6498669286,
            "y": 4317903.788055021,
            "yaw": -1.342031713073164,
            "z": 0
        },
        "speeds": {
            "vmax": 10,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 7
    },
    {
        "driving_direction": 1,
        "heading": -1.3429154782732016,
        "id": "1366_2",
        "pos": {
            "x": 566829.7629753174,
            "y": 4317903.300316008,
            "yaw": -1.3429154782732016,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3429040557382,
        "id": "1366_2",
        "pos": {
            "x": 566829.8756681336,
            "y": 4317902.8143927865,
            "yaw": -1.3429040557382,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3428909908248803,
        "id": "1366_2",
        "pos": {
            "x": 566829.9885165319,
            "y": 4317902.327825375,
            "yaw": -1.3428909908248803,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.342877026345044,
        "id": "1366_2",
        "pos": {
            "x": 566830.1015534166,
            "y": 4317901.840476338,
            "yaw": -1.342877026345044,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.342863337027875,
        "id": "1366_2",
        "pos": {
            "x": 566830.2146749278,
            "y": 4317901.3527930835,
            "yaw": -1.342863337027875,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.34284989940778,
        "id": "1366_2",
        "pos": {
            "x": 566830.3276547902,
            "y": 4317900.865750512,
            "yaw": -1.34284989940778,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3428367127522625,
        "id": "1366_2",
        "pos": {
            "x": 566830.4407368242,
            "y": 4317900.378296944,
            "yaw": -1.3428367127522625,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3428238032841024,
        "id": "1366_2",
        "pos": {
            "x": 566830.553830319,
            "y": 4317899.8908228725,
            "yaw": -1.3428238032841024,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3428111344271676,
        "id": "1366_2",
        "pos": {
            "x": 566830.6668596023,
            "y": 4317899.403653888,
            "yaw": -1.3428111344271676,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3427987066884013,
        "id": "1366_2",
        "pos": {
            "x": 566830.7799794441,
            "y": 4317898.916122357,
            "yaw": -1.3427987066884013,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.342786550075355,
        "id": "1366_2",
        "pos": {
            "x": 566830.893053448,
            "y": 4317898.4288155995,
            "yaw": -1.342786550075355,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.342774612289325,
        "id": "1366_2",
        "pos": {
            "x": 566831.0061250417,
            "y": 4317897.941545891,
            "yaw": -1.342774612289325,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.342762936744625,
        "id": "1366_2",
        "pos": {
            "x": 566831.1192757434,
            "y": 4317897.453961422,
            "yaw": -1.342762936744625,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.342751481492433,
        "id": "1366_2",
        "pos": {
            "x": 566831.232338435,
            "y": 4317896.966781791,
            "yaw": -1.342751481492433,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.342740275765041,
        "id": "1366_2",
        "pos": {
            "x": 566831.3454455882,
            "y": 4317896.479435641,
            "yaw": -1.342740275765041,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3427292983976926,
        "id": "1366_2",
        "pos": {
            "x": 566831.4586037938,
            "y": 4317895.991894082,
            "yaw": -1.3427292983976926,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3427185469670115,
        "id": "1366_2",
        "pos": {
            "x": 566831.5716797899,
            "y": 4317895.504730737,
            "yaw": -1.3427185469670115,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3427080522217838,
        "id": "1366_2",
        "pos": {
            "x": 566831.6848160585,
            "y": 4317895.017331231,
            "yaw": -1.3427080522217838,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3426977712667991,
        "id": "1366_2",
        "pos": {
            "x": 566831.7979623218,
            "y": 4317894.529911676,
            "yaw": -1.3426977712667991,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3426877088238935,
        "id": "1366_2",
        "pos": {
            "x": 566831.9110723473,
            "y": 4317894.042670721,
            "yaw": -1.3426877088238935,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3426778806196047,
        "id": "1366_2",
        "pos": {
            "x": 566832.0242315441,
            "y": 4317893.555239951,
            "yaw": -1.3426778806196047,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3426682774167154,
        "id": "1366_2",
        "pos": {
            "x": 566832.1373732153,
            "y": 4317893.067906173,
            "yaw": -1.3426682774167154,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3426588929273549,
        "id": "1366_2",
        "pos": {
            "x": 566832.250511207,
            "y": 4317892.580609243,
            "yaw": -1.3426588929273549,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.342649730659774,
        "id": "1366_2",
        "pos": {
            "x": 566832.363687353,
            "y": 4317892.093168503,
            "yaw": -1.342649730659774,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3426407821575421,
        "id": "1366_2",
        "pos": {
            "x": 566832.4768316026,
            "y": 4317891.605885162,
            "yaw": -1.3426407821575421,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.342632063464067,
        "id": "1366_2",
        "pos": {
            "x": 566832.5899916787,
            "y": 4317891.118553208,
            "yaw": -1.342632063464067,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.342623544887846,
        "id": "1366_2",
        "pos": {
            "x": 566832.7031763257,
            "y": 4317890.63113451,
            "yaw": -1.342623544887846,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.342615245869702,
        "id": "1366_2",
        "pos": {
            "x": 566832.8163328171,
            "y": 4317890.143855648,
            "yaw": -1.342615245869702,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3426071612166783,
        "id": "1366_2",
        "pos": {
            "x": 566832.9295092297,
            "y": 4317889.656509118,
            "yaw": -1.3426071612166783,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3425992934199378,
        "id": "1366_2",
        "pos": {
            "x": 566833.0426942917,
            "y": 4317889.169142989,
            "yaw": -1.3425992934199378,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3425916254379668,
        "id": "1366_2",
        "pos": {
            "x": 566833.1558723444,
            "y": 4317888.6818242185,
            "yaw": -1.3425916254379668,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3425841760999324,
        "id": "1366_2",
        "pos": {
            "x": 566833.2690594358,
            "y": 4317888.194483241,
            "yaw": -1.3425841760999324,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.34257694080066,
        "id": "1366_2",
        "pos": {
            "x": 566833.3822517854,
            "y": 4317887.707135871,
            "yaw": -1.34257694080066,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3425698912523405,
        "id": "1366_2",
        "pos": {
            "x": 566833.4954457758,
            "y": 4317887.219797222,
            "yaw": -1.3425698912523405,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.342563077694482,
        "id": "1366_2",
        "pos": {
            "x": 566833.6086379342,
            "y": 4317886.732481786,
            "yaw": -1.342563077694482,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3425564419730949,
        "id": "1366_2",
        "pos": {
            "x": 566833.7218444363,
            "y": 4317886.2451194655,
            "yaw": -1.3425564419730949,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.342550043602034,
        "id": "1366_2",
        "pos": {
            "x": 566833.8350487612,
            "y": 4317885.75778093,
            "yaw": -1.342550043602034,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3425438308213407,
        "id": "1366_2",
        "pos": {
            "x": 566833.9482403756,
            "y": 4317885.270511067,
            "yaw": -1.3425438308213407,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3425378063279088,
        "id": "1366_2",
        "pos": {
            "x": 566834.0614679292,
            "y": 4317884.783099997,
            "yaw": -1.3425378063279088,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3425320290860423,
        "id": "1366_2",
        "pos": {
            "x": 566834.1746769615,
            "y": 4317884.295781707,
            "yaw": -1.3425320290860423,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.342526420344613,
        "id": "1366_2",
        "pos": {
            "x": 566834.2878789898,
            "y": 4317883.808506165,
            "yaw": -1.342526420344613,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.342521029128168,
        "id": "1366_2",
        "pos": {
            "x": 566834.4011179591,
            "y": 4317883.321083764,
            "yaw": -1.342521029128168,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.342515836618074,
        "id": "1366_2",
        "pos": {
            "x": 566834.5143260033,
            "y": 4317882.833806176,
            "yaw": -1.342515836618074,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3425108537197352,
        "id": "1366_2",
        "pos": {
            "x": 566834.6275470075,
            "y": 4317882.346484056,
            "yaw": -1.3425108537197352,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.342506063468357,
        "id": "1366_2",
        "pos": {
            "x": 566834.7407901828,
            "y": 4317881.859077315,
            "yaw": -1.342506063468357,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3425014783722446,
        "id": "1366_2",
        "pos": {
            "x": 566834.8539914307,
            "y": 4317881.371861387,
            "yaw": -1.3425014783722446,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424971045945067,
        "id": "1366_2",
        "pos": {
            "x": 566834.9672386767,
            "y": 4317880.884457395,
            "yaw": -1.3424971045945067,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424929151452054,
        "id": "1366_2",
        "pos": {
            "x": 566835.0804801708,
            "y": 4317880.397087622,
            "yaw": -1.3424929151452054,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424889399752995,
        "id": "1366_2",
        "pos": {
            "x": 566835.1936686551,
            "y": 4317879.909955006,
            "yaw": -1.3424889399752995,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424851702269238,
        "id": "1366_2",
        "pos": {
            "x": 566835.306949616,
            "y": 4317879.422432965,
            "yaw": -1.3424851702269238,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.342481595221968,
        "id": "1366_2",
        "pos": {
            "x": 566835.4201833565,
            "y": 4317878.935122268,
            "yaw": -1.342481595221968,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424782202445753,
        "id": "1366_2",
        "pos": {
            "x": 566835.5333838263,
            "y": 4317878.447962421,
            "yaw": -1.3424782202445753,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424750555495175,
        "id": "1366_2",
        "pos": {
            "x": 566835.6466753031,
            "y": 4317877.960418153,
            "yaw": -1.3424750555495175,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424721008504272,
        "id": "1366_2",
        "pos": {
            "x": 566835.7598949831,
            "y": 4317877.473189633,
            "yaw": -1.3424721008504272,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424693443891629,
        "id": "1366_2",
        "pos": {
            "x": 566835.8731287699,
            "y": 4317876.985906728,
            "yaw": -1.3424693443891629,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424667810037476,
        "id": "1366_2",
        "pos": {
            "x": 566835.9864110154,
            "y": 4317876.498421166,
            "yaw": -1.3424667810037476,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424644384161437,
        "id": "1366_2",
        "pos": {
            "x": 566836.0996100438,
            "y": 4317876.011299128,
            "yaw": -1.3424644384161437,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424622904121073,
        "id": "1366_2",
        "pos": {
            "x": 566836.2128855251,
            "y": 4317875.5238530645,
            "yaw": -1.3424622904121073,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424603402012902,
        "id": "1366_2",
        "pos": {
            "x": 566836.3261517714,
            "y": 4317875.036451254,
            "yaw": -1.3424603402012902,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424586187702194,
        "id": "1366_2",
        "pos": {
            "x": 566836.4393232223,
            "y": 4317874.549461414,
            "yaw": -1.3424586187702194,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424570937093008,
        "id": "1366_2",
        "pos": {
            "x": 566836.5526491546,
            "y": 4317874.061810421,
            "yaw": -1.3424570937093008,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424557824901437,
        "id": "1366_2",
        "pos": {
            "x": 566836.6658922648,
            "y": 4317873.574518954,
            "yaw": -1.3424557824901437,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424546730977527,
        "id": "1366_2",
        "pos": {
            "x": 566836.7790872538,
            "y": 4317873.087437228,
            "yaw": -1.3424546730977527,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424537805139791,
        "id": "1366_2",
        "pos": {
            "x": 566836.8924143794,
            "y": 4317872.599789124,
            "yaw": -1.3424537805139791,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424530957098617,
        "id": "1366_2",
        "pos": {
            "x": 566837.0056267907,
            "y": 4317872.112636376,
            "yaw": -1.3424530957098617,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424526405392176,
        "id": "1366_2",
        "pos": {
            "x": 566837.1188749708,
            "y": 4317871.6253309855,
            "yaw": -1.3424526405392176,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424523768624081,
        "id": "1366_2",
        "pos": {
            "x": 566837.2321755023,
            "y": 4317871.137801126,
            "yaw": -1.3424523768624081,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424523432425342,
        "id": "1366_2",
        "pos": {
            "x": 566837.3453491669,
            "y": 4317870.650817493,
            "yaw": -1.3424523432425342,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.342452528310694,
        "id": "1366_2",
        "pos": {
            "x": 566837.4586607367,
            "y": 4317870.163240302,
            "yaw": -1.342452528310694,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424529229396929,
        "id": "1366_2",
        "pos": {
            "x": 566837.571926323,
            "y": 4317869.675860334,
            "yaw": -1.3424529229396929,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424535408125617,
        "id": "1366_2",
        "pos": {
            "x": 566837.685068618,
            "y": 4317869.189009763,
            "yaw": -1.3424535408125617,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.342454380725634,
        "id": "1366_2",
        "pos": {
            "x": 566837.7984383439,
            "y": 4317868.701178942,
            "yaw": -1.342454380725634,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424554581654848,
        "id": "1366_2",
        "pos": {
            "x": 566837.9116600412,
            "y": 4317868.213982979,
            "yaw": -1.3424554581654848,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.342456750888451,
        "id": "1366_2",
        "pos": {
            "x": 566838.0248717959,
            "y": 4317867.726827195,
            "yaw": -1.342456750888451,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.342458261592453,
        "id": "1366_2",
        "pos": {
            "x": 566838.138200951,
            "y": 4317867.2391631175,
            "yaw": -1.342458261592453,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424600132330238,
        "id": "1366_2",
        "pos": {
            "x": 566838.2513691502,
            "y": 4317866.752188034,
            "yaw": -1.3424600132330238,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424620050650609,
        "id": "1366_2",
        "pos": {
            "x": 566838.3646624095,
            "y": 4317866.264670674,
            "yaw": -1.3424620050650609,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.342464222194033,
        "id": "1366_2",
        "pos": {
            "x": 566838.4779409657,
            "y": 4317865.777211938,
            "yaw": -1.342464222194033,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424666828061695,
        "id": "1366_2",
        "pos": {
            "x": 566838.5910453148,
            "y": 4317865.290497689,
            "yaw": -1.3424666828061695,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424693777370442,
        "id": "1366_2",
        "pos": {
            "x": 566838.7044327841,
            "y": 4317864.802559407,
            "yaw": -1.3424693777370442,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424723119678328,
        "id": "1366_2",
        "pos": {
            "x": 566838.8176499153,
            "y": 4317864.315347912,
            "yaw": -1.3424723119678328,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424754929382712,
        "id": "1366_2",
        "pos": {
            "x": 566838.930832618,
            "y": 4317863.828277814,
            "yaw": -1.3424754929382712,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424789241537298,
        "id": "1366_2",
        "pos": {
            "x": 566839.0441743054,
            "y": 4317863.340516224,
            "yaw": -1.3424789241537298,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424826160784629,
        "id": "1366_2",
        "pos": {
            "x": 566839.1573182992,
            "y": 4317862.853597544,
            "yaw": -1.3424826160784629,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424865384064115,
        "id": "1366_2",
        "pos": {
            "x": 566839.27060706,
            "y": 4317862.36604743,
            "yaw": -1.3424865384064115,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.342490744619787,
        "id": "1366_2",
        "pos": {
            "x": 566839.3838772606,
            "y": 4317861.8785681985,
            "yaw": -1.342490744619787,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424951936353575,
        "id": "1366_2",
        "pos": {
            "x": 566839.4969372954,
            "y": 4317861.391983914,
            "yaw": -1.3424951936353575,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3424999210965904,
        "id": "1366_2",
        "pos": {
            "x": 566839.6103452803,
            "y": 4317860.903891975,
            "yaw": -1.3424999210965904,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3425049100477198,
        "id": "1366_2",
        "pos": {
            "x": 566839.7235306568,
            "y": 4317860.416747379,
            "yaw": -1.3425049100477198,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3425101713416312,
        "id": "1366_2",
        "pos": {
            "x": 566839.8367120981,
            "y": 4317859.929608399,
            "yaw": -1.3425101713416312,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.342515713027755,
        "id": "1366_2",
        "pos": {
            "x": 566839.9500359673,
            "y": 4317859.441844453,
            "yaw": -1.342515713027755,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3425215179773633,
        "id": "1366_2",
        "pos": {
            "x": 566840.0631220147,
            "y": 4317858.9550915975,
            "yaw": -1.3425215179773633,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.342527626439975,
        "id": "1366_2",
        "pos": {
            "x": 566840.176441733,
            "y": 4317858.467319775,
            "yaw": -1.342527626439975,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3425340071077034,
        "id": "1366_2",
        "pos": {
            "x": 566840.2896662108,
            "y": 4317857.979944088,
            "yaw": -1.3425340071077034,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3425406942053366,
        "id": "1366_2",
        "pos": {
            "x": 566840.4027389844,
            "y": 4317857.493206982,
            "yaw": -1.3425406942053366,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3425476757464194,
        "id": "1366_2",
        "pos": {
            "x": 566840.5161128199,
            "y": 4317857.005158784,
            "yaw": -1.3425476757464194,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    },
    {
        "driving_direction": 1,
        "heading": -1.3425549740252827,
        "id": "1366_2",
        "pos": {
            "x": 566840.6292212454,
            "y": 4317856.518237346,
            "yaw": -1.3425549740252827,
            "z": 0
        },
        "speeds": {
            "vmax": 20,
            "vmax_dev": 0
        },
        "time_window": None,
        "type": 1
    }
]


def pub_navis(che_id):
    # with open('/home/trunk/PycharmProjects/tpg/tests/2.json', 'r') as f:
    #     data = json.loads(f.read())

    navi = {
        'header': {
            'che_id': che_id,
            'trace_id': str(uuid.uuid4()),
            'trans_id': str(uuid.uuid4()),
            'timestamp': f'{datetime.now().isoformat()}Z'
        },
        'waypoints': data
    }
    print(navi)
    navis = ParseDict(navi, Navi())
    pl = navis.SerializeToString()
    client.publish(f"oy/from/v2/navi/request/{che_id}", pl)


def pub_act_status(che_id, point, yaw):
    status = {
        'header': {
            'che_id': che_id,
            'trace_id': str(uuid.uuid4()),
            'trans_id': str(uuid.uuid4()),
            'timestamp': f'{datetime.now().isoformat()}Z'
        },
        'point': {
            'x': point[0],
            'y': point[1]
        },
        'speed': 0,
        'state_flow': 0,
        'yaw': yaw
    }
    act_status = ParseDict(status, ActStatus())
    pl = act_status.SerializeToString()
    topic = f"oy/from/v2/{'act' if che_id.startswith('A') else 'rtg'}_status/notify/{che_id}"
    print(topic)
    resp = client.publish(topic, pl)
    print(resp)


def pub_counterpoint(che_id, offset):
    counterpoint = {
        "MsgID": "20250225091254506R314",
        "CraneCode": "R312",
        "AreaType": 2,
        "AreaCode": "Y.01D:B.37",
        "GantryGPos": 0,
        "GantryGpsPosX": 373.89,
        "GantryGpsPosY": 180.94,
        "TrolleyPos": 27,
        "HoistPos": 1775,
        "IsRunning": 0,
        "RunDirection": 0,
        "Speed": 0,
        "DestAreaCode": "",
        "OperationStatus": 0,
        "EnterTrucks": [
            {
                "CHECode": "",
                "CHEType": che_id
            }
        ],
        "Spreader": [
            {
                "SpreaderSize": 40,
                "Land": 0,
                "Lock": 0,
                "UnLock": 1,
                "CHECode": che_id
            }
        ],
        "Lane": [
            {
                "LaneCode": "Y.01D:L.37.1",
                "CPSStatus": 0,
                "TrkIK": 1,
                "TrkOffsetPos": offset,
                "TrkTaskType": 1
            },
            {
                "LaneCode": "Y.05D:L.14.2",
                "CPSStatus": 0,
                "TrkIK": 0,
                "TrkOffsetPos": 0,
                "TrkTaskType": 1
            }
        ],
        "TaskType": "",
        "UptTime": "2025-02-25 09:12:54:506"
    }
    topic = "ECS/RMG/R312"
    print(topic)
    data = json.dumps(counterpoint)
    resp = client.publish(topic, data)
    print(resp)

client.connect(host="10.188.73.108", port=1883, keepalive=10)

while True:
    pub_counterpoint('A510', 80)
    # pub_act_status("Y312-1", [566827.4845977076, 4317926.684940939], -1.344)
    # pub_act_status("Y312-2", [566824.0217991376, 4317941.690574083], -1.344)
    # pub_act_status("Y312-3", [566836.3261517714, 4317875.036451254], -1.344)
    # pub_act_status("A512", (566829.103030812, 4317935.245554973,), -1.344)
    # pub_navis('A512')
    time.sleep(1)
