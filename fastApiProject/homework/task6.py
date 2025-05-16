import json
import socket
import threading
import time

import basic
import parse_navis_works
import create_xml_test

'''
    - 获取数据构造xml文件的函数先不用写
'''
pass

'''
    1. 从move_tasks里面取出数据，来构建xml
        - 如果车号对应的数据为None，那么从redis的navis_works里面取出数据，然后放到move_tasks里面
        - 如果车号里面有数据，则提取一条数据，构造出xml，然后发出
'''
pass
'''
    - 前提要判断一下是否为锁站任务，如果为锁站任务，则不用构造xml。
    - 2. 构造函数，输入为一个车辆的任务循环中的一条任务数据、che_id、一个车辆的任务循环，输出为构造好的xml    
'''


# 单箱作业的构建xml的函数
def create_base_xml_str(data: dict, che_id: str = 'che_id', works: dict = None) -> str:
    containers = data.get('containers')[0]
    base_xml = create_xml_test.create_task(
        che_id,  # che_id
        containers.get('id'),
        containers.get('size'),
        containers.get('weight'),
        basic.putjpos_dict.get(containers.get('position')),
        data.get('target'),
        works.get('tasks')[0].get('actual_destination'),
        works.get('tasks')[0].get('target'),
        'YardRow',  # from_area_type
        works.get('tasks')[-1].get('actual_destination'),
        works.get('tasks')[-1].get('target'),
        'Vessel',  # to_area_type
        basic.from_id.get(data.get('dest_type')),
        basic.business_type.get(data.get('act_business_type')),
        works.get('vbay'),
    )
    return base_xml


# task构建xml的函数,每次传入一个作业大循环和大循环中的一个小任务
def task_to_xml(data: dict, che_id: str = 'che_id', works: dict = None) -> str:
    xml_str = ""
    containers = data.get('containers')
    # 证明双箱作业
    if len(containers) == 2:
        container_0 = containers[0]
        container_1 = containers[1]

        xml_str = create_xml_test.create_two_tasks(
            che_id,
            container_0.get('id'),
            container_1.get('id'),
            container_0.get('size'),
            container_1.get('size'),
            container_0.get('weight'),
            container_1.get('weight'),
            basic.putjpos_dict.get(container_0.get('position')),
            basic.putjpos_dict.get(container_1.get('position')),
            works.get('tasks')[0].get('actual_destination'),
            works.get('tasks')[0].get('target'),
            'YardRow',  # from_area_type
            works.get('tasks')[1].get('actual_destination'),
            works.get('tasks')[1].get('target'),
            'Vessel',
            basic.from_id.get(data.get('dest_type')),
            data.get('target'),
            works.get('vbay'),

        )
    # 否则是单箱作业
    else:
        xml_str = create_base_xml_str(data, che_id, works)
    return xml_str


'''
    - 前提是只有判断move_tasks里面的车号有对应的数据才可以调用这个函数
    - 2. 每次从move_tasks里面取出一条数据，然后删除掉
'''


# 输出车号，从车号所对应的作业循环中提取出一个作业xml字符串
def func(che_id: str):
    # 连接数据库
    r = parse_navis_works.connect_redis(basic.redis_host, basic.redis_port, basic.redis_password, basic.redis_db)
    # 找到数据库中车辆待发送的任务的键
    key = f'sim:move_tasks:{che_id}'
    # 提取出一个作业循环中的一个任务
    task = r.lindex(key, -1)
    # 关闭数据库连接
    r.connection_pool.disconnect()

    if json.loads(task.decode('utf-8')).get('target') == 'PSTP':
        return None
    else:
        return task


# 定义一个函数，查找车辆所对应的岸桥是否还有任务
def check_bridge(key_name, r, che_id):
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


'''
    3. 发送数据,遍历车辆，首先判断move里面是否有任务
       - 如果有任务，则发送任务
       - 如果没有任务，然后去navis里面，判断navis里面对应的岸桥是否有任务
            - 如果有，则提取出来，放到move里
            - 如果没有，则岸桥对应的所有任务结束 
'''


# 发送初始化数据的处理
def client_handler(client_socket):
    # 存储没有任务的岸桥
    cur = set()
    # 连接数据库
    r = parse_navis_works.connect_redis(basic.redis_host, basic.redis_port, basic.redis_password, basic.redis_db)
    while len(cur) != basic.WORK_LINE.__len__():
        client_socket.settimeout(1)  # 设置超时时间为1秒
        for che_id in basic.CHE_IDS:
            # 如果任务存在
            if r.exists(f'sim:move_tasks:{che_id}') and func(che_id) is not None:
                task = func(che_id)
                print(che_id)
                print(task)
            else:
                # 如果车辆所对应的岸桥在redis数据库中还有数据
                if not check_bridge("sim:navis_works:*", r, che_id):
                    cur.add(get_bridge(che_id))
                else:
                    continue
            try:
                client_socket.send(task)
                # 尝试接收客户端消息
                try:
                    data = client_socket.recv(8192).decode()
                    if data:
                        print(f"Received from client: {data}")
                except socket.timeout:
                    pass  # 超时后继续发送下一个任务

                # 模拟发送间隔
                time.sleep(0.5)
            except (BrokenPipeError, ConnectionResetError, OSError):
                print(f"Connection to {client_socket.getpeername()} closed")
                pass


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
            # 接收客户端连接
            client_socket, address = server_socket.accept()
            print(f"Accepted connection from {address}")
            # 为每个客户端连接创建一个新的线程
            client_thread = threading.Thread(target=client_handler, args=(client_socket,))
            client_thread.start()

    except KeyboardInterrupt:
        print("Server interrupted. Closing...")
    finally:
        server_socket.close()


if __name__ == '__main__':
    main()


r = parse_navis_works.connect_redis(basic.redis_host, basic.redis_port, basic.redis_password, basic.redis_db)
