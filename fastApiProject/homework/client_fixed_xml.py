"""
    - 用户客户端测试连接，测试发送内容是否正确
"""

import socket
import xml.etree.ElementTree as ET


def main():
    def send_message(client, message):
        """
        发送消息到服务器
        """
        try:
            client.send(message.encode('utf-8'))
        except Exception as e:
            print(f"发送消息时发生错误: {e}")

    # 创建TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 连接服务器
    server_address = ("localhost", 8082)
    client_socket.connect(server_address)
    print(f"Connected to {server_address}")

    try:
        while True:
            # 接收数据
            data = client_socket.recv(8192).decode()
            if not data:
                print("No more data received. Stopping...")
                break

            # 输出接收到的数据
            # root = ET.fromstring(data)
            # che_id = root.find('.//che').get('CHID')
            # print(f'Received: {che_id}')
            print(data)
            # send_message(client_socket, f"{che_id}车辆已经收到任务！！！")
    except KeyboardInterrupt:
        print("Client interrupted. Closing...")
    finally:
        # 关闭客户端socket
        client_socket.close()


if __name__ == "__main__":
    main()
