import json
from typing import List, Optional


# 定义Container类
class Container:
    def __init__(self, id: str, size: int, weight: int, position: int):
        self.id = id
        self.size = size
        self.weight = weight
        self.position = position

    def to_dict(self):
        return {
            "id": self.id,
            "size": self.size,
            "weight": self.weight,
            "position": self.position
        }


# 定义Task类
class Task:
    def __init__(self, trace_id: str, has_navi: bool, status: int, containers: List[Container], guide_cps: bool,
                 target: str, sub_target: Optional[str], task_type: int, task_id: str, task_mode: int,
                 actual_destination: Optional[str], act_business_type: int, act_order_type: int, dest_type: int,
                 route_direction: int, up_vpb: str, down_vpb: str, crane_id: str):
        self.trace_id = trace_id
        self.has_navi = has_navi
        self.status = status
        self.containers = containers
        self.guide_cps = guide_cps
        self.target = target
        self.sub_target = sub_target
        self.task_type = task_type
        self.task_id = task_id
        self.task_mode = task_mode
        self.actual_destination = actual_destination
        self.act_business_type = act_business_type
        self.act_order_type = act_order_type
        self.dest_type = dest_type
        self.route_direction = route_direction
        self.up_vpb = up_vpb
        self.down_vpb = down_vpb
        self.crane_id = crane_id

    def to_dict(self):
        return {
            "trace_id": self.trace_id,
            "has_navi": self.has_navi,
            "status": self.status,
            "containers": [container.to_dict() for container in self.containers],
            "guide_cps": self.guide_cps,
            "target": self.target,
            "sub_target": self.sub_target,
            "task_type": self.task_type,
            "task_id": self.task_id,
            "task_mode": self.task_mode,
            "actual_destination": self.actual_destination,
            "act_business_type": self.act_business_type,
            "act_order_type": self.act_order_type,
            "dest_type": self.dest_type,
            "route_direction": self.route_direction,
            "up_vpb": self.up_vpb,
            "down_vpb": self.down_vpb,
            "crane_id": self.crane_id
        }


# 定义VbayData类
class VbayData:
    def __init__(self, vbay: int, tasks: List[Task], seq: int):
        self.vbay = vbay
        self.tasks = tasks
        self.seq = seq

    def to_dict(self):
        return {
            "vbay": self.vbay,
            "tasks": [task.to_dict() for task in self.tasks],
            "seq": self.seq
        }


# 填充数据的函数
def fill_data(data: dict) -> VbayData:
    tasks = []
    for task_data in data["tasks"]:
        containers = [Container(**container) for container in task_data["containers"]]
        task = Task(
            trace_id=task_data["trace_id"],
            has_navi=task_data["has_navi"],
            status=task_data["status"],
            containers=containers,
            guide_cps=task_data["guide_cps"],
            target=task_data["target"],
            sub_target=task_data["sub_target"],
            task_type=task_data["task_type"],
            task_id=task_data["task_id"],
            task_mode=task_data["task_mode"],
            actual_destination=task_data["actual_destination"],
            act_business_type=task_data["act_business_type"],
            act_order_type=task_data["act_order_type"],
            dest_type=task_data["dest_type"],
            route_direction=task_data["route_direction"],
            up_vpb=task_data["up_vpb"],
            down_vpb=task_data["down_vpb"],
            crane_id=task_data["crane_id"]
        )
        tasks.append(task)

    vbay_data = VbayData(
        vbay=data["vbay"],
        tasks=tasks,
        seq=data["seq"]
    )
    return vbay_data


# JSON数据
data_json = '''
{
    "vbay": 25,
    "tasks": [
        {
            "trace_id": "b814a465-1380-4dc3-bb9e-ab246432226d",
            "has_navi": false,
            "status": 1,
            "containers": [
                {"id": "FTAU1873283", "size": 20, "weight": 24188, "position": 1},
                {"id": "APZU3916594", "size": 20, "weight": 30220, "position": 3}
            ],
            "guide_cps": true,
            "target": "O6D",
            "sub_target": "35",
            "task_type": 3,
            "task_id": "tosc-sim-b78a624d-ea3a-4b49-83a0-a98bc92b5428",
            "task_mode": 1,
            "actual_destination": "O6D.35",
            "act_business_type": 1,
            "act_order_type": 3,
            "dest_type": 1,
            "route_direction": 1,
            "up_vpb": "",
            "down_vpb": "",
            "crane_id": "O6D"
        },
        {
            "trace_id": "3d4c8d9c-228d-47a4-9e66-4af00695ff4f",
            "has_navi": false,
            "status": 1,
            "containers": [
                {"id": "APZU3916594", "size": 20, "weight": 30220, "position": 3},
                {"id": "FTAU1873283", "size": 20, "weight": 24188, "position": 1}
            ],
            "guide_cps": true,
            "target": "O6D",
            "sub_target": "35",
            "task_type": 3,
            "task_id": "tosc-sim-7c740469-e47a-40fc-b813-b1acda240a16",
            "task_mode": 1,
            "actual_destination": "O6D.35",
            "act_business_type": 1,
            "act_order_type": 3,
            "dest_type": 1,
            "route_direction": 1,
            "up_vpb": "",
            "down_vpb": "",
            "crane_id": "O6D"
        },
        {
            "trace_id": "f4fe47ed-6468-4c7e-ac11-e75f3c5bb54f",
            "has_navi": false,
            "status": 1,
            "containers": [
                {"id": "FTAU1873283", "size": 20, "weight": 24188, "position": 1},
                {"id": "APZU3916594", "size": 20, "weight": 30220, "position": 3}
            ],
            "guide_cps": true,
            "target": "PSTP",
            "sub_target": "None",
            "task_type": 10,
            "task_id": "tosc-sim-346e9e19-916b-4fe3-9177-e69448ee7b62",
            "task_mode": 1,
            "actual_destination": null,
            "act_business_type": 1,
            "act_order_type": 2,
            "dest_type": 2,
            "route_direction": 1,
            "up_vpb": "",
            "down_vpb": "",
            "crane_id": "PSTP"
        },
        {
            "trace_id": "c5010c5d-8d81-47ae-b671-836f8e1297aa",
            "has_navi": false,
            "status": 1,
            "containers": [
                {"id": "FTAU1873283", "size": 20, "weight": 24188, "position": 1},
                {"id": "APZU3916594", "size": 20, "weight": 30220, "position": 3}
            ],
            "guide_cps": true,
            "target": "Q108",
            "sub_target": "3",
            "task_type": 2,
            "task_id": "tosc-sim-92e85a30-47ec-4d31-938d-fa99933d9384",
            "task_mode": 1,
            "actual_destination": "Q108.3",
            "act_business_type": 1,
            "act_order_type": 2,
            "dest_type": 6,
            "route_direction": 1,
            "up_vpb": "",
            "down_vpb": "",
            "crane_id": "Q108"
        }
    ],
    "seq": 386
}
'''

# 解析JSON数据
data = json.loads(data_json)

# 填充数据
vbay_data = fill_data(data)

# 将对象转换为JSON字符串并打印
vbay_data_json = json.dumps(vbay_data.to_dict(), indent=4)
print(vbay_data_json)
