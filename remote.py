import json
import asyncio
import aiohttp
import time
from method import status

class Subscriber:
    audio_endpoint = "/sony/audio"
    av_endpoint = "/sony/avContent"
    sys_endpoint = "/sony/system"

    header = {
        "Accept": "*/*",
        "Content-Type": "application/json"
    }

    DATA = {
        "method": "switchNotifications",
        "id": 2,
        "params": [{
            "enabled": [{"name": "notifyPlayingContentInfo", "version": "1.0"}]
        }],
        "version": "1.0"
    }

    def __init__(self, ip):
        self.URL = "ws://" + ip + self.av_endpoint
        self.isRunning = True
        self.ws = None
        

    async def sub(self):
        async with aiohttp.ClientSession() as session:
            session = aiohttp.ClientSession()
            try:
                self.ws = await session.ws_connect(self.URL)
                await self.ws.send_json(self.DATA)
                j = json.dumps(await self.ws.receive_json())
                print("successfully subscribed to input notification")
            except aiohttp.client_exceptions.ClientConnectorError:
                print("failed to subscribe to input notification, check ip settings")


    async def subscribe(self):
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(self.URL) as self.ws:
                await self.ws.send_json(self.DATA)

                j = json.dumps(await self.ws.receive_json())
                print(j)

    async def listen(self,queue):
        global status
        while self.isRunning:
            j = json.dumps(await self.ws.receive_json())
            j = (await self.ws.receive_json())
            # print("[listener] ",end='')
            # print(j)
            while not queue.qsize()==0:
                queue.get()
            j = j["params"][0]["source"]
            queue.put(j)
            

    def run(self,queue):
        self.event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.event_loop)
        # event_loop = asyncio.get_event_loop()
        self.event_loop.run_until_complete(self.sub())
        self.run_app = asyncio.ensure_future(self.listen(queue,))
        self.event_loop.run_forever()
        print('[listener] Stopped!')

    def stop(self):
        print('[listener] Requested stop!')
        # loop = asyncio.get_running_loop()
        # self.session.close()
        self.run_app.cancel()
        self.event_loop.call_soon_threadsafe(self.event_loop.stop)
        self.isRunning = False
        
        