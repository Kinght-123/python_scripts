'''
    - 用于从处理好的数据列表中提取出xml数据，并通过socket模拟客户端发送xml数据
    - all_data -> all_xml
    - 多线程
'''

import socket
import threading
import time

import parse_navis_works
import basic
import subprocess

# xml_ls为临界资源
parse_navis_works.to_xml_ls(parse_navis_works.bridges, parse_navis_works.all_data)
xml_ls = parse_navis_works.all_xml


# 通过平板车获取对应岸桥的函数
def get_bridge(truck_id) -> (None, str):
    for key, values in basic.WORK_LINE.items():
        if truck_id in values:
            return key
    return None


# 把xml中的CHID字段补上对应的che_id
def che_id_xml(bridge_che_id: str, str_data: str) -> str:
    return str_data.replace('che_id', bridge_che_id)


# 获取一个进程锁
# lock = threading.Lock()


# 定义一个函数，用于处理客户端连接
# def client_handler(client_socket, bridge_name: str, work_line: dict):
#     connection_closed = False  # 用于跟踪连接是否已关闭
#     try:
#         # lock.acquire()
#         for i in range(len(xml_ls[bridge_name])):
#             j = i if i <= 5 else i % 6
#             for data in xml_ls[bridge_name][i]:
#                 data = che_id_xml(work_line[bridge_name][j], data)
#                 # print(data.replace('/n', ''))
#                 try:
#                     # 发送str数据给客户端
#                     client_socket.send(data.encode())
#                 except (BrokenPipeError, ConnectionResetError, OSError):
#                     # 如果客户端断开连接，则提前关闭连接
#                     if not connection_closed:
#                         connection_closed = True
#                         print(f"{bridge_name}  Connection Closed!!!")
#                         if isinstance(client_socket, socket.socket):
#                             client_socket.close()
#                     return
#                 time.sleep(5)  # 5秒钟的延迟，模拟发送间隔
#
#     finally:
#         if isinstance(client_socket, socket.socket) and not client_socket._closed:
#             client_socket.close()
#             if not connection_closed:
#                 print(f"{bridge_name}  Connection Closed!!!")
#         # lock.release()


data_str = ""
lock = threading.Lock()


def client_handler(client_socket, bridge_name: str, work_line: dict):
    connection_closed = False  # 用于跟踪连接是否已关闭
    client_socket.settimeout(1.0)  # 设置非阻塞接收的超时时间

    try:
        # 接收数据的线程或循环
        def receive_data():
            while not connection_closed:
                try:
                    reply_data = client_socket.recv(8192)  # 缓冲区大小为1024字节
                    if reply_data:
                        print(f"从 {bridge_name} 接收到: {data.decode()}")
                        continue
                    else:
                        # 如果没有数据，表示客户端已经关闭连接
                        return
                except socket.timeout:
                    continue  # 没有接收到数据，继续下一次迭代
                except (ConnectionResetError, OSError):
                    if not connection_closed:
                        print(f"{bridge_name} 连接已关闭！")
                        return

        # 以非阻塞方式启动接收数据的线程
        receiver_thread = threading.Thread(target=receive_data)
        receiver_thread.start()
        global data_str
        # 遍历任务
        for i in range(len(basic.WORK_LINE[bridge_name]), len(xml_ls[bridge_name])):
            j = i if i <= 5 else i % 6
            # 遍历车号
            for data in xml_ls[bridge_name][i]:
                # 如果车此时无任务，是空闲的，则发送数据
                if check_che_id(work_line[bridge_name][j]):
                    data_str = che_id_xml(work_line[bridge_name][j], data)
                    try:
                        client_socket.send(data_str.encode())
                    except (BrokenPipeError, ConnectionResetError, OSError):
                        if not connection_closed:
                            connection_closed = True
                            print(f"{bridge_name} 连接已关闭！")
                            if isinstance(client_socket, socket.socket):
                                client_socket.close()
                        return
                time.sleep(5)  # 5秒钟的延迟，模拟发送间隔
    finally:
        if isinstance(client_socket, socket.socket) and not client_socket._closed:
            client_socket.close()
            if not connection_closed:
                print(f"{bridge_name} 连接已关闭！")
        connection_closed = True


# 主函数，负责创建服务器Socket并监听连接
def main():
    # 创建TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定IP和端口
    server_socket.bind(("localhost", 8081))
    # 开始监听，最大连接数为5
    server_socket.listen(5)
    print("Server started, waiting for connections...")

    try:
        while True:
            # 接受客户端连接
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")

            # 存储线程列表
            threads = []
            # 创建新线程处理客户端请求
            for i, bridge_name_ in enumerate(parse_navis_works.bridges):
                client_thread = threading.Thread(target=client_handler,
                                                 args=(client_socket, bridge_name_, basic.WORK_LINE))
                threads.append(client_thread)
                client_thread.start()
            # 等待所有线程完成
            for client_thread in threads:
                client_thread.join()

    except KeyboardInterrupt:
        print("Server interrupted. Closing...")


# 初始化任务的函数
def begin_tasks() -> None:
    subprocess.run(['python', 'begin_work.py'])


# 判断车是否空闲的函数
def check_che_id(che_id: str) -> bool:
    return True


begin_tasks()
if __name__ == '__main__':
    main()
