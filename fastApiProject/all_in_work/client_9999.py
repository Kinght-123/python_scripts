import socket
import threading
import time

import parse_navis_works
import basic

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
                        pass
                    else:
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

        for i in range(len(xml_ls[bridge_name])):
            j = i if i <= 5 else i % 6
            for data in xml_ls[bridge_name][i]:
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


def handle_client(client_socket, addr):
    print(f"Accepted connection from {addr}")
    threads = []
    for bridge_name_ in parse_navis_works.bridges:
        client_thread = threading.Thread(target=client_handler, args=(client_socket, bridge_name_, basic.WORK_LINE))
        threads.append(client_thread)
        client_thread.start()
    for client_thread in threads:
        client_thread.join()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 8081))
    server_socket.listen(5)
    print("Server started, waiting for connections...")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server interrupted. Closing...")
    finally:
        server_socket.close()


if __name__ == '__main__':
    main()
