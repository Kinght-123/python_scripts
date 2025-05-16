import socket
import threading
import redis
import json

import basic
import create_xml


# 连接数据库
def connect_redis(host: str, port: int, password: str, db: int) -> bytes:
    r = redis.Redis(host=host, port=port, password=password, db=db)
    return r


# 通过平板车获取对应岸桥的函数
def get_bridge(truck_id) -> (None, str):
    for key, values in basic.WORK_LINE.items():
        if truck_id in values:
            return key
    return None


'''
    - 1. 首先，写一个函数，传入任务和车号，构造出xml文件
'''


def task_to_xml(task: dict, che_id: str = 'che_id') -> str:
    # 公共的参数
    che_id = che_id
    vaby = task.get('vbay', None)
    target = task.get('target', None)
    mvkd = basic.business_type.get(task.get('act_business_type', None), None)

    # position的参数

    # 如果双箱作业

    # 如果单箱作业
    container = task.get('containers', None)
    eqid = container.get('id', None)
    lnth = container.get('size', None)
    qwgt = container.get('weight', None)
    putjpos = basic.putjpos_dict.get(container.get('position', None), None)

    return 'test'


# 获取所有待发送任务的che_id
def get_move_che_ids() -> list:
    # 连接数据库
    r = connect_redis(basic.redis_host, basic.redis_port, basic.redis_password, basic.redis_db)
    # 找到数据库
    # # 通过平板车获取对应岸桥的函数
    # def get_bridge(truck_id) -> (None, str):
    #     for key, values in basic.WORK_LINE.items():
    #         if truck_id in values:
    #             return key
    #     return None中车辆待发送的任务的键
    keys = r.keys('sim:move_tasks:*')

    # 获取move_tasks中的所有车号
    che_ids = [key.decode('utf-8').split(':')[-1] for key in keys]
    # 关闭数据库连接
    r.connection_pool.disconnect()

    return che_ids


# 测试的函数
def test():
    r = connect_redis(basic.redis_host, basic.redis_port, basic.redis_password, basic.redis_db)
    keys = r.keys('sim:navis_works:*')
    a = [key.decode('utf-8').split(':')[-2] + ':' + key.decode('utf-8').split(':')[-1] for key in keys]

    t = set()
    for b in a:
        new_key = f'sim:navis_works:{b}'
        value = r.lrange(new_key, 0, -1)
        print(f'{b[-4:]}岸桥')
        for i in value:
            j = json.loads(i.decode('utf-8'))
            t.add(len(j))
    print(t)

test()
