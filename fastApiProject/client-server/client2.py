
import socket
import time


def receive_data():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 8081))
    print("已连接到服务器")

    # 接收数据
    data = client_socket.recv(8192)
    print("接收到的数据：")
    print(data.decode('utf-8'))

    time.sleep(5)
    bk = '连接已关闭'
    client_socket.send(bk.encode('utf-8'))
    client_socket.close()
    print("连接已关闭")


if __name__ == "__main__":
    receive_data()
