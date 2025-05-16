import pika
from google.protobuf.json_format import ParseDict
from trunk_protos.common.enums_pb2 import ControlType
from trunk_protos.common.task_control_pb2 import TaskControl

HOST, PORT, VHOST = '10.188.73.105', 5672, '/prod'
# TRUCK_ID, TYPE = 'A505', ControlType.FINISH
TRUCK_ID, TYPE = 'A504', ControlType.CANCEL

credentials = pika.PlainCredentials('trunk', 'Trunk@123')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=HOST, port=PORT, virtual_host=VHOST, credentials=credentials
))
task_control = ParseDict(
    {
        'header': {
            'che_id': TRUCK_ID
        },
        'sender': 'test',
        'type': TYPE,
        'task_id': ''
    },
    TaskControl()
)
channel = connection.channel()
result = channel.basic_publish(
    body=task_control.SerializeToString(),
    exchange='fmp.v2.e.topic.cmd',
    routing_key='fmp.v2.k.cmd.tos_task_control.{}'.format(TRUCK_ID)
)
connection.close()
print(result)
