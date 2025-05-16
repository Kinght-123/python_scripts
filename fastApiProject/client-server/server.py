import socket
import threading
import time


def handle_client(client_socket):
    """
    处理客户端连接的函数。
    接收客户端的消息并响应。
    """
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Received from client: {message}")
            response = input("Enter your response: ")
            client_socket.send(response.encode('utf-8'))
        except ConnectionResetError:
            print("客户端意外断开连接")
            break
        except Exception as e:
            print(f"发生错误: {e}")
            break
    client_socket.close()


def start_server():
    """
    启动服务器的函数。
    创建套接字并监听传入连接。
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 8081))
    server.listen(5)
    print("服务器监听在端口 8081")

    active_clients = []  # 用于存储活跃客户端连接

    def accept_connections():
        while True:
            try:
                client_socket, addr = server.accept()
                print(f"接受来自 {addr} 的连接")
                active_clients.append(client_socket)
                # 创建新线程处理客户端连接
                client_handler = threading.Thread(target=handle_client, args=(client_socket,))
                client_handler.start()
            except OSError as e:
                print(f"接受连接时发生操作系统错误: {e}")
                break
            except Exception as e:
                print(f"接受连接时发生其他错误: {e}")
                break
            break

    accept_thread = threading.Thread(target=accept_connections)
    accept_thread.start()

    # 定时器检查无活跃客户端并关闭服务器
    # def check_active_clients():
    #     while True:
    #         time.sleep(3)  # 每隔3秒检查一次
    #         try:
    #             active_sockets = [client_socket for client_socket in active_clients if client_socket.fileno() != -1]
    #             if not active_sockets:
    #                 print("无活跃客户端连接。关闭服务器...")
    #                 server.close()
    #                 break
    #         except Exception as e:
    #             print(f"检查活跃客户端时发生错误: {e}")
    #             break
    #         break
    #
    # check_thread = threading.Thread(target=check_active_clients)
    # check_thread.start()


if __name__ == "__main__":
    start_server()
