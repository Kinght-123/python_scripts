import asyncio
import websockets
import json
import random
from typing import Dict, Any


class OrderSystemServer:
    def __init__(self, host: str = "127.0.0.1", port: int = 8765):
        self.host = host
        self.port = port
        self.clients: Dict[websockets.WebSocketServerProtocol, str] = {}  # 客户端连接

    async def handle_client(self, websocket: websockets.WebSocketServerProtocol, path: str):
        """处理客户端连接"""
        # 注册客户端
        self.clients[websocket] = None
        print(f"客户端连接: {websocket.remote_address}")

        try:
            # 接收客户端消息（如果有）
            async for message in websocket:
                data = json.loads(message)
                print(f"收到消息: {data}")
        except websockets.exceptions.ConnectionClosed:
            print(f"客户端断开: {websocket.remote_address}")
        finally:
            # 移除客户端
            del self.clients[websocket]

    async def send_messages(self):
        """周期性发送消息"""
        while True:
            await asyncio.sleep(3)  # 每3秒发送一次消息

            # 随机选择一个消息类型
            message_type = random.choice(["new_order", "order_status", "promotion"])

            # 根据消息类型生成数据
            if message_type == "new_order":
                data = self.generate_order_data()
            elif message_type == "order_status":
                data = self.generate_order_status_data()
            else:
                data = self.generate_promotion_data()

            # 发送消息给所有连接的客户端
            for client in list(self.clients.keys()):
                if client.open:
                    await client.send(json.dumps(data))
                else:
                    # 移除已断开的客户端
                    del self.clients[client]

    def generate_order_data(self) -> Dict[str, Any]:
        """生成新订单数据"""
        return {
            "type": "new_order",
            "order_id": f"ORD-{random.randint(1000, 9999)}",
            "items": [
                {"id": random.randint(1, 100), "name": "Item 1", "quantity": random.randint(1, 10)},
                {"id": random.randint(1, 100), "name": "Item 2", "quantity": random.randint(1, 10)}
            ]
        }

    def generate_order_status_data(self) -> Dict[str, Any]:
        """生成订单状态更新数据"""
        statuses = ["pending", "processing", "shipped", "delivered"]
        return {
            "type": "order_status",
            "order_id": f"ORD-{random.randint(1000, 9999)}",
            "status": random.choice(statuses)
        }

    def generate_promotion_data(self) -> Dict[str, Any]:
        """生成促销信息数据"""
        return {
            "type": "promotion",
            "promotion_code": f"PROMO-{random.randint(1000, 9999)}",
            "description": "Special discount for loyal customers!"
        }

    async def start(self):
        """启动服务端"""
        async with websockets.serve(self.handle_client, self.host, self.port):
            print(f"服务端已启动: ws://{self.host}:{self.port}")
            await self.send_messages()


async def main():
    server = OrderSystemServer()
    await server.start()


if __name__ == "__main__":
    asyncio.run(main())
