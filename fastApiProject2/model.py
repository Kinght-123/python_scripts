from pydantic import BaseModel, Field
from typing import List, Dict


class LaneData(BaseModel):
    lane_id: str = Field(..., description="车道id")
    load_ps: List[str] = Field(..., description="装锁站")
    dsch_ps: List[str] = Field(..., description="卸锁站")
    up_vpb: List[str] = Field(..., description="上行VPB")
    down_vpb: List[str] = Field(..., description="下行VPB")
    up_vpb_navi: List[str] = Field(..., description="上行vpb(navi)")
    down_vpb_navi: List[str] = Field(..., description="下行VPB(navi)")


class QCData(BaseModel):
    Q110: LaneData = Field(..., description="Q110船期设置")
    Q109: LaneData = Field(..., description="Q109船期设置")
