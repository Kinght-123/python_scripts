"""
    - 用于从redis获取的数据中解析出需要的字段，并处理成对应的数据结构进行存储。
    - all_data ---- all_xml
"""

# 连接到Redis数据库
import json
import redis

import basic
import create_xml_test


# 把task任务处理成字典并返回的函数
def task_to_dict(task: dict, tasks: list, vbay: int) -> dict:
    # task外层的数据
    from_ppos = tasks[0].get('actual_destination')
    from_area = tasks[0].get('target')

    to_ppos = tasks[-1].get('actual_destination')
    to_area = tasks[-1].get('target')

    form_id = basic.from_id.get(str(task.get('dest_type')), None)
    mvkd = basic.business_type.get(str(tasks[0]['act_business_type']), None)
    target = to_area

    # 单箱作业的参数
    eqid_0 = task['containers'][0].get('id')
    lnth_0 = task['containers'][0].get('size')
    qwgt_0 = task['containers'][0].get('weight')
    putjpos_0 = basic.putjpos_dict.get(str(task['containers'][0].get('position')), None)

    # 单箱作业
    if len(task['containers']) == 1:
        # 构建字典
        keys_ls = ['eqid_0', 'lnth_0', 'qwgt_0', 'putjpos_0', 'target_0', 'from_ppos_0',
                   'from_area_0', 'to_ppos_0', 'to_area_0', 'form_id', 'mvkd',
                   'vbay']
        values_ls = [eqid_0, lnth_0, qwgt_0, putjpos_0,
                     target, from_ppos, from_area, to_ppos, to_area, form_id, mvkd, vbay]
        # 创建一个新的字典，使用keys_ls中的名字作为键，对应变量的值作为值
        dic_test = dict(zip(keys_ls, values_ls))
        return dic_test
    # 双箱作业
    else:
        # 第二个箱子的参数
        eqid_1 = task['containers'][1].get('id')
        lnth_1 = task['containers'][1].get('size')
        qwgt_1 = task['containers'][1].get('weight')
        putjpos_1 = basic.putjpos_dict.get(str(task['containers'][1].get('position')), None)
        # 构建字典
        keys_ls = ['eqid_0', 'lnth_0', 'qwgt_0', 'putjpos_0',
                   'eqid_1', 'lnth_1', 'qwgt_1', 'putjpos_1',
                   'target_0', 'from_ppos_0', 'from_area_0', 'to_ppos_0', 'to_area_0', 'form_id', 'mvkd',
                   'vbay']
        values_ls = [eqid_0, lnth_0, qwgt_0, putjpos_0,
                     eqid_1, lnth_1, qwgt_1, putjpos_1,
                     target, from_ppos, from_area, to_ppos, to_area, form_id, mvkd, vbay]
        # 创建一个新的字典，使用keys_ls中的名字作为键，对应变量的值作为值
        dic_test = dict(zip(keys_ls, values_ls))
        return dic_test


# 获取task信息，然后根据里面的数据转换成相对应的字典并返回
def tasks_to_dict(tasks: list, vbay: int) -> list:
    new__ls = []
    # 遍历任务
    for task in tasks:
        # 如果不是处于进锁站、进岸桥、进堆场的状态
        if task.get('target') == "PSTP" or task.get('target') == "QCTP" or task.get('target') == "YCTP":
            continue
        else:
            new__ls.append(task_to_dict(task, tasks, vbay))
    return new__ls


# 获取对应岸桥的相关数据，并存储到对应的字典中
def get_value(keys: list, dict1: dict) -> dict:
    values_dic = {key: [] for key in keys}
    # 岸桥对应的任务循环的字典，里面存储着构建成xml的参数
    # print(values_dic)

    # 遍历岸桥的所有循环作业数
    for key, values in dict1.items():
        # 初始化cur
        cur = 0
        # print(key)

        # 对应的一个作业循环
        for value in values:
            vbay = value.get('vbay')
            tasks = value.get('tasks')
            values_dic[key].append(tasks_to_dict(tasks, vbay))
    return values_dic


# 连接redis数据库
def connect_redis(host: str, port: int, password: str, db: int) -> bytes:
    r = redis.Redis(host=host, port=port, password=password, db=db)
    return r


# 从redis中提取数据，获取每个岸桥的所有循环轮次的信息，并放到相对应的字典中
def get_redis_data(host: str, port: int, password: str, db: int) -> dict:
    # 创建Redis连接
    r = connect_redis(host=host, port=port, password=password, db=db)
    key_name = "plan:navis_works:*"
    keys = [key.decode('utf-8') for key in r.keys(key_name)]
    # 提取岸桥的数据
    names = [keys[i].split(':')[-1] for i in range(len(keys))]
    # 根据names里面的键来创建字典，对应的数值为空列表
    bridge_dic = {name: [] for name in names}

    for key in keys:
        value = r.lrange(key, 0, -1)
        ls = [json.loads(v.decode('utf-8')) for v in value]
        # 把ls里面的元素添加到对应的键（键为(key.split(':')[-1])）对应的列表中，字典为bridge_dic
        bridge_dic[key.split(':')[-1]] = ls
    values_dic = get_value(names, bridge_dic)
    return values_dic


# print(get_redis_data(redis_host, redis_port, redis_password, redis_db))

# 获取对应岸桥的全部数据
all_data = get_redis_data(basic.redis_host, basic.redis_port, basic.redis_password, basic.redis_db)

# print(all_data)
'''
    - 之前的代码已经没问题了，all__data里面的数据就是岸桥里面存储着每个作业循环所需的参数。
'''


# 获取redis缓存里面的岸桥数据
def get_bridges(host, port, password, db) -> list:
    # 创建Redis连接
    r = connect_redis(host=host, port=port, password=password, db=db)
    key_name = "plan:navis_works:*"
    keys = [key.decode('utf-8') for key in r.keys(key_name)]
    # 提取岸桥的数据
    names = [keys[i].split(':')[-1] for i in range(len(keys))]
    return names


# 初始化岸桥
bridges = get_bridges(basic.redis_host, basic.redis_port, basic.redis_password, basic.redis_db)

# 初始化存储xml数据的数据结构
all_xml = all_data.copy()


# 用提取出来的数据构建xml，并存储到相对应的数据结构中
def to_xml_ls(bridges: list, all_data: dict) -> dict:
    # 遍历岸桥
    for name in bridges:
        # 遍历岸桥所对应的所有循环总数
        for i in range(len(all_data[name])):
            # 将参数处理成xml数据
            to_xml = data_to_xml(all_data[name][i])
            # 填入对应的数据结构中
            all_xml[name][i] = to_xml
    return all_xml


# 把一组作业循环换成xml并替换存储
def data_to_xml(data_list: list) -> list:
    new_ls = []
    for data in data_list:
        new_ls.append(task_to_xml(data))
    return new_ls


# 单箱作业的构建xml的函数
def create_base_xml_str(data: dict) -> str:
    base_xml = create_xml_test.create_task(
        'che_id',  # che_id
        data.get('eqid_0'),
        data.get('lnth_0'),
        data.get('qwgt_0'),
        data.get('putjpos_0'),
        data.get('target_0'),
        data.get('from_ppos_0'),
        data.get('from_area_0'),
        'YardRow',  # from_area_type
        data.get('to_ppos_0'),
        data.get('to_area_0'),
        'Vessel',  # to_area_type
        data.get('form_id'),
        data.get('mvkd'),
        data.get('vbay'),
    )
    return base_xml


# 把一组作业循环中的一个作业循环替换成xml字符串
def task_to_xml(data: dict) -> str:
    xml_str = ""
    # 证明双箱作业
    if "eqid_1" in data.keys():
        xml_str = create_xml_test.create_two_tasks(
            'che_id',  # che_id
            data.get('eqid_0'),
            data.get('eqid_1'),
            data.get('lnth_0'),
            data.get('lnth_1'),
            data.get('qwgt_0'),
            data.get('qwgt_1'),
            data.get('putjpos_0'),
            data.get('putjpos_1'),
            data.get('from_ppos_0'),
            data.get('from_area_0'),
            'YardRow',  # from_area_type
            data.get('to_ppos_0'),
            data.get('to_area_0'),
            'Vessel',  # to_area_type
            data.get('form_id'),
            data.get('mvkd'),
            data.get('target_0'),
            data.get('vbay'),
        )
    # 否则是单箱作业
    else:
        xml_str = create_base_xml_str(data)
    return xml_str


# 获取每个岸桥对应的任务数量
def get_bridge_task(key: str) -> str:
    return f'{key}岸桥 ---- {len(all_xml[key])}个任务'

# for key in bridges:
#     print(get_bridge_task(key))

# # 最终的xml数据
# to_xml_ls(bridges)
# print(all_xml)
