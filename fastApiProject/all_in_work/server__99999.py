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
from try_generate import gen
from basic import bridges_all

# xml_ls为临界资源
parse_navis_works.to_xml_ls(parse_navis_works.bridges)
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

def main():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('127.0.0.1', 8081)
    tcp_socket.connect(server_address)
    # 还有岸桥的任务在继续
    if judge():
        for item in bridges_all:
            if item not in parse_navis_works.bridges:
                print(f'{item}岸桥的任务已经完成了！！！')


def judge():
    if xml_ls is not None:
        return True
    return False

# if __name__ == '__main__':
#     main()
