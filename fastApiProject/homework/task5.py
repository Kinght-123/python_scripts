import json
import socket
import threading
import time

import basic
import parse_navis_works
import create_xml_test

'''
    - 写一个函数，
'''

'''
    - 1. 初始化数据，把数据写入到redis中(默认是有数据的)
'''


# 初始化，将数据写入到redis中的函数
def write_redis(all_data: dict):
    # 创建Redis连接
    r = parse_navis_works.connect_redis(basic.redis_host, basic.redis_port, basic.redis_password, basic.redis_db)

    # 创建一个Redis Pipeline
    pipeline = r.pipeline()

    # 在redis数据库中填写数据
    for q_key, trucks in basic.WORK_LINE.items():
        for cur, truck in enumerate(trucks):
            key = f'test:{truck}'
            # 删除原来的数据
            pipeline.delete(key)
            tasks = all_data[q_key][cur]
            for task in tasks:
                # 添加数据
                pipeline.lpush(key, json.dumps(task))

    # 执行批量操作
    pipeline.execute()

    # 关闭数据库连接
    r.connection_pool.disconnect()
    # print("车辆初始化完成，数据已经成功写入到redis数据库中！！！")


# 测试一下提取出最右侧的任务并删除
# key1 = 'test:A520'
# a = r.rpop(key1)
# print(a.decode('utf-8'))

'''
    - 2. 构造函数，输入为一个车辆的任务循环中的一条任务数据和che_id，输出为构造好的xml
'''


# 单箱作业的构建xml的函数
def create_base_xml_str(data: dict, che_id: str = 'che_id') -> str:
    base_xml = create_xml_test.create_task(
        che_id,  # che_id
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


# task构建xml的函数
def task_to_xml(data: dict, che_id: str = 'che_id') -> str:
    xml_str = ""
    # 证明双箱作业
    if "eqid_1" in data.keys():
        xml_str = create_xml_test.create_two_tasks(
            che_id,  # che_id
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
        xml_str = create_base_xml_str(data, che_id)
    return xml_str


'''
    - 3. 再次连接数据库，每次取出一条数据，并构造xml
'''


# 输出车号，从车号所对应的作业循环中提取出一个作业xml字符串
def func(che_id: str) -> str:
    # 连接数据库
    r = parse_navis_works.connect_redis(basic.redis_host, basic.redis_port, basic.redis_password, basic.redis_db)

    # 找到数据库中车辆待发送的任务的键
    key = f'test:{che_id}'
    # 提取出一个作业循环中的一个任务
    task = r.rpop(key)
    # 关闭数据库连接
    r.connection_pool.disconnect()
    return task_to_xml(json.loads(task.decode('utf-8')), che_id)


'''
    - 把Redis中的岸桥中的对应数据添加到test:{che_id}中
'''


# 后续可能会修改, 通过车号，从对应岸桥的navis任务中取出一个放到test里面
def navis_to_test(che_id: str):
    # 创建Redis连接
    r = parse_navis_works.connect_redis(basic.redis_host, basic.redis_port, basic.redis_password, basic.redis_db)

    # 创建一个Redis Pipeline
    pipeline = r.pipeline()

    # test为船的名称
    key_name = "sim:navis_works:*"
    test = r.keys(key_name)[0].decode('utf-8').split(':')[2]
    navis_key = f'sim:navis_works:{test}:{get_bridge(che_id)}'

    # 提取出岸桥的一个作业循环
    tasks = r.lindex(navis_key, -1)     # tasks = r.rpop(navis_key)

    test_key = f'test:{che_id}'
    for task in json.loads(tasks.decode('utf-8')):
        # 添加数据
        pipeline.lpush(test_key, json.dumps(task))
    # 执行批量操作
    pipeline.execute()
    # 关闭数据库连接
    r.connection_pool.disconnect()


# 定义一个函数，查找车辆所对应的岸桥是否还有任务
def check_bridge(key_name, r, che_id) -> bool:
    test = r.keys(key_name)[0].decode('utf-8').split(':')[2]
    # 如果车辆所对应的岸桥还有任务
    if r.exists(f'sim:navis_works:{test}:{get_bridge(che_id)}'):
        return True
    else:
        return False


# 通过平板车获取对应岸桥的函数
def get_bridge(truck_id) -> (None, str):
    for key, values in basic.WORK_LINE.items():
        if truck_id in values:
            return key
    return None


# print(func('A520'))

'''
    - 4. 发送初始化的数据
        - 遍历所有的车号，发送数据库中对应车号的第一条数据并删除。
        - 接下来就进入到正常发送任务，处理任务的逻辑当中了。
        - 首先判断rendis中车号的数据是否为None，
            - 如果为None，则说明没有数据，需要从数据中取出一组数据放入到redis中；
            - 如果不为None，判断车是否为空闲状态
                - 如果为空闲状态，从redis中取出一条数据发送；
                - 如果不为空闲状态，继续循环                 
'''


# 发送初始化数据的处理
def client_handler(client_socket):
    try:
        client_socket.settimeout(1)  # 设置超时时间为1秒
        # 用于保证第一次发送初始化任务
        tag = True
        while tag:
            # 提取出在工作的岸桥
            for item in parse_navis_works.bridges:
                print(f'{item}岸桥开始初始化发送任务...')
                # 提取出岸桥对应的车辆和索引
                for i, che_id in enumerate(basic.WORK_LINE[item]):
                    # 根据车号从redis数据里提取出一条任务
                    task = func(che_id)
                    # print(type(task))
                    try:
                        client_socket.send(task.encode())
                        # 模拟发送间隔
                        time.sleep(0.5)
                    except (BrokenPipeError, ConnectionResetError, OSError):
                        print(f"Connection to {client_socket.getpeername()} closed")
                        return
            tag = False
        # 尝试接收客户端消息
        try:
            data = client_socket.recv(8192).decode()
            if data:
                print(f"Received from client: {data}")
        except socket.timeout:
            pass  # 超时后继续发送下一个任务
    finally:
        client_socket.close()


# 初始化发送任务的线程
# def begin_task(server_socket):
#     client_socket, address = server_socket.accept()
#     print(f"Accepted connection from {address}")
#     # 为每个客户端连接创建一个新的线程
#     client_thread = threading.Thread(target=client_handler, args=(client_socket,))
#     client_thread.start()
#     server_socket.close()


# 主函数，负责创建服务器Socket并监听连接
def main():
    # 创建TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定IP和端口
    server_socket.bind(("localhost", 8082))
    # 开始监听，最大连接数为5
    server_socket.listen(5)
    print("Server started, waiting for connections...")

    try:
        while True:
            # 接受客户端连接
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")

            # 构建线程， 线程启动
            server_thread = threading.Thread(target=client_handler, args=(client_socket,))
            server_thread.start()
    except KeyboardInterrupt:
        print("Server interrupted. Closing...")


if __name__ == "__main__":
    # 初始化数据
    a = parse_navis_works.get_redis_data(basic.redis_host, basic.redis_port, basic.redis_password, basic.redis_db)
    b = a.copy()
    write_redis(b)
    print("初始化数据已经成功写入到redis缓存中！！！")
    main()
