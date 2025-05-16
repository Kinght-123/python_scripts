import asyncio
import websockets
import json
from typing import Callable, Dict, Any


class OrderSystemClient:
    def __init__(self):
        self.message_handlers: Dict[str, Callable] = {}  # 消息类型到回调函数的映射

    def on_message(self, message_type: str):
        """装饰器：注册消息处理函数"""

        def decorator(func: Callable):
            self.message_handlers[message_type] = func
            return func

        return decorator

    async def handle_messages(self, websocket):
        async for message in websocket:
            data = json.loads(message)
            message_type = data.get("type")
            if message_type in self.message_handlers:
                await self.message_handlers[message_type](data)
            else:
                print(f"未知消息类型: {message_type}")

    async def connect(self, uri: str):
        async with websockets.connect(uri) as websocket:
            await self.handle_messages(websocket)


# 使用回调机制处理消息
client = OrderSystemClient()


@client.on_message("new_order")
async def handle_new_order(data):
    print(f"新订单: {data['order_id']} - {data['items']}")


@client.on_message("order_status")
async def handle_order_status(data):
    print(f"订单状态更新: {data['order_id']} - {data['status']}")


@client.on_message("promotion")
async def handle_promotion(data):
    print(f"促销信息: {data['promotion_code']} - {data['description']}")


async def main():
    await client.connect("ws://127.0.0.1:8765")


if __name__ == "__main__":
    asyncio.run(main())
