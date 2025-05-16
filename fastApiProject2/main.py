from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List

app = FastAPI()


# 定义请求模型
class PowConfig(BaseModel):
    lane_id: str
    pow_down_vpb: List[str]  # pow_down_vpb: Optional[List[str]] = None  # 允许缺失或为
    pow_up_vpb: List[str]


class VpbConfig(BaseModel):
    down_vpb: List[str]
    up_vpb: List[str]


class PsConfig(BaseModel):
    load_ps: List[str]
    dsch_ps: List[str]


class ShipConfig(BaseModel):
    ship_id: str
    load_mode: str
    pow: Dict[str, PowConfig]
    vpb: VpbConfig
    ps: PsConfig

    class Config:
        schema_extra = {
            "example": {
                "ship_id": "test_ship",
                "load_mode": "free",
                "pow": {
                    "Q109": {
                        "lane_id": "6",
                        "pow_down_vpb": ["110", "112"],
                        "pow_up_vpb": ["220", "221"]
                    },
                    "Q111": {
                        "lane_id": "7",
                        "pow_down_vpb": ["110", "112"],
                        "pow_up_vpb": ["220", "221"]
                    }
                },
                "vpb": {
                    "down_vpb": ["110", "112"],
                    "up_vpb": ["220", "221"]
                },
                "ps": {
                    "load_ps": ["110", "112"],
                    "dsch_ps": ["220", "221"]
                },
            }
        }


class ShipId(BaseModel):
    ShipId: str


from fastapi import FastAPI, Body

app = FastAPI()


@app.get("/add-down-vpb-master/{ship_id}")
async def add_down_vpb_master(ship_id: str):
    return {"message": "Data received", "ship_id": ship_id}


def main():
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == '__main__':
    main()
