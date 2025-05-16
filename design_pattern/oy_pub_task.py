from datetime import datetime

import pika
from google.protobuf.json_format import ParseDict
from trunk_protos.common.enums_pb2 import OrderStatus, TaskType, WorkCycleDirection, OrderType
from trunk_protos.common.task_pb2 import Task
import uuid

# oy
HOST, PORT, VHOST = '10.188.73.108', 5672, '/prod'

credentials = pika.PlainCredentials('trunk', 'Trunk@123')

# TRUCK_ID, TARGET, SUB_TARGET, TASK_TYPE = 'A505', 'PSTP', '201', TaskType.EMPTY_TO_INTERACTION
TRUCK_ID, TARGET, SUB_TARGET, TASK_TYPE = 'A505', 'O4D', '50', TaskType.FULL_TO_YC
# TRUCK_ID, TARGET, SUB_TARGET, TASK_TYPE = 'A505', 'Q111', '5', TaskType.FULL_TO_QC
# TRUCK_ID, TARGET, SUB_TARGET, TASK_TYPE = 'A506', 'Q111', '5', TaskType.FULL_TO_QC
# TRUCK_ID, TARGET, SUB_TARGET, TASK_TYPE = 'A508', 'Q110', '6', TaskType.FULL_TO_QC
# TRUCK_ID, TARGET, SUB_TARGET, TASK_TYPE = 'A504', 'Q111', '4', TaskType.FULL_TO_QC
# TRUCK_ID, TARGET, SUB_TARGET, TASK_TYPE = 'A506', 'O2D', '8', TaskType.EMPTY_TO_YC

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=HOST, port=PORT, virtual_host=VHOST, credentials=credentials
))
task = ParseDict(
    {
        'header': {
            'che_id': TRUCK_ID,
            'timestamp': f'{datetime.now().isoformat()}Z'
        },
        'has_navi': False,
        'status': OrderStatus.ENTERED,
        'containers': [
            {
                'id': 'FAKE', 'size': 40, 'weight': 0, 'position': 2
            }
        ],
        'guide_cps': True,
        'target': TARGET, 'sub_target': SUB_TARGET,
        'task_type': TASK_TYPE,
        'task_id': 'test-' + str(uuid.uuid4()),
        'crane_id': TARGET,
        'act_order_type': OrderType.DELIVER,
        'route_direction': WorkCycleDirection.CLOCKWISE,
        'up_vpb': '',
        'down_vpb': ''
    },
    Task()
)
print(task)
channel = connection.channel()
result = channel.basic_publish(
    body=task.SerializeToString(),
    exchange='fmp.v2.e.topic.cmd',
    routing_key='fmp.v2.k.cmd.tos_task.{}'.format(TRUCK_ID),
)
connection.close()
print(result)
