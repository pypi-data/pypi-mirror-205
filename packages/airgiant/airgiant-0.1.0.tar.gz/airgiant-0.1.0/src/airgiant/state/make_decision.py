from behavior import *
from imports import *


async def control():
    async with websockets.connect(f"ws://10.20.24.10:5555/ws", ping_interval=5, ping_timeout=5) as ws:
        while True:
            a = input("input your cmd:")
            if a == "ask":
                my_list = []

                # 循环读取用户输入
                while True:
                    user_input = input("please input a number")

                    # 如果用户按下回车键，退出循环
                    if not user_input:
                        break

                    # 尝试将用户输入转换为整数
                    try:
                        user_input_int = float(user_input)
                    except ValueError:
                        print("not integer, please try again")
                        continue

                    # 将整数添加到列表中
                    my_list.append(user_input_int)
                await asyncio.gather(globals()[a](ws,my_list),recvpump(ws))
                
            else:
                    tasks = [
                    #asyncio.ensure_future(SkelCoord()),
                    #asyncio.ensure_future(test(ws)),
                    asyncio.ensure_future(globals()[a](ws)),
                    asyncio.ensure_future(recvpump(ws))
                    ]
                    await asyncio.wait(tasks)

async def auto():    # automatically doing the state changes. ideally we want the robot to be running this when presenting

    async with websockets.connect(f"ws://10.20.24.10:5555/ws", ping_interval=5, ping_timeout=5) as ws:
        tasks = [
        asyncio.ensure_future(simulate_signal()),
        asyncio.ensure_future(Decision(ws)),
        asyncio.ensure_future(recvpump(ws))
        ]
        await asyncio.wait(tasks)
