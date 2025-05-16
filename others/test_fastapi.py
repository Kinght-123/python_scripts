from fastapi import FastAPI, Body
from typing import List, Dict

app = FastAPI()

@app.post("/master/add_ship/")
async def create_ship_setting(
    ship_id: str = Body(..., description="船期，与TOS指令中的vessel_id保持一致"),
    load_mode: str = Body("strict", description="装船模式，分free, strict, selective三种"),
    dsch_ps: List[Dict] = Body(None, description="卸锁站"),
    load_ps: List[Dict] = Body(None, description="装锁站"),
    down_vpb_master: List[Dict] = Body(None, description="下行VPB"),
    up_vpb_master: List[Dict] = Body(None, description="上行VPB"),
    down_vpb_navi: List[Dict] = Body(None, description="岸桥下行通道，规划用"),
    up_vpb_navi: List[Dict] = Body(None, description="岸桥上行通道，规划用"),
):
    # 处理逻辑
    return {
        "ship_id": ship_id,
        "load_mode": load_mode,
        "dsch_ps": dsch_ps,
        "load_ps": load_ps,
        "down_vpb_master": down_vpb_master,
        "up_vpb_master": up_vpb_master,
        "down_vpb_navi": down_vpb_navi,
        "up_vpb_navi": up_vpb_navi,
    }