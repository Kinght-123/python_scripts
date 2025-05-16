import selectors  # 选择器模块，用于多路复用I/O操作
import socket  # 套接字模块，用于网络通信
import threading  # 线程模块，用于并发操作
import time  # 时间模块，用于延时操作
import uvicorn  # Uvicorn模块，用于ASGI应用的服务器
from fastapi import FastAPI, Query  # 从FastAPI模块导入FastAPI应用和Query查询
from fastapi.responses import JSONResponse  # 从FastAPI模块导入JSON响应
from pydantic import BaseModel  # 从Pydantic模块导入BaseModel类，用于数据模型定义


class Task(BaseModel):  # 定义一个任务类，继承自BaseModel
    che_id: str = 'A500'  # 任务的che_id字段，默认值为'A500'
    form_id: str = 'FORM_TRUCK_EMPTY_TO_ORIGIN'  # 任务的form_id字段，默认值为'FORM_TRUCK_EMPTY_TO_ORIGIN'
    mvkd: str = 'DSCH'  # 任务的mvkd字段，默认值为'DSCH'
    from_pos: str = 'Q302-0'  # 任务的from_pos字段，默认值为'Q302-0'
    to_pos: str = '04E06F.1'  # 任务的to_pos字段，默认值为'04E06F.1'


def build(message):  # 定义一个构建消息的函数
    data = bytearray(message, 'ascii')  # 将消息转换为ASCII编码的字节数组
    length = len(data) + 2  # 计算消息的长度
    print('length', length)  # 打印消息的长度
    m = bytes([length >> 8, length & 0xff]) + bytes.fromhex('1f 41') + data + bytes.fromhex('ff')  # 构建完整的消息
    print(m)  # 打印消息
    return m  # 返回消息


def send_to_navis(message):  # 定义一个发送消息到Navis的函数
    for _, conn in enumerate(conn_list):  # 遍历连接列表
        try:
            conn.send(build(message))  # 尝试发送构建的消息
        except Exception as e:
            print(f' send error:{e}')  # 发送失败时打印错误信息


def send_to_prod_navis(message):  # 定义一个发送消息到生产Navis的函数
    # from navis_client import thread_main, client
    # thread_main()
    # time.sleep(1)
    # try:
    #     conn.send(build(message))
    # except Exception as e:
    #     print(f'client send error:{e}')

    for _, conn in enumerate(conn_list):  # 遍历连接列表
        try:
            conn.send(build(message))  # 尝试发送构建的消息
        except Exception as e:
            print(f' send error:{e}')  # 发送失败时打印错误信息


app = FastAPI()  # 创建FastAPI应用实例


@app.post("/navis_task", response_class=JSONResponse, name="navis_tasks", tags=["navis"])  # 定义POST接口，路径为/navis_task
async def navis_task(
        che_id: str = Query(default='A500'),  # 查询参数che_id，默认值为'A500'
        form_id: str = Query(enum=['FORM_TRUCK_EMPTY_TO_ORIGIN', 'FORM_TRUCK_LADEN_TO_DEST', 'FORM_TRUCK_IDLE']),
        # 查询参数form_id，限制可选值
        mvkd: str = Query(enum=['DSCH', 'YARD', 'LOAD'], default='DSCH'),  # 查询参数mvkd，限制可选值，默认值为'DSCH'
        from_area_type: str = Query(enum=['YardBlock', 'Vessel'], default='Vessel'),
        # 查询参数from_area_type，限制可选值，默认值为'Vessel'
        from_pos: str = Query(default='Q10-0'),  # 查询参数from_pos，默认值为'Q10-0'
        to_area_type: str = Query(enum=['YardBlock', 'Vessel'], default='Vessel'),
        # 查询参数to_area_type，限制可选值，默认值为'Vessel'
        to_pos: str = Query(default='04D0606.1')  # 查询参数to_pos，默认值为'04D0606.1'
):
    print(che_id, form_id, mvkd, mvkd, from_pos, to_pos)  # 打印查询参数

    task = f'''<message formId="{form_id}" ack="N" MSID="-5240164"><che CHID="{che_id}" equipType="TRUCK" MTEU="2" 
    DSTA="ICTV" OPMD="TRUCK" CHASSIS="BOMBCART" status="Working" locale="en_US" location="05D5703.3" 
    userID="465026"><pool name="POOL_Q07"><list count="1" type="pow"><pow name="Q07" mode="TrucksOnly" 
    /></list></pool><work count="1" moveStage="PLANNED" planningIntent="SINGLE"><job MVKD="{mvkd}" pow="Q07" 
    age="799" priority="N" shift="0" moveStage="PLANNED"><container EQID="SEGU2161106" LNTH="40" QWGT="2300" MNRS="" 
    QCAT="T" EQTP="45G1" HGHT="2591" LOPR="ZGX" TRKC="" ACRR="HUAS21_048" DCRR="XINHM_232" RLSE="G" RFRT="" CCON="" 
    ISHZ="N" DWTS="0" ISGP="GP" GRAD="" RMRK="" JPOS="CTR" PUTJPOS="CTR" /><position PPOS="{from_pos}" 
    refID="V.HUAS21_048:B.13.02.04" AREA="Q07" AREA_TYPE="{from_area_type}" type="from" DOOR="U" VBAY="13B" 
    /><position PPOS="{to_pos}" refID="Y.TECT:EC..." AREA="EC" AREA_TYPE="{to_area_type}" type="to" DOOR="Y" 
    /></job></work><displayMsg msgID="0">No Error</displayMsg></che></message>'''  # 构建任务XML消息

    send_to_navis(task)  # 发送任务消息到Navis

    return JSONResponse(status_code=200, content={'code': 0, 'msg': 'success'})  # 返回成功响应


@app.post("/navis_two_task", response_class=JSONResponse, name="navis_tasks",
          tags=["navis"])  # 定义POST接口，路径为/navis_two_task
async def navis_two_task(
        che_id: str = Query(default='A500'),  # 查询参数che_id，默认值为'A500'
        form_id: str = Query(enum=['FORM_TRUCK_EMPTY_TO_ORIGIN', 'FORM_TRUCK_LADEN_TO_DEST', 'FORM_TRUCK_IDLE']),
        # 查询参数form_id，限制可选值
        mvkd: str = Query(enum=['DSCH', 'YARD', 'LOAD'], default='LOAD'),  # 查询参数mvkd，限制可选值，默认值为'LOAD'
        from_area_type_0: str = Query(enum=['YardBlock', 'Vessel', 'ITV'], default='YardBlock'),
        # 查询参数from_area_type_0，限制可选值，默认值为'YardBlock'
        from_pos_0: str = Query(default='04D0606.1'),  # 查询参数from_pos_0，默认值为'04D0606.1'
        to_area_type_0: str = Query(enum=['YardBlock', 'Vessel', 'ITV'], default='Vessel'),
        # 查询参数to_area_type_0，限制可选值，默认值为'Vessel'
        to_pos_0: str = Query(default='Q10-0'),  # 查询参数to_pos_0，默认值为'Q10-0'
        from_area_type_1: str = Query(enum=['YardBlock', 'Vessel', 'ITV'], default='YardBlock'),
        # 查询参数from_area_type_1，限制可选值，默认值为'YardBlock'
        from_pos_1: str = Query(default='04D0606.1'),  # 查询参数from_pos_1，默认值为'04D0606.1'
        to_area_type_1: str = Query(enum=['YardBlock', 'Vessel', 'ITV'], default='Vessel'),  # 查询参数to_area_type_1
        # ，限制可选值，默认值为'Vessel'
        to_pos_1: str = Query(default='Q10-0'),  # 查询参数to_pos_1，默认值为'Q10-0'
):
    print(che_id, form_id, mvkd, mvkd, from_pos_0, to_pos_0, from_pos_1, to_pos_1)  # 打印查询参数

    from_area_0 = from_pos_0  # 初始化from_area_0为from_pos_0
    from_area_1 = from_pos_1  # 初始化from_area_1为from_pos_1
    to_area_0 = to_pos_0  # 初始化to_area_0为to_pos_0
    to_area_1 = to_pos_1  # 初始化to_area_1为to_pos_1
    if from_area_type_0 == 'YardBlock':  # 如果from_area_type_0为'YardBlock'
        from_area_0 = from_pos_0[:5]  # 截取from_pos_0的前5个字符作为from_area_0

    if from_area_type_1 == 'YardBlock':  # 如果from_area_type_1为'YardBlock'
        from_area_1 = from_pos_1[:5]  # 截取from_pos_1的前5个字符作为from_area_1

    if to_area_type_0 == 'YardBlock':  # 如果to_area_type_0为'YardBlock'
        to_area_0 = to_pos_0[:5]  # 截取to_pos_0的前5个字符作为to_area_0

    if to_area_type_1 == 'YardBlock':  # 如果to_area_type_1为'YardBlock'
        to_area_1 = to_pos_1[:5]  # 截取to_pos_1的前5个字符作为to_area_1

    task = f'''<message formId="{form_id}" ack="N" MSID="-5240164"><che CHID="{che_id}" equipType="TRUCK" MTEU="2" 
    DSTA="ICTV" OPMD="TRUCK" CHASSIS="BOMBCART" status="Working" locale="en_US" location="05D5703.3" 
    userID="465026"><pool name="POOL_Q07"><list count="1" type="pow"><pow name="Q07" mode="TrucksOnly" 
    /></list></pool><work count="1" moveStage="PLANNED" planningIntent="SINGLE"><job MVKD="{mvkd}" pow="Q07" 
    age="799" priority="N" shift="0" moveStage="PLANNED"><container EQID="SEGU2161106" LNTH="20" QWGT="2300" MNRS="" 
    QCAT="T" EQTP="45G1" HGHT="2591" LOPR="ZGX" TRKC="" ACRR="HUAS21_048" DCRR="XINHM_232" RLSE="G" RFRT="" CCON="" 
    ISHZ="N" DWTS="0" ISGP="GP" GRAD="" RMRK="" JPOS="AFT" PUTJPOS="AFT" /><position PPOS="{from_pos_0}" 
    refID="V.HUAS21_048:B.13.02.04" AREA="{from_area_0}" AREA_TYPE="{from_area_type_0}" type="from" DOOR="U" 
    VBAY="13B" /><position PPOS="{to_pos_0}" refID="Y.TECT:EC..." AREA="{to_area_0}" AREA_TYPE="{to_area_type_0}" 
    type="to" DOOR="Y" /></job><job MVKD="{mvkd}" pow="Q07" age="799" priority="N" shift="0" 
    moveStage="PLANNED"><container EQID="SEGU2161106" LNTH="20" QWGT="2300" MNRS="" QCAT="T" EQTP="45G1" HGHT="2591" 
    LOPR="ZGX" TRKC="" ACRR="HUAS21_048" DCRR="XINHM_232" RLSE="G" RFRT="" CCON="" ISHZ="N" DWTS="0" ISGP="GP" 
    GRAD="" RMRK="" JPOS="FWD" PUTJPOS="FWD" /><position PPOS="{from_pos_1}" refID="V.HUAS21_048:B.13.02.04" AREA="
    {from_area_1}" AREA_TYPE="{from_area_type_1}" type="from" DOOR="U" VBAY="13B" /><position PPOS="{to_pos_1}" 
    refID="Y.TECT:EC..." AREA="{to_area_1}" AREA_TYPE="{to_area_type_1}" type="to" DOOR="Y" 
    /></job></work><displayMsg msgID="0">No Error</displayMsg></che></message>'''  # 构建任务XML消息
    print(task)  # 打印任务消息
    send_to_navis(task)  # 发送任务消息到Navis

    return JSONResponse(status_code=200, content={'code': 0, 'msg': 'success'})  # 返回成功响应


@app.post("/cancel_navis_task", response_class=JSONResponse, name="cancel_navis_task",
          tags=["navis"])  # 定义POST接口，路径为/cancel_navis_task
async def cancel_navis_task(
        che_id: str = Query(default='A500'),  # 查询参数che_id，默认值为'A500'
        form_id: str = Query(enum=['FORM_TRUCK_EMPTY_TO_ORIGIN', 'FORM_TRUCK_LADEN_TO_DEST', 'FORM_TRUCK_IDLE'],
                             default='FORM_TRUCK_EMPTY_TO_ORIGIN'),
        # 查询参数form_id，限制可选值，默认值为'FORM_TRUCK_EMPTY_TO_ORIGIN'
):
    cmd = f'<message type="2630" MSID="7" formId="{form_id}"><che CHID="{che_id}" action="X"/></message>'  # 构建取消任务的XML消息
    print(cmd)  # 打印取消任务消息
    send_to_prod_navis(cmd)  # 发送取消任务消息到生产Navis
    return JSONResponse(status_code=200, content={'code': 0, 'msg': 'success'})  # 返回成功响应


conn_list = []  # 初始化连接列表
conn_cnt_map = {}  # 初始化连接计数映射


def sock_server(server_addr):  # 定义套接字服务器函数
    sel = selectors.DefaultSelector()  # 创建默认选择器

    def accept(sock, mask):  # 定义接受连接的函数
        conn, addr = sock.accept()  # 接受连接
        conn.setblocking(False)  # 设置非阻塞
        sel.register(conn, selectors.EVENT_READ, read)  # 注册读取事件
        print(conn)  # 打印连接
        try:
            conn.send(build('<message type="2509" MSID="0"/>'))  # 尝试发送初始化消息
            conn_list.append(conn)  # 添加连接到连接列表
            conn_cnt_map[conn] = 0  # 初始化连接计数映射
        except Exception as e:
            print(e)  # 打印错误信息
            sel.unregister(conn)  # 取消注册连接
            conn.close()  # 关闭连接

    def read(conn, mask):  # 定义读取数据的函数
        try:
            data = conn.recv(1024)  # 接收数据
            print(data)  # 打印数据
        except Exception as e:
            print(e)  # 打印错误信息

        time.sleep(1)  # 延时1秒

    def send():  # 定义发送数据的函数
        msgid = 1  # 初始化消息ID
        while True:
            for i, conn in enumerate(conn_list):  # 遍历连接列表
                try:
                    ping = f'<message type="1509" ack="Y" MSID="{msgid}"/>'  # 构建ping消息
                    conn.send(build(ping))  # 发送ping消息
                    msgid += 1  # 增加消息ID
                except Exception as e:
                    print(f' send error:{e}')  # 打印发送错误信息
                    print(conn)  # 打印连接
                    sel.unregister(conn)  # 取消注册连接
                    conn.close()  # 关闭连接
                    conn_list.remove(conn)  # 从连接列表中移除连接
                    break

            time.sleep(10)  # 延时10秒

    sock = socket.socket()  # 创建套接字
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 设置套接字选项
    sock.bind(server_addr)  # 绑定地址
    sock.listen(5)  # 监听连接
    sock.setblocking(False)  # 设置非阻塞
    sel.register(sock, selectors.EVENT_READ, accept)  # 注册接受连接事件

    sendt = threading.Thread(target=send)  # 创建发送线程
    sendt.setDaemon(True)  # 设置为守护线程
    sendt.start()  # 启动发送线程

    while True:
        events = sel.select(timeout=1)  # 选择事件
        for key, mask in events:  # 遍历事件
            callback = key.data  # 获取回调函数
            try:
                callback(key.fileobj, mask)  # 调用回调函数
            except socket.error as e:
                pass  # 忽略套接字错误
            except Exception as e:
                pass  # 忽略其他错误


if __name__ == '__main__':  # 主程序入口
    def server():  # 定义服务器函数
        sock_server(("10.188.73.101", 13101))  # 启动套接字服务器


    t = threading.Thread(target=server)  # 创建服务器线程
    t.setDaemon(True)  # 设置为守护线程
    t.start()  # 启动服务器线程
    # http://127.0.0.1:8085/docs
    uvicorn.run(app, host='0.0.0.0', port=8085)  # 启动Uvicorn服务器
