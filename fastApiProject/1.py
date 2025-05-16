import selectors  # 用于处理非阻塞I/O操作的高级选择器库
import socket  # 提供对底层网络接口的访问
import threading  # 提供线程相关功能
import time  # 提供时间相关功能，如睡眠、获取当前时间等
import uvicorn  # 用于运行FastAPI应用的ASGI服务器
from fastapi import FastAPI, Query  # FastAPI框架核心类和查询参数处理
from fastapi.responses import JSONResponse  # 用于返回JSON格式的响应
from pydantic import BaseModel  # 用于数据验证和解析的库


# 定义任务数据模型，使用Pydantic来进行数据验证
class Task(BaseModel):
    che_id: str = 'A500'  # 车ID，默认值为'A500'
    form_id: str = 'FORM_TRUCK_EMPTY_TO_ORIGIN'  # 表单ID，默认值为'FORM_TRUCK_EMPTY_TO_ORIGIN'
    mvkd: str = 'DSCH'  # 移动代码，默认值为'DSCH'
    from_pos: str = 'Q302-0'  # 起始位置，默认值为'Q302-0'
    to_pos: str = '04E06F.1'  # 目标位置，默认值为'04E06F.1'


# 将消息转换为指定格式的字节数组
def build(message):
    data = bytearray(message, 'ascii')  # 将消息转换为字节数组
    length = len(data) + 2  # 计算消息长度（数据长度加上2个字节的头部）
    print('length', length)  # 打印消息长度
    # 构建消息字节数组，前两个字节为消息长度，中间为消息内容，最后一个字节为结束符
    m = bytes([length >> 8, length & 0xff]) + bytes.fromhex('1f 41') + data + bytes.fromhex('ff')
    print(m)  # 打印构建的消息
    return m  # 返回构建的消息


# 将消息发送到所有连接
def send_to_navis(message):
    for _, conn in enumerate(conn_list):  # 遍历所有连接
        try:
            conn.send(build(message))  # 发送构建的消息
        except Exception as e:
            print(f' send error:{e}')  # 如果发送失败，打印错误信息


# 另一个发送消息到生产环境的函数
def send_to_prod_navis(message):
    for _, conn in enumerate(conn_list):  # 遍历所有连接
        try:
            conn.send(build(message))  # 发送构建的消息
        except Exception as e:
            print(f' send error:{e}')  # 如果发送失败，打印错误信息


# 创建FastAPI应用实例
app = FastAPI()


# 定义POST请求处理函数，用于处理/navis_task端点
@app.post("/navis_task", response_class=JSONResponse, name="navis_tasks", tags=["navis"])
async def navis_task(
        che_id: str = Query(default='A500'),  # 查询参数，车ID，默认值为'A500'
        form_id: str = Query(enum=['FORM_TRUCK_EMPTY_TO_ORIGIN', 'FORM_TRUCK_LADEN_TO_DEST', 'FORM_TRUCK_IDLE']),
        # 表单ID，限定值
        mvkd: str = Query(enum=['DSCH', 'YARD', 'LOAD'], default='DSCH'),  # 移动代码，限定值，默认值为'DSCH'
        from_area_type: str = Query(enum=['YardBlock', 'Vessel'], default='Vessel'),  # 起始区域类型，限定值，默认值为'Vessel'
        from_pos: str = Query(default='Q10-0'),  # 起始位置，默认值为'Q10-0'
        to_area_type: str = Query(enum=['YardBlock', 'Vessel'], default='Vessel'),  # 目标区域类型，限定值，默认值为'Vessel'
        to_pos: str = Query(default='04D0606.1')  # 目标位置，默认值为'04D0606.1'
):
    print(che_id, form_id, mvkd, mvkd, from_pos, to_pos)  # 打印接收到的参数

    # 构建任务消息
    task = f'''<message formId="{form_id}" ack="N" MSID="-5240164"><che CHID="{che_id}" equipType="TRUCK" MTEU="2" 
    DSTA="ICTV" OPMD="TRUCK" CHASSIS="BOMBCART" status="Working" locale="en_US" location="05D5703.3" 
    userID="465026"><pool name="POOL_Q07"><list count="1" type="pow"><pow name="Q07" mode="TrucksOnly" 
    /></list></pool><work count="1" moveStage="PLANNED" planningIntent="SINGLE"><job MVKD="{mvkd}" pow="Q07" 
    age="799" priority="N" shift="0" moveStage="PLANNED"><container EQID="SEGU2161106" LNTH="40" QWGT="2300" MNRS="" 
    QCAT="T" EQTP="45G1" HGHT="2591" LOPR="ZGX" TRKC="" ACRR="HUAS21_048" DCRR="XINHM_232" RLSE="G" RFRT="" CCON="" 
    ISHZ="N" DWTS="0" ISGP="GP" GRAD="" RMRK="" JPOS="CTR" PUTJPOS="CTR" /><position PPOS="{from_pos}" 
    refID="V.HUAS21_048:B.13.02.04" AREA="Q07" AREA_TYPE="{from_area_type}" type="from" DOOR="U" VBAY="13B" 
    /><position PPOS="{to_pos}" refID="Y.TECT:EC..." AREA="EC" AREA_TYPE="{to_area_type}" type="to" DOOR="Y" 
    /></job></work><displayMsg msgID="0">No Error</displayMsg></che></message>'''

    send_to_navis(task)  # 发送任务消息到NAVIS系统

    return JSONResponse(status_code=200, content={'code': 0, 'msg': 'success'})  # 返回成功响应


# 定义POST请求处理函数，用于处理/navis_two_task端点
@app.post("/navis_two_task", response_class=JSONResponse, name="navis_tasks", tags=["navis"])
async def navis_two_task(
        che_id: str = Query(default='A500'),  # 查询参数，车ID，默认值为'A500'
        form_id: str = Query(enum=['FORM_TRUCK_EMPTY_TO_ORIGIN', 'FORM_TRUCK_LADEN_TO_DEST', 'FORM_TRUCK_IDLE']),
        # 表单ID，限定值
        mvkd: str = Query(enum=['DSCH', 'YARD', 'LOAD'], default='LOAD'),  # 移动代码，限定值，默认值为'LOAD'
        from_area_type_0: str = Query(enum=['YardBlock', 'Vessel', 'ITV'], default='YardBlock'),
        # 起始区域类型0，限定值，默认值为'YardBlock'
        from_pos_0: str = Query(default='04D0606.1'),  # 起始位置0，默认值为'04D0606.1'
        to_area_type_0: str = Query(enum=['YardBlock', 'Vessel', 'ITV'], default='Vessel'),  # 目标区域类型0，限定值，默认值为'Vessel'
        to_pos_0: str = Query(default='Q10-0'),  # 目标位置0，默认值为'Q10-0'
        from_area_type_1: str = Query(enum=['YardBlock', 'Vessel', 'ITV'], default='YardBlock'),
        # 起始区域类型1，限定值，默认值为'YardBlock'
        from_pos_1: str = Query(default='04D0606.1'),  # 起始位置1，默认值为'04D0606.1'
        to_area_type_1: str = Query(enum=['YardBlock', 'Vessel', 'ITV'], default='Vessel'),  # 目标区域类型1，限定值，默认值为'Vessel'
        to_pos_1: str = Query(default='Q10-0')  # 目标位置1，默认值为'Q10-0'
):
    print(che_id, form_id, mvkd, mvkd, from_pos_0, to_pos_0, from_pos_1, to_pos_1)  # 打印接收到的参数

    # 根据区域类型截取位置的前五个字符
    from_area_0 = from_pos_0[:5] if from_area_type_0 == 'YardBlock' else from_pos_0
    from_area_1 = from_pos_1[:5] if from_area_type_1 == 'YardBlock' else from_pos_1
    to_area_0 = to_pos_0[:5] if to_area_type_0 == 'YardBlock' else to_pos_0
    to_area_1 = to_pos_1[:5] if to_area_type_1 == 'YardBlock' else to_pos_1

    # 构建两个任务的消息
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
    /></job></work><displayMsg msgID="0">No Error</displayMsg></che></message>'''

    print(task)  # 打印任务消息
    send_to_navis(task)  # 发送任务消息到NAVIS系统

    return JSONResponse(status_code=200, content={'code': 0, 'msg': 'success'})  # 返回成功响应


# 定义POST请求处理函数，用于处理/cancel_navis_task端点
@app.post("/cancel_navis_task", response_class=JSONResponse, name="cancel_navis_task", tags=["navis"])
async def cancel_navis_task(
        che_id: str = Query(default='A500'),  # 查询参数，车ID，默认值为'A500'
        form_id: str = Query(enum=['FORM_TRUCK_EMPTY_TO_ORIGIN', 'FORM_TRUCK_LADEN_TO_DEST', 'FORM_TRUCK_IDLE'],
                             default='FORM_TRUCK_EMPTY_TO_ORIGIN'),  # 表单ID，限定值，默认值为'FORM_TRUCK_EMPTY_TO_ORIGIN'
):
    # 构建取消任务的消息
    cmd = f'<message type="2630" MSID="7" formId="{form_id}"><che CHID="{che_id}" action="X"/></message>'
    print(cmd)  # 打印取消任务的消息
    send_to_prod_navis(cmd)  # 发送取消任务的消息到NAVIS系统
    return JSONResponse(status_code=200, content={'code': 0, 'msg': 'success'})  # 返回成功响应


# 连接列表和连接计数映射
conn_list = []
conn_cnt_map = {}


# 定义Socket服务器
def sock_server(server_addr):
    sel = selectors.DefaultSelector()  # 创建选择器实例

    def accept(sock, mask):
        conn, addr = sock.accept()  # 接受连接
        conn.setblocking(False)  # 设置非阻塞模式
        sel.register(conn, selectors.EVENT_READ, read)  # 注册读取事件
        print(conn)  # 打印连接信息
        try:
            conn.send(build('<message type="2509" MSID="0"/>'))  # 发送初始化消息
            conn_list.append(conn)  # 添加连接到列表
            conn_cnt_map[conn] = 0  # 初始化连接计数
        except Exception as e:
            print(e)  # 打印异常信息
            sel.unregister(conn)  # 取消注册
            conn.close()  # 关闭连接

    def read(conn, mask):
        try:
            data = conn.recv(1024)  # 接收数据
            print(data)  # 打印接收到的数据
        except Exception as e:
            print(e)  # 打印异常信息

        time.sleep(1)  # 睡眠1秒

    def send():
        msgid = 1
        while True:
            for i, conn in enumerate(conn_list):  # 遍历所有连接
                try:
                    ping = f'<message type="1509" ack="Y" MSID="{msgid}"/>'  # 构建心跳消息
                    conn.send(build(ping))  # 发送心跳消息
                    msgid += 1  # 消息ID递增
                except Exception as e:
                    print(f' send error:{e}')  # 打印发送错误信息
                    print(conn)  # 打印连接信息
                    sel.unregister(conn)  # 取消注册
                    conn.close()  # 关闭连接
                    conn_list.remove(conn)  # 从列表中移除连接
                    break

            time.sleep(10)  # 每隔10秒发送一次心跳消息

    sock = socket.socket()  # 创建Socket对象
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 设置Socket选项,允许地址重用
    sock.bind(server_addr)  # 绑定地址
    sock.listen(5)  # 监听连接
    sock.setblocking(False)  # 设置非阻塞模式
    sel.register(sock, selectors.EVENT_READ, accept)  # 注册接受事件

    sendt = threading.Thread(target=send)  # 创建发送线程
    sendt.setDaemon(True)  # 设置为守护线程
    sendt.start()  # 启动发送线程

    while True:
        events = sel.select(timeout=1)  # 等待事件
        for key, mask in events:  # 处理事件
            callback = key.data
            try:
                callback(key.fileobj, mask)  # 调用回调函数
            except socket.error as e:
                pass
            except  Exception as e:
                pass


# 主程序入口
if __name__ == '__main__':
    def server():
        sock_server(("10.188.73.101", 13101))  # 启动Socket服务器


    t = threading.Thread(target=server)  # 创建服务器线程
    t.setDaemon(True)  # 设置为守护线程
    t.start()  # 启动服务器线程
    # http://127.0.0.1:8085/docs
    uvicorn.run(app, host='0.0.0.0', port=8085)  # 启动FastAPI应用



