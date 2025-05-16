from fastapi import FastAPI, WebSocket

app = FastAPI()

che_state_dict = {}


@app.websocket("/standard/che/{che_id}")
async def websocket_endpoint(websocket: WebSocket, che_id: str):
    await websocket.accept()
    while True:
        recv_data = await websocket.receive_json()
        msg_type = recv_data["MsgType"]
        if msg_type != "ReportHeartbeat":
            print(f"收到 {msg_type} 请求:", recv_data)
        # 初始化返回
        if msg_type == "RequestInitialize":
            res_data = {
                "MsgType": "RequestInitializeResponse",
                "MsgId": "20221103091125922332",
                "Result": "Y",
                "Code": "200",
                "Timestamp": "2022-11-03 14:23:30.229",
                "Message": "处理失败，原因……",
                "Data": {
                    "equipmentId": che_id,
                    "activeState": "Y",
                    "jobIDList": [
                        "01",
                        "02"
                    ],
                    "equipmentState": che_state_dict.get(che_id, "0"),
                    "truckType": "1",
                    "serverTime": "2023-02-01 14: 00: 00",
                    "username": "123",
                    "equipmentType": 9,
                    "selectMark": 0,
                    "targetJobId1": "",
                    "targetJobId2": "",
                    "jobList": []
                }
            }
            await websocket.send_json(res_data)
        elif msg_type == "Login":
            res_data = {
                "MsgType": "LoginResponse",
                "MsgId": "20221103091125922332",
                "Result": "Y",
                "Code": "200",
                "Timestamp": "2022-11-03 14:23:30.229",
                "Message": "处理失败，原因……",
                "Data": {
                    "equipmentId": che_id,
                    "username": "user1",
                    "equipmentType": "9"
                }
            }
            che_state_dict[che_id] = "U"
            await websocket.send_json(res_data)
        elif msg_type == "Activate":
            active_state = "N"
            if recv_data["Data"]["activeState"] == "Y":
                active_state = "Y"
            res_data = {
                "MsgType": "ActivateResponse",
                "MsgId": "20221103091125922332",
                "Result": "Y",
                "Code": "200",
                "Timestamp": "2022-11-03 14:23:30.229",
                "Message": "处理失败，原因……",
                "Data": {
                    "equipmentId": che_id,
                    "activeState": active_state
                }
            }
            che_state_dict[che_id] = "F"
            await websocket.send_json(res_data)
        elif msg_type == "Logout":
            res_data = {
                "MsgType": "LogoutResponse",
                "MsgId": "20221103091125922332",
                "Result": "Y",
                "Code": "200",
                "Timestamp": "2022-11-03 14:23:30.229",
                "Message": "处理失败，原因……",
                "Data": {
                    "equipmentId": "GN2687"
                }
            }
            await websocket.send_json(res_data)
        elif msg_type == "ReportHeartbeat":
            # 判断车辆是否可用
            che_state = che_state_dict.get(che_id, "0")
            if che_state == "0":
                print(f"{che_id} 未登录")
            elif che_state == "U":
                print(f"{che_id} 未激活")
            elif che_state == "F":
                print(f"{che_id} 空闲")
                res_data = {
                    "MsgType": "ReportTruckJob",
                    "MsgId": "20221103091125922332",
                    "Result": "Y",
                    "Code": "200",
                    "Timestamp": "2022-11-03 14:23:30.229",
                    "Message": "处理失败，原因……",
                    "Data": {
                        "truckID": che_id,
                        "truckJob": {
                            "jobID": "34902",
                            "jobType": "LOAD",
                            "container": {
                                "containerId": "EITU0331430",
                                "ISO": "22G1",
                                "emptyWeight": "",
                                "weight": 0,
                                "dangerous": "",
                                "VST": "",
                                "slct": "",
                                "containerSize": ""
                            },
                            "mailContainerType": "To",
                            "yardPosition": {
                                "blockId": "H01",
                                "bay": "65",
                                "lane": "",
                                "tier": "",
                                "cabinMark": "A",
                                "laneNum": "4",
                                "tlpMark": ""
                            },
                            "distributionTime": "2023-03-27T09:12:49.1697639+08:00",
                            "twinSign": "0",
                            "boxDirection": "F",
                            "planPositionType": "Y"
                        }
                    }
                }
                che_state_dict[che_id] = "B"
                await websocket.send_json(res_data)
            elif che_state == "B":
                print(f"{che_id} 繁忙")
        else:
            print("未知 msg:", recv_data)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app='jtos:app', host='0.0.0.0', port=9999)
