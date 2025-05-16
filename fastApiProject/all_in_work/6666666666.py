import json
import redis
import socket
import threading
import time


# 定义一个函数，用于处理客户端连接
def client_handler(client_socket):
    for data in xml_ls:
        # 发送数据给客户端
        client_socket.send(data.encode())
        time.sleep(1)  # 1秒钟的延迟，模拟发送间隔

    # 发送完毕后关闭连接
    client_socket.close()


# 主函数，负责创建服务器Socket并监听连接
def main():
    # 创建TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定IP和端口
    server_socket.bind(("localhost", 8081))
    # 开始监听，最大连接数为5
    server_socket.listen(5)
    print("Server started, waiting for connections...")

    try:
        while True:
            # 接受客户端连接
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")

            # 创建新线程处理客户端请求
            client_thread = threading.Thread(target=client_handler, args=(client_socket,))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server interrupted. Closing...")


def create_two_tasks(
        che_id: str,
        eqid: str,
        lnth_0: int,
        lnth_1: int,
        qgwt_0: int,
        qgwt_1: int,
        putjpos_0: str,
        putjpos_1: str,
        target: str,
):
    data = f'''<message formId="FORM_TRUCK_EMPTY_TO_ORIGIN" ack="N" MSID="-106447">
      <che CHID="{che_id}" equipType="TRUCK" MTEU="2" DSTA="ICTY" OPMD="TRUCK" CHASSIS="BOMBCART" status="Working"
           locale="en_US" location="Q308" userID="160134">
        <pool name="Q308 POOL">
          <list count="1" type="pow">
            <pow name="Q308" mode="TrucksOnly"/>
          </list>
        </pool>
        <work count="2" moveStage="PLANNED" planningIntent="TWIN">
          <job MVKD="LOAD" pow="{target}" age="1164" priority="N" shift="7" moveStage="PLANNED">
            <container EQID="{eqid}" LNTH="{lnth_0}" QWGT="{qgwt_0}" MNRS="" QCAT="E" EQTP="22G1" HGHT="2591" LOPR="PAN" TRKC=""
                       ACRR="CHUANWW_15B" DCRR="XINDD_010" RLSE="" RFRT="" CCON="" ISHZ="N" DWTS="2" ISGP="GP" GRAD=""
                       RMRK="" JPOS="FWD" PUTJPOS="{putjpos_0}"/>
            <position PPOS="B087305.1" refID="Y.FICT:B08.73.05.2" AREA="B0873" AREA_TYPE="YardRow" type="from" DOOR="Y"/>
            <position PPOS="Q308-0" refID="V.XINDD_010:B.17.03.06" AREA="Q308" AREA_TYPE="Vessel" type="to" DOOR="Y"
                      VBAY="17B"/>
          </job>
          <job MVKD="LOAD" pow="{target}" age="1164" priority="N" shift="8" moveStage="PLANNED">
            <container EQID="{eqid}" LNTH="{lnth_1}" QWGT="{qgwt_1}" MNRS="" QCAT="E" EQTP="22G1" HGHT="2591" LOPR="PAN" TRKC=""
                       ACRR="CHUANWW_15B" DCRR="XINDD_010" RLSE="" RFRT="" CCON="" ISHZ="N" DWTS="2" ISGP="GP" GRAD=""
                       RMRK="" JPOS="AFT" PUTJPOS="{putjpos_1}"/>
            <position PPOS="B087305.2" refID="Y.FICT:B08.73.05.1" AREA="B0873" AREA_TYPE="YardRow" type="from" DOOR="Y"/>
            <position PPOS="Q308-0" refID="V.XINDD_010:B.19.03.06" AREA="Q308" AREA_TYPE="Vessel" type="to" DOOR="Y"
                      VBAY="19B"/>
          </job>
        </work>
        <displayMsg msgID="0">0 No Error</displayMsg>
      </che>
</message>'''
    return data


# 创建XML数据
def create_task(
        che_id: str,
        eqid: str,
        lnth: int,
        qwgt: int,
        putjpos: str,
        target: str,
        from_ppos: str,
        from_area: str,
        to_ppos: str,
        to_area: str,
):
    data = f'''<message formId="FORM_TRUCK_EMPTY_TO_ORIGIN" ack="N" MSID="-5953245">
        <che CHID="{che_id}" equipType="TRUCK" MTEU="2" DSTA="ICTY" OPMD="TRUCK" CHASSIS="BOMBCART" status="Working"
             locale="en_US" location="Q01" userID="465006">
            <pool name="POOL_Q01">
                <list count="1" type="pow">
                    <pow name="Q01" mode="TrucksOnly"/>
                </list>
            </pool>
            <work count="1" moveStage="PLANNED" planningIntent="SINGLE">
                <job MVKD="LOAD" pow="{target}" age="916" priority="N" shift="0" moveStage="PLANNED">
                    <container EQID="{eqid}" LNTH="{lnth}" QWGT="{qwgt}" MNRS="" QCAT="E" EQTP="45G1" HGHT="2896" LOPR="CMA"
                               TRKC="" ACRR="TRUCK" DCRR="WANGJLT_002" RLSE="" RFRT="" CCON="" ISHZ="N" DWTS="3" ISGP="GP"
                               GRAD="" RMRK="" JPOS="CTR" PUTJPOS="{putjpos}"/>
                    <position PPOS="{from_ppos}" refID="Y.TECT:01B.56.01.1" AREA="{from_area}" AREA_TYPE="YardRow" type="from"
                              DOOR="A" TKPS="2"/>
                    <position PPOS="{to_ppos}" refID="V.WANGJLT_002:A.46.07.82" AREA="{to_area}" AREA_TYPE="Vessel" type="to" DOOR="Y"
                              TKPS="2" VBAY="46A"/>
                </job>
            </work>
            <displayMsg msgID="0">No Error</displayMsg>
        </che>
</message>'''
    return data


# 连接到Redis数据库
redis_host = '10.188.73.101'
redis_port = 6379
redis_password = "Trunk@123"  # 如果你的Redis服务器有密码，请在这里填写密码
redis_db = 0  # Redis数据库索引，默认为0

# 岸桥和平板车的对应关系
WORK_LINE = {
    'Q108': ['A538', 'A539', 'A540', 'A541', 'A542', 'A543'],
    'Q109': [
        'A520',
        'A521',
        'A522',
        'A523',
        'A524',
        'A525',
    ],
    'Q110': [
        'A526',
        'A527',
        'A528',
        'A529',
        'A530',
        'A531',
    ],
    'Q111': [
        'A532',
        'A533',
        'A534',
        'A535',
        'A536',
        'A537',
    ]  #
}

# 集装箱在车上的位置，是车辆点位判断依据之一
putjpos_dict = {'1': 'FWD',  # 前
                '2': 'CTR',  # 中
                '3': 'AFT',  # 后
                }


def get_json(host, port, password, db):
    # 创建Redis连接
    r = redis.Redis(host=host, port=port, password=password, db=db)

    xml_ls = []
    key_name = "plan:move_tasks:*"
    keys = r.keys(key_name)
    print(f'{len(keys)}辆车')
    # 打印所有键
    for key in keys:
        key = key.decode('utf-8')
        che_id = key[-4:]
        # print(che_id)
        ls = r.lrange(key, 0, -1)
        for i in ls:
            i = i.decode('utf-8')
            l = json.loads(i)
            eqid = l['containers'][0]['id']
            pow = l['target']
            if len(l['containers']) == 1:
                lnth = l['containers'][0]['size']
                qwgt = l['containers'][0]['weight']
                putjpos = putjpos_dict.get(str(l['containers'][0]['position']), None)
                xml_data = create_task(che_id, eqid, lnth, qwgt, putjpos, pow)
            else:
                lnth_0 = l['containers'][0]['size']
                lnth_1 = l['containers'][1]['size']
                qwgt_0 = l['containers'][0]['weight']
                qwgt_1 = l['containers'][1]['weight']
                putjpos_0 = putjpos_dict.get(str(l['containers'][0]['position']), None)
                putjpos_1 = putjpos_dict.get(str(l['containers'][1]['position']), None)
                xml_data = create_two_tasks(che_id, eqid, lnth_0, lnth_1, qwgt_0, qwgt_1, putjpos_0, putjpos_1, pow)
            xml_ls.append(xml_data)
    return xml_ls


# get_json(redis_host, redis_port, redis_password, redis_db)
xml_ls = get_json(redis_host, redis_port, redis_password, redis_db)

if __name__ == '__main__':
    main()
