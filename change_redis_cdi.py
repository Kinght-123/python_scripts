import redis
import json
from typing import Dict, Any

# 测试redis
oy_fz_redis_settings = {
    'host': '10.188.73.101',
    'port': 6379,
    'password': 'Trunk@123',
    'decode_responses': True
}

# 生产redis
sc_redis_settings = {
    'host': '10.188.73.102',
    'port': 6379,
    'password': 'Trunk@123',
    # 'decode_responses': True
}

# 青岛redis
qd_redis_settings = {
    'host': '10.11.1.51',
    'port': 6378,
    'password': 'Trunk@123',
}


def export_redis_data(redis_client: Dict[str, Any], ship_id: str) -> None:
    # 连接Redis并获取数据
    with redis.Redis(**redis_client) as redis_client:
        # 获取所有匹配的键
        keys = redis_client.keys(f"vessel:{ship_id}:slot:*")

        for key in keys:
            redis_client.hset(key, 'occupied', 'false')
            redis_client.hdel(key, 'id')


if __name__ == "__main__":
    export_redis_data(oy_fz_redis_settings, 'WEIDLY2_003')
