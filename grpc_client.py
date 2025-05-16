#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2020/9/15
from datetime import datetime
import sys
import uuid

import grpc
from google.protobuf.json_format import ParseDict
from trunk_protos.common.remote_control_pb2 import TaskMaunal, RCControl, RCVehicleCmd
from trunk_protos.fms.svr_fms_to_tpa_pb2_grpc import SvrFmsToTpaStub
from trunk_protos.common.task_control_pb2 import TaskControl
from trunk_protos.common.enums_pb2 import Gear, Sender, LidarPosition, PowerMgmtType, ControlType
from trunk_protos.fms.lidar_pb2 import LidarControl
from trunk_protos.fms.powermgmt_pb2 import PowerMgmt
from trunk_protos.fms.maintenance_pb2 import MaintenanceControl

if __name__ == '__main__':
    print('argv: type \n --login bms cancel_rep rep')
    if len(sys.argv) < 2:
        print('len(argv) < 2.')
        sys.exit(0)
    type = sys.argv[1]
    che_id = sys.argv[2]
    print(type, che_id)
    channel = grpc.insecure_channel("0.0.0.0:50002")  # tpa host:port
    stub = SvrFmsToTpaStub(channel=channel)


    def set_header(msg, che_id="A001", version="v0.1"):
        msg.header.trace_id = str(uuid.uuid4())
        msg.header.trans_id = str(uuid.uuid4())
        if che_id:
            msg.header.che_id = che_id
        msg.header.timestamp.FromDatetime(datetime.now())
        msg.header.version = version


    if type == "t":
        msg = TaskControl()
        resp = stub.task_control_svr(msg)
        print(resp)
    if type == "maunal":
        msg = TaskMaunal()
        set_header(msg)
        ParseDict(
            {
                "task_mode": 2,
            },
            msg
        )
        resp = stub.task_manual_svr(msg)
        print(resp)
    elif type == "zhu":
        msg = TaskMaunal()
        ParseDict(
            {
                "x": 1.1,
                "y": 1,
                "yaw": 1.12
            },
            msg
        )
        resp = stub.temp_stay_point_svr(msg)
        print(resp.status)
    elif type == "c":
        msg = RCControl()
        ParseDict(
            {
                "task_mode": 2,
                "control": 1,
            },
            msg
        )
        resp = stub.rc_control_svr(msg)
        print(resp)
    elif type == "cmd":
        msg = RCVehicleCmd()
        set_header(msg)
        ParseDict(
            {
                "front_wheel_angle": 0.2,
                "back_wheel_angle": 0.2,
                "expected_speed": 1,
                "expected_distance": 5,
                "expected_duration": 2,
                "gear": 3,
            },
            msg
        )
        resp = stub.rc_vehicle_cmd_svr(msg)
        print(resp)
    elif type == 'lidar':
        # print(type)
        msg = ParseDict(
            {
                'header': {'che_id': che_id},
                "sender": Sender.FIT,
                "lidars": [
                    {"lidar_name": "lidar1", "position": LidarPosition.LEFT_FRONT, "switch": True},
                    {"lidar_name": "lidar2", "position": LidarPosition.LEFT_REAR, "switch": True}
                          ]
            }, LidarControl()
        )
        resp = stub.set_lidar_control_svr(msg)
        print(resp)
    elif type == 'power':
        msg = ParseDict({
            'header': {'che_id': che_id},
            "sender": Sender.FIT,
            "power_cmd": {"type": PowerMgmtType.UP}
        }, PowerMgmt())
        stub.power_mgmt_svr(msg)
    elif type == 'yk':
        msg = ParseDict({
            'header': {'che_id': che_id},
            "sender": Sender.FIT,
            "switch": False
        }, MaintenanceControl())
        resp = stub.set_maintenance_control_svr(msg)
        print(resp)
    elif type == 'lock':
        msg = ParseDict({
            'header': {'che_id': che_id},
            "sender": 'test',
            "task_id": str(uuid.uuid4()),
            'type': ControlType.LOCK,
        }, TaskControl())
        resp = stub.set_maintenance_control_svr(msg)
        print(resp)
