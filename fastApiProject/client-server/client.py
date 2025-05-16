import socket  # 导入socket模块，用于网络通信


def start_client():
    """
    启动客户端的函数。
    连接到服务器并进行消息传递。
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建一个TCP/IP套接字
    try:
        client.connect(('127.0.0.1', 9999))  # 连接到服务器，地址为本地回环地址，端口为9999
    except ConnectionRefusedError:
        print("连接断开，服务端可能已经停止运行。。。")
        return
    except Exception as e:
        print(f"An error occurred while connecting to the server: {e}")
        return

    def close_client():
        print("关闭客户端连接")
        client.close()

    while True:
        # 主循环，发送消息并接收响应
        try:
            message = input("输入你的消息：")  # 从控制台输入消息
            if message.lower() == 'q':
                print("退出客户端程序。。。")
                break  # 如果输入为'q'，则退出循环
            send_message(client, message)
            response = receive_response(client)
            if response:
                print(f"来自服务端的回复：{response}")
            else:
                print("连接丢失。服务器可能已断开连接。")
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    # 确保在退出循环时关闭客户端连接
    close_client()


def send_message(client, message):
    """
    发送消息到服务器
    """
    try:
        client.send(message.encode('utf-8'))
    except Exception as e:
        print(f"发送消息时发生错误: {e}")


def receive_response(client):
    """
    从服务器接收响应
    """
    try:
        return client.recv(1024).decode('utf-8')
    except ConnectionResetError:
        return None
    except Exception as e:
        print(f"接收响应时发生错误: {e}")
        return None


if __name__ == "__main__":
    start_client()  # 如果是主模块，则启动客户端
