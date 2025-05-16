import socket
import time


def receive_data():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 8081))
    print("已连接到服务器")

    try:
        while True:  # 添加一个无限循环来持续接收数据
            data = client_socket.recv(8192)
            if not data:
                print("没有接收到数据，可能是服务器断开连接。")
                break  # 如果没有接收到数据，跳出循环
            print("接收到的数据：")
            print(data)
            # print(data)
            # print(data.decode('utf-8'))
            # 可以添加一些逻辑来处理接收到的数据
    except Exception as e:
        print(f'接收数据失败：{e}')
    finally:
        client_socket.close()  # 关闭socket连接
        print("连接已关闭")


if __name__ == "__main__":
    receive_data()