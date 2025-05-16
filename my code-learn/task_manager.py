# task_manager.py
from datetime import datetime
import task_pb2  # 导入生成的模块
from google.protobuf import timestamp_pb2  # 导入 Google 的 timestamp 模块


def create_task():
    # 创建一个新的 Task 消息
    task = task_pb2.Task()
    task.header.user_id = "user123"

    # 创建一个 Timestamp 消息
    updated = timestamp_pb2.Timestamp()
    updated.FromDatetime(datetime.datetime.utcnow())
    task.updated.CopyFrom(updated)

    task.trace_id = "trace456"
    task.order_version = 1
    task.task_id = "task789"
    task.task_version = 2
    task.status = task_pb2.OrderStatus.IN_PROGRESS

    # 创建一些 Container 消息并添加到 repeated 字段
    container1 = task.containers.add()
    container1.id = "container1"
    container1.length = 10.5
    container1.width = 5.0
    container1.height = 8.0

    container2 = task.containers.add()
    container2.id = "container2"
    container2.length = 12.0
    container2.width = 6.0
    container2.height = 9.0

    # 序列化消息为字符串
    serialized_task = task.SerializeToString()
    print(f"Serialized task: {serialized_task}")

    # 反序列化字符串回消息
    new_task = task_pb2.Task()
    new_task.ParseFromString(serialized_task)
    print(f"Task ID: {new_task.task_id}")
    print(f"Task Status: {task_pb2.OrderStatus.Name(new_task.status)}")


def main():
    create_task()


if __name__ == "__main__":
    main()