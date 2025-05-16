"""
    - 用于创建单箱的task任务的xml字符串
    - 用于创建双箱的task任务的xml字符串
    - all_data -> all_xml
"""


def create_task(
        che_id: str = 'A999',
        eqid: str = '',
        lnth: int = 0,
        qwgt: int = 0,
        putjpos: str = '',
        target: str = '',
        from_ppos: str = '',
        from_area: str = '',
        from_area_type: str = 'YardRow',
        to_ppos: str = '',
        to_area: str = '',
        to_area_type: str = 'Vessel',
        from_id: str = '',
        mvkd: str = '',
        vbay: str = '',
) -> str:
    data = f'''<message formId="{from_id}" ack="N" MSID="-5953245">
        <che CHID="{che_id}" equipType="TRUCK" MTEU="2" DSTA="ICTY" OPMD="TRUCK" CHASSIS="BOMBCART" status="Working"
             locale="en_US" location="{target}" userID="465006">
            <pool name="POOL_{target}">
                <list count="1" type="pow">
                    <pow name="{target}" mode="TrucksOnly"/>
                </list>
            </pool>
            <work count="1" moveStage="PLANNED" planningIntent="SINGLE">
                <job MVKD="{mvkd}" pow="{target}" age="916" priority="N" shift="0" moveStage="PLANNED">
                    <container EQID="{eqid}" LNTH="{lnth}" QWGT="{qwgt}" MNRS="" QCAT="E" EQTP="45G1" HGHT="2896" LOPR="CMA"
                               TRKC="" ACRR="TRUCK" DCRR="WANGJLT_002" RLSE="" RFRT="" CCON="" ISHZ="N" DWTS="3" ISGP="GP"
                               GRAD="" RMRK="" JPOS="{putjpos}" PUTJPOS="{putjpos}"/>
                    <position PPOS="{from_ppos}" refID="Y.TECT:01B.56.01.1" AREA="{from_area}" AREA_TYPE="{from_area_type}" type="from"
                              DOOR="A" TKPS="2" VBAY="{vbay}"/>
                    <position PPOS="{to_ppos}" refID="V.WANGJLT_002:A.46.07.82" AREA="{to_area}" AREA_TYPE="{to_area_type}" type="to" DOOR="Y"
                              TKPS="2" VBAY="{vbay}"/>
                </job>
            </work>
            <displayMsg msgID="0">No Error</displayMsg>
        </che>
</message>'''
    return data


# 创建两个任务的xml
def create_two_tasks(
        che_id: str = 'A999',
        eqid_0: str = '',
        eqid_1: str = '',
        lnth_0: int = 0,
        lnth_1: int = 0,
        qgwt_0: int = 0,
        qgwt_1: int = 0,
        putjpos_0: str = '',
        putjpos_1: str = '',
        from_ppos: str = '',
        from_area: str = '',
        from_area_type: str = 'YardRow',
        to_ppos: str = '',
        to_area: str = '',
        to_area_type: str = 'Vessel',
        from_id: str = '',
        mvkd: str = '',
        target: str = '',
        vbay: str = '',
) -> str:
    data = f'''<message formId="{from_id}" ack="N" MSID="-106447">
      <che CHID="{che_id}" equipType="TRUCK" MTEU="2" DSTA="ICTY" OPMD="TRUCK" CHASSIS="BOMBCART" status="Working"
           locale="en_US" location="{target}" userID="160134">
        <pool name="{target} POOL">
          <list count="1" type="pow">
            <pow name="{target}" mode="TrucksOnly"/>
          </list>
        </pool>
        <work count="2" moveStage="PLANNED" planningIntent="TWIN">
          <job MVKD="{mvkd}" pow="{target}" age="1164" priority="N" shift="7" moveStage="PLANNED">
            <container EQID="{eqid_0}" LNTH="{lnth_0}" QWGT="{qgwt_0}" MNRS="" QCAT="E" EQTP="22G1" HGHT="2591" LOPR="PAN" TRKC=""
                       ACRR="CHUANWW_15B" DCRR="XINDD_010" RLSE="" RFRT="" CCON="" ISHZ="N" DWTS="2" ISGP="GP" GRAD=""
                       RMRK="" JPOS="{putjpos_0}" PUTJPOS="{putjpos_0}"/>
            <position PPOS="{from_ppos}.1" refID="Y.FICT:B08.73.05.2" AREA="{from_area}" AREA_TYPE="{from_area_type}" type="from" DOOR="Y" 
                      VBAY="{vbay}"/>
            <position PPOS="{to_ppos}" refID="V.XINDD_010:B.17.03.06" AREA="{to_area}" AREA_TYPE="{to_area_type}" type="to" DOOR="Y"
                      VBAY="{vbay}"/>
          </job>
          <job MVKD="{mvkd}" pow="{target}" age="1164" priority="N" shift="8" moveStage="PLANNED">
            <container EQID="{eqid_1}" LNTH="{lnth_1}" QWGT="{qgwt_1}" MNRS="" QCAT="E" EQTP="22G1" HGHT="2591" LOPR="PAN" TRKC=""
                       ACRR="CHUANWW_15B" DCRR="XINDD_010" RLSE="" RFRT="" CCON="" ISHZ="N" DWTS="2" ISGP="GP" GRAD=""
                       RMRK="" JPOS="{putjpos_0}" PUTJPOS="{putjpos_1}"/>
            <position PPOS="{from_ppos}.2" refID="Y.FICT:B08.73.05.1" AREA="{from_area}" AREA_TYPE="{from_area_type}" type="from" DOOR="Y"
                      VBAY="{vbay}"/>
            <position PPOS="{to_ppos}" refID="V.XINDD_010:B.19.03.06" AREA="{to_area}" AREA_TYPE="{to_area_type}" type="to" DOOR="Y"
                      VBAY="{vbay}"/>
          </job>
        </work>
        <displayMsg msgID="0">0 No Error</displayMsg>
      </che>
</message>'''
    return data
