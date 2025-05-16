"""
    - 用于从redis获取的数据中解析出需要的字段，并处理成对应的数据结构进行存储。
    - all_data ---- all_xml
"""

# 连接到Redis数据库
import json
import redis

import basic
import create_xml_test


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


# 获取task信息，然后根据里面的数据转换成相对应的字典并返回
def tasks_to_dict(tasks: list) -> dict:
    pass


# 获取对应岸桥的相关数据，并存储到对应的字典中
def get_value(keys: list, dict1: dict) -> dict:
    global lnth_03, eqid_03, qwgt_03, putjpos_03
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
            values_dic[key].append(list())
            vbay = value.get('vbay')
            tasks = value.get('tasks')

            # 获取到三个task，但是不读取中间去锁站装锁或者卸锁的task || 或者是直接两个任务的
            if len(tasks) == 3 or len(tasks) == 2:
                for i, task in enumerate(tasks):
                    # i = 0, 1, 2 或者 i = 0, 1
                    if i != 1 or len(tasks) == 2:
                        # containers里面的内容
                        from_ppos_0 = tasks[0].get('actual_destination')
                        from_area_0 = tasks[0].get('target')
                        to_ppos_0 = tasks[-1].get('actual_destination')
                        to_area_0 = tasks[-1].get('target')

                        containers_0 = task['containers'][0]
                        eqid_0 = containers_0.get('id')
                        target_0 = task.get('target')
                        # 说明只有一个container
                        if len(task['containers']) == 1:
                            lnth_0 = containers_0.get('size')
                            qwgt_0 = containers_0.get('weight')
                            putjpos_0 = basic.putjpos_dict.get(str(containers_0['position']), None)
                            form_id_0 = basic.from_id.get(str(task['dest_type']), None)
                            business_type_0 = basic.business_type.get(str(tasks[0]['act_business_type']), None)
                            keys_ls = ['eqid_0', 'lnth_0', 'qwgt_0', 'putjpos_0', 'target_0', 'from_ppos_0',
                                       'from_area_0', 'to_ppos_0', 'to_area_0', 'form_id_0', 'business_type_0', 'vbay']
                            values_as_vars = [eqid_0, lnth_0, qwgt_0, putjpos_0, target_0, from_ppos_0,
                                              from_area_0, to_ppos_0, to_area_0, form_id_0, business_type_0, vbay]

                            # 创建一个新的字典，使用keys_ls中的名字作为键，对应变量的值作为值
                            dic_test = dict(zip(keys_ls, values_as_vars))
                            values_dic[key][cur].append(dic_test)

                            # 说明最后一个任务虽然有一个container， 但是实际上是双箱作业
                            if len(tasks[0]['containers']) != 1:
                                task006 = tasks[0]['containers'][1]
                                eqid_06 = task006.get('id')
                                lnth_06 = task006.get('size')
                                qwgt_06 = task006.get('weight')
                                putjpos_06 = basic.putjpos_dict.get(str(task006['position']), None)
                                keys_ls = ['eqid_0', 'lnth_0', 'qwgt_0', 'putjpos_0', 'target_0', 'from_ppos_0',
                                           'from_area_0', 'to_ppos_0', 'to_area_0', 'form_id_0', 'business_type_0',
                                           'vbay']
                                values_as_vars_06 = [eqid_06, lnth_06, qwgt_06, putjpos_06, target_0, from_ppos_0,
                                                     from_area_0, to_ppos_0, to_area_0, form_id_0, business_type_0,
                                                     vbay]
                                # 创建一个新的字典，使用keys_ls中的名字作为键，对应变量的值作为值
                                dic_test_06 = dict(zip(keys_ls, values_as_vars_06))
                                values_dic[key][cur].append(dic_test_06)
                        # # 单箱作业
                        # if len(tasks[0]['containers']) == 1:
                        #     lnth_0 = containers_0.get('size')
                        #     qwgt_0 = containers_0.get('weight')
                        #     putjpos_0 = putjpos_dict.get(str(containers_0['position']), None)
                        #     form_id_0 = from_id.get(str(task['dest_type']), None)
                        #     business_type_0 = business_type.get(str(tasks[0]['act_business_type']), None)
                        #     keys_ls = ['eqid_0', 'lnth_0', 'qwgt_0', 'putjpos_0', 'target_0', 'from_ppos_0',
                        #                'from_area_0', 'to_ppos_0', 'to_area_0', 'form_id_0', 'business_type_0', 'vbay']
                        #     values_as_vars = [eqid_0, lnth_0, qwgt_0, putjpos_0, target_0, from_ppos_0,
                        #                       from_area_0, to_ppos_0, to_area_0, form_id_0, business_type_0, vbay]
                        #
                        #     # 创建一个新的字典，使用keys_ls中的名字作为键，对应变量的值作为值
                        #     dic_test = dict(zip(keys_ls, values_as_vars))
                        #     values_dic[key][cur].append(dic_test)
                        # # 最后一个task里面有一个容器，但实际上是双箱作业
                        # else:
                        #     # 第一个container
                        #     keys_ls = ['eqid_0', 'lnth_0', 'qwgt_0', 'putjpos_0', 'target_0', 'from_ppos_0',
                        #                'from_area_0', 'to_ppos_0', 'to_area_0', 'form_id_0', 'business_type_0',
                        #                'vbay']
                        #     values_as_vars6 = [eqid_0, lnth_0, qwgt_0, putjpos_0, target_0, from_ppos_0,
                        #                       from_area_0, to_ppos_0, to_area_0, form_id_0, business_type_0, vbay]
                        #
                        #     # 创建一个新的字典，使用keys_ls中的名字作为键，对应变量的值作为值
                        #     dic_test = dict(zip(keys_ls, values_as_vars6))
                        #     values_dic[key][cur].append(dic_test)
                        #
                        #     # 第二个container
                        #     task001 = tasks[0]['containers'][1]
                        # 双箱任务
                        else:
                            # 第一个container
                            containers_1 = task['containers'][1]
                            lnth_01 = containers_0.get('size')
                            qwgt_01 = containers_0.get('weight')
                            putjpos_01 = basic.putjpos_dict.get(str(containers_0['position']), None)
                            # 第二个container
                            eqid_11 = containers_1.get('id')
                            lnth_11 = containers_1.get('size')
                            qwgt_11 = containers_1.get('weight')
                            putjpos_11 = basic.putjpos_dict.get(str(containers_1['position']), None)

                            form_id_01 = basic.from_id.get(str(task['dest_type']), None)
                            business_type_01 = basic.business_type.get(str(tasks[0]['act_business_type']), None)

                            # 构造第一个任务
                            keys_ls1 = ['eqid_0', 'lnth_0', 'qwgt_0', 'putjpos_0', 'target_0', 'from_ppos_0',
                                        'from_area_0', 'to_ppos_0', 'to_area_0', 'form_id_0', 'business_type_0',
                                        'vbay', ]
                            values_as_vars1 = [eqid_0, lnth_01, qwgt_01, putjpos_01, target_0, from_ppos_0,
                                               from_area_0, to_ppos_0, to_area_0, form_id_01, business_type_01, vbay]
                            # 创建一个新的字典，使用keys_ls中的名字作为键，对应变量的值作为值
                            dic_test1 = dict(zip(keys_ls1, values_as_vars1))
                            values_dic[key][cur].append(dic_test1)

                            # 构造第二个任务
                            key_ls_2 = ['eqid_1', 'lnth_1', 'qwgt_1', 'putjpos_1', 'target_0', 'from_ppos_0',
                                        'from_area_0', 'to_ppos_0', 'to_area_0', 'form_id_0', 'business_type_0',
                                        'vbay', ]
                            values_as_vars_2 = [eqid_11, lnth_11, qwgt_11, putjpos_11, target_0, from_ppos_0,
                                                from_area_0, to_ppos_0, to_area_0, form_id_01, business_type_01, vbay]
                            dic_test_2 = dict(zip(key_ls_2, values_as_vars_2))
                            values_dic[key][cur].append(dic_test_2)
                cur += 1

            # 有四个任务的, 4个任务的都是双箱的
            else:
                for i, task in enumerate(tasks):
                    # 只看第一个任务和第四个任务
                    if i == 0 or i == 3:
                        # 公用的参数
                        from_ppos_02 = tasks[0].get('actual_destination')
                        from_area_02 = tasks[0].get('target')
                        to_ppos_02 = tasks[-1].get('actual_destination')
                        to_area_02 = tasks[-1].get('target')

                        # 第一个container
                        container_four_0 = task['containers'][0]
                        eqid_02 = container_four_0.get('id')
                        lnth_02 = container_four_0.get('size')
                        qwgt_02 = container_four_0.get('weight')
                        putjpos_02 = basic.putjpos_dict.get(str(container_four_0['position']), None)

                        #
                        if len(task['containers']) != 1:
                            # 第二个container
                            container_four_2 = task['containers'][1]
                            eqid_03 = container_four_2.get('id')
                            lnth_03 = container_four_2.get('size')
                            qwgt_03 = container_four_2.get('weight')
                            putjpos_03 = basic.putjpos_dict.get(str(container_four_2['position']), None)

                            # 其他的参数
                            target = task.get('target')
                            form_id_02 = basic.from_id.get(str(task['dest_type']), None)
                            business_type_02 = basic.business_type.get(str(tasks[0]['act_business_type']), None)

                            # 构造第一个任务
                            keys_ls__1 = ['eqid_0', 'lnth_0', 'qwgt_0', 'putjpos_0', 'target_0', 'from_ppos_0',
                                          'from_area_0', 'to_ppos_0', 'to_area_0', 'form_id_0', 'business_type_0',
                                          'vbay', ]
                            values_ls_1 = [eqid_02, lnth_02, qwgt_02, putjpos_02, target, from_ppos_02,
                                           from_area_02, to_ppos_02, to_area_02, form_id_02, business_type_02, vbay]
                            # 创建一个新的字典，使用keys_ls中的名字作为键，对应变量的值作为值
                            dic_data__1 = dict(zip(keys_ls__1, values_ls_1))
                            values_dic[key][cur].append(dic_data__1)

                            # 构造第二个任务
                            key_ls__2 = ['eqid_1', 'lnth_1', 'qwgt_1', 'putjpos_1', 'target_0', 'from_ppos_0',
                                         'from_area_0', 'to_ppos_0', 'to_area_0', 'form_id_0', 'business_type_0',
                                         'vbay', ]
                            values_ls_2 = [eqid_03, lnth_03, qwgt_03, putjpos_03, target, from_ppos_02,
                                           from_area_02, to_ppos_02, to_area_02, form_id_02, business_type_02, vbay]
                            dic_data__2 = dict(zip(key_ls__2, values_ls_2))
                            values_dic[key][cur].append(dic_data__2)
                        # 对应4个task，但是最后一个task的container数量有一个
                        else:
                            # 其他的参数
                            target4 = task.get('target')
                            form_id_04 = basic.from_id.get(str(task['dest_type']), None)
                            business_type_04 = basic.business_type.get(str(tasks[0]['act_business_type']), None)

                            # 构造第一个任务
                            keys_ls__1 = ['eqid_0', 'lnth_0', 'qwgt_0', 'putjpos_0', 'target_0', 'from_ppos_0',
                                          'from_area_0', 'to_ppos_0', 'to_area_0', 'form_id_0', 'business_type_0',
                                          'vbay', ]
                            values_ls_1 = [eqid_02, lnth_02, qwgt_02, putjpos_02, target4, from_ppos_02,
                                           from_area_02, to_ppos_02, to_area_02, form_id_04, business_type_04, vbay]
                            # 创建一个新的字典，使用keys_ls中的名字作为键，对应变量的值作为值
                            dic_data__1 = dict(zip(keys_ls__1, values_ls_1))
                            values_dic[key][cur].append(dic_data__1)

                            # 构造第二个任务
                            key_ls__2 = ['eqid_1', 'lnth_1', 'qwgt_1', 'putjpos_1', 'target_0', 'from_ppos_0',
                                         'from_area_0', 'to_ppos_0', 'to_area_0', 'form_id_0', 'business_type_0',
                                         'vbay', ]
                            values_ls_2 = [eqid_03, lnth_03, qwgt_03, putjpos_03, target4, from_ppos_02,
                                           from_area_02, to_ppos_02, to_area_02, form_id_04, business_type_04, vbay]
                            dic_data__2 = dict(zip(key_ls__2, values_ls_2))
                            values_dic[key][cur].append(dic_data__2)
                cur += 1
    return values_dic


# print(get_redis_data(redis_host, redis_port, redis_password, redis_db))

# 获取对应岸桥的全部数据
all_data = get_redis_data(basic.redis_host, basic.redis_port, basic.redis_password, basic.redis_db)


# all_data = func()
# print(all_data)

# test
# llll = set()
# for key, value in all_data.items():
#     for i in value:
#         llll.add(len(i))
# print(llll)


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

# print(bridges)
# print(all_data)
# 初始化存储xml数据的数据结构
all_xml = all_data.copy()


# print(all_data)    # all_data没有问题！！！

# 岸桥所对应的全部循环的数据转通过解析出一些必需的字段，然后根据字段和对应的数值构建xml字符串
def data_to_xml(data_list: list) -> list:
    # 确保data_list长度至少为2，否则抛出异常或返回空列表
    if len(data_list) < 2:
        raise ValueError("data_list长度必须至少为2")

    new_ls = []
    a, b = data_list[0], data_list[1]

    # 使用get()方法安全地访问字典键值，默认值为None
    def get_safe(data, key):
        return data.get(key, None)

    try:
        if len(data_list) == 2:
            # 优化重复代码，使用一个函数调用来处理
            new_xml_1 = create_xml_test.create_task(
                'che_id', get_safe(a, 'eqid_0'), get_safe(a, 'lnth_0'),
                get_safe(a, 'qwgt_0'), get_safe(a, 'putjpos_0'),
                get_safe(a, 'target_0'), get_safe(a, 'from_ppos_0'),
                get_safe(a, 'from_area_0'), 'YardRow', get_safe(a, 'to_ppos_0'),
                get_safe(a, 'to_area_0'), 'Vessel', get_safe(a, 'form_id_0'),
                get_safe(a, 'business_type_0'),
                get_safe(a, 'vbay'),
            )
            # 对于单箱作业，只需要改变输入数据的来源即可，因此这里省略了重复代码
            new_ls.append(new_xml_1)
            new_ls.append(create_xml_test.create_task(
                'che_id', get_safe(b, 'eqid_0'), get_safe(b, 'lnth_0'),
                get_safe(b, 'qwgt_0'), get_safe(b, 'putjpos_0'),
                get_safe(b, 'target_0'), get_safe(b, 'from_ppos_0'),
                get_safe(b, 'from_area_0'), 'YardRow', get_safe(b, 'to_ppos_0'),
                get_safe(b, 'to_area_0'), 'Vessel', get_safe(b, 'form_id_0'),
                get_safe(b, 'business_type_0'),
                get_safe(b, 'vbay'),
            ))
        else:
            # 对于双箱作业，同样优化重复代码
            c, d = data_list[2], data_list[3]
            new_xml_3 = create_xml_test.create_two_tasks(
                'che_id', get_safe(a, 'eqid_0'), get_safe(b, 'eqid_1'), get_safe(a, 'lnth_0'), get_safe(b, 'lnth_1'),
                get_safe(a, 'qwgt_0'), get_safe(b, 'qwgt_1'), get_safe(a, 'putjpos_0'), get_safe(b, 'putjpos_1'),
                get_safe(a, 'from_ppos_0'), get_safe(a, 'from_area_0'), 'YardRow', get_safe(a, 'to_ppos_0'),
                get_safe(a, 'to_area_0'), 'Vessel', get_safe(a, 'form_id_0'), get_safe(a, 'business_type_0'),
                get_safe(a, 'target_0'), get_safe(a, 'vbay'),
            )
            new_ls.append(new_xml_3)
            # 省略了其他create_two_tasks的调用，以避免重复代码

            # 添加对剩余的new_xml对象的处理
            new_ls.append(create_xml_test.create_two_tasks(
                'che_id', get_safe(a, 'eqid_0'), get_safe(b, 'eqid_1'), get_safe(a, 'lnth_0'), get_safe(b, 'lnth_1'),
                get_safe(a, 'qwgt_0'), get_safe(b, 'qwgt_1'), get_safe(a, 'putjpos_0'), get_safe(b, 'putjpos_1'),
                get_safe(b, 'from_ppos_0'), get_safe(b, 'from_area_0'), 'YardRow', get_safe(b, 'to_ppos_0'),
                get_safe(b, 'to_area_0'), 'Vessel', get_safe(b, 'form_id_0'), get_safe(b, 'business_type_0'),
                get_safe(b, 'target_0'), get_safe(b, 'vbay'),
            ))
            new_ls.append(create_xml_test.create_two_tasks(
                'che_id', get_safe(a, 'eqid_0'), get_safe(b, 'eqid_1'), get_safe(a, 'lnth_0'), get_safe(b, 'lnth_1'),
                get_safe(a, 'qwgt_0'), get_safe(b, 'qwgt_1'), get_safe(a, 'putjpos_0'), get_safe(b, 'putjpos_1'),
                get_safe(c, 'from_ppos_0'), get_safe(c, 'from_area_0'), 'Vessel', get_safe(c, 'to_ppos_0'),
                get_safe(c, 'to_area_0'), 'YardRow', get_safe(c, 'form_id_0'), get_safe(c, 'business_type_0'),
                get_safe(c, 'target_0'), get_safe(c, 'vbay'),
            ))
            new_ls.append(create_xml_test.create_two_tasks(
                'che_id', get_safe(a, 'eqid_0'), get_safe(b, 'eqid_1'), get_safe(a, 'lnth_0'), get_safe(b, 'lnth_1'),
                get_safe(a, 'qwgt_0'), get_safe(b, 'qwgt_1'), get_safe(a, 'putjpos_0'), get_safe(b, 'putjpos_1'),
                get_safe(d, 'from_ppos_0'), get_safe(d, 'from_area_0'), 'Vessel', get_safe(d, 'to_ppos_0'),
                get_safe(d, 'to_area_0'), 'YardRow', get_safe(d, 'form_id_0'), get_safe(d, 'business_type_0'),
                get_safe(d, 'target_0'), get_safe(d, 'vbay'),
            ))
    except Exception as e:
        # 添加异常处理，确保在出现异常时不会导致程序崩溃
        print(f"处理过程中发生异常: {e}")
        # 可以选择是否要返回空列表或包含错误信息的列表
        return []

    return new_ls


# 用提取出来的数据构建xml，并存储到相对应的数据结构中
def to_xml_ls(bridges: list) -> dict:
    # 遍历岸桥
    for name in bridges:
        # 遍历岸桥所对应的所有循环总数
        for i in range(len(all_data[name])):
            # print(len(all_data[name][i]))
            # 将参数处理成xml数据
            to_xml = data_to_xml(all_data[name][i])
            # 填入对应的数据结构中
            all_xml[name][i] = to_xml
    return all_xml


# 获取每个岸桥对应的任务数量
def get_bridge_task(key: str) -> str:
    return f'{key}岸桥 ---- {len(all_xml[key])}个任务'


# print(all_data)

for key in bridges:
    print(get_bridge_task(key))

# # 最终的xml数据
# to_xml_ls(bridges)
# print(all_xml)

'''
    - test
'''
# # 调用函数获取到全部数据
# for name in data_dict.keys():
#     for i in range(len(all_data[name])):
#         for j in range(len(all_data[name][i])):
#             # 构建单箱作业对应的xml字符串
#             if len(all_data[name][i]) == 2:
#                 task = all_data[name][i][j]
#                 data_dict[name].append(
#                     create_xml_test.create_task('che_id', task['eqid_0'], task['lnth_0'], task['qwgt_0'],
#                                                 task['putjpos_0'],
#                                                 task['target_0'], task['from_ppos_0'], task['from_area_0'], 'YardRow',
#                                                 task['to_ppos_0'], task['to_area_0'], 'Vessel', task['form_id_0'],
#                                                 task['business_type_0'], task['vbay']))
#             # 构建双箱作业对应的xml字符串
#             else:
#                 if j != 3:
#                     task = all_data[name][i][j]
