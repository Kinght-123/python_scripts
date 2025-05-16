import socket
import threading
import time

import parse_navis_works
import basic

# xml_ls为临界资源
parse_navis_works.to_xml_ls(parse_navis_works.bridges)
xml_ls = parse_navis_works.all_xml


# 把xml中的CHID字段补上对应的che_id
def che_id_xml(bridge_che_id: str, str_data: str) -> str:
    return str_data.replace('che_id', bridge_che_id)


# 客户端处理函数
def client_handler(client_socket):
    try:
        client_socket.settimeout(0.5)  # 设置超时时间为0.5秒

        # 提取出在工作的岸桥
        for item in parse_navis_works.bridges:
            print(f'{item}岸桥开始初始化发送任务...')
            # 提取出岸桥对应的车辆和索引
            for i, che_id in enumerate(basic.WORK_LINE[item]):
                for j in range(len(xml_ls[item][i])):
                    task = che_id_xml(che_id, xml_ls[item][i][j])
                    try:
                        client_socket.send(task.encode())

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
                        return
        print('岸桥初始化任务已经完成！！！')
    finally:
        client_socket.close()


# 主函数，负责创建服务器Socket并监听连接
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定IP和端口
    server_socket.bind(("localhost", 8081))
    # 开始监听，最大连接数为5
    server_socket.listen(5)
    print("Server started, waiting for connections...")

    try:
        while True:
            client_socket, address = server_socket.accept()
            print(f"Accepted connection from {address}")
            # 为每个客户端连接创建一个新的线程
            client_thread = threading.Thread(target=client_handler, args=(client_socket,))
            client_thread.start()
            break
    except KeyboardInterrupt:
        print("Server interrupted. Closing...")
    finally:
        server_socket.close()


if __name__ == '__main__':
    main()
