import socket
import time


def connect_to_server():
    # 创建客户端套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8081)

    try:
        # 连接到服务器
        client_socket.connect(server_address)
        print("已连接到服务器")

        while True:
            # 接收服务器发送的XML数据
            xml_data = client_socket.recv(4096).decode('utf-8')
            print(f"收到的XML数据:\n{xml_data}")

            # 模拟处理数据的时间
            time.sleep(2)

            # # 发送确认消息到服务器
            # message = "服务器已收到消息"
            # client_socket.sendall(message.encode('utf-8'))
            # print("发送确认消息")

            # 条件判断是否继续运行，例如在特定条件下退出循环
            # 在这个示例中，客户端将继续运行，直到用户手动停止
            # 可以添加特定的逻辑来控制客户端的退出条件
            # message = input("输入'连接已关闭'以断开连接或继续接收消息: ")
            # if message == "连接已关闭":
            #     client_socket.sendall(message.encode('utf-8'))
            #     break

    except Exception as e:
        print(f"连接服务器时发生错误: {e}")

    finally:
        client_socket.close()
        print("已断开与服务器的连接")


if __name__ == "__main__":
    connect_to_server()
