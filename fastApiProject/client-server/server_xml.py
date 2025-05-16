import socket
import threading
import time
from tqdm import tqdm


# 创建XML数据
def create_xml_data():
    xml_str = '''<message formId="FORM_TRUCK_EMPTY_TO_ORIGIN" ack="N" MSID="-5953245">
    <che CHID="PE411" equipType="TRUCK" MTEU="2" DSTA="ICTY" OPMD="TRUCK" CHASSIS="BOMBCART" status="Working"
         locale="en_US" location="Q01" userID="465006">
        <pool name="POOL_Q01">
            <list count="1" type="pow">
                <pow name="Q01" mode="TrucksOnly"/>
            </list>
        </pool>
        <work count="1" moveStage="PLANNED" planningIntent="SINGLE">
            <job MVKD="LOAD" pow="Q01" age="916" priority="N" shift="0" moveStage="PLANNED">
                <container EQID="TRHU8108829" LNTH="40" QWGT="30740" MNRS="" QCAT="E" EQTP="45G1" HGHT="2896" LOPR="CMA"
                           TRKC="" ACRR="TRUCK" DCRR="WANGJLT_002" RLSE="" RFRT="" CCON="" ISHZ="N" DWTS="3" ISGP="GP"
                           GRAD="" RMRK="" JPOS="CTR" PUTJPOS="CTR"/>
                <position PPOS="01B5601.1" refID="Y.TECT:01B.56.01.1" AREA="01B56" AREA_TYPE="YardRow" type="from"
                          DOOR="A" TKPS="2"/>
                <position PPOS="Q01-0" refID="V.WANGJLT_002:A.46.07.82" AREA="Q01" AREA_TYPE="Vessel" type="to" DOOR="Y"
                          TKPS="2" VBAY="46A"/>
            </job>
        </work>
        <displayMsg msgID="0">No Error</displayMsg>
    </che>
</message>'''
    return xml_str


# 创建一个列表存储客户端地址
ls = []
# 创建一个锁对象，用于线程安全地操作列表
ls_lock = threading.Lock()
# 用于控制服务器运行状态的全局变量
server_running = True


def countdown_timer(seconds: int):
    for i in tqdm(range(seconds), desc="服务器关闭", unit="s"):
        time.sleep(1)
    print("服务器已经关闭")


# 处理客户端连接
def handle_client(client_socket, client_address, server_socket):
    global ls
    global server_running
    print(f"客户端 {client_address} 已连接")

    # 获取锁，安全地操作 ls 列表
    with ls_lock:
        ls.append(client_address)
    print(f'连接的用户端有：{ls}')

    try:
        while True:
            # 创建XML数据并发送给客户端
            xml_data = create_xml_data()
            client_socket.sendall(xml_data.encode('utf-8'))

            print("已发送XML数据")

            # # 接收客户端的消息
            # message = client_socket.recv(1024).decode('utf-8')
            # print(f"客户端消息: {message}")
            #
            # # 检查客户端是否请求断开连接
            # if message == "连接已关闭":
            #     break
            # else:
            #     # 回复客户端
            #     response = "服务器已收到消息"
            #     client_socket.sendall(response.encode('utf-8'))
            time.sleep(5)  # 间隔5s发送信息，模拟信息处理
    except Exception as e:
        print(f"处理客户端 {client_address} 时发生错误: {e}")

    finally:
        # 获取锁，安全地操作 ls 列表
        with ls_lock:
            ls.remove(client_address)
            client_socket.close()
            print(f"客户端 {client_address} 已断开连接")
            print(f'连接的用户端有：{ls}')

            # 检测连接的用户端列表是否为空，如果为空则关闭服务端
            if not ls:
                print("没有客户端连接，10s后关闭服务器...")
                countdown_timer(10)
                server_running = False
                server_socket.close()


# 配置服务器
def start_server():
    global server_running
    # 创建服务器套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 设置SO_REUSEADDR选项
    server_socket.bind(("localhost", 8081))  # 使用更高的端口号
    server_socket.listen(5)
    print("服务器已启动，等待客户端连接...")

    while server_running:
        try:
            # 接受客户端连接
            client_socket, client_address = server_socket.accept()
            # 创建一个线程处理客户端连接
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, server_socket))
            client_thread.start()
        except OSError:
            break


if __name__ == "__main__":
    start_server()
