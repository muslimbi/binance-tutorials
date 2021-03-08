import asyncio
import websockets


async def candle_stick_data():
    url = "wss://stream.binance.com:9443/ws/" #steam address
    first_pair = 'bnbbtc@kline_1m' #first pair
    async with websockets.connect(url+first_pair) as sock:
        pairs = '{"method": "SUBSCRIBE", "params": ["xrpbtc@kline_1m","ethbtc@kline_1m" ],  "id": 1}' #other pairs

        await sock.send(pairs)
        print(f"> {pairs}")
        while True:
            resp = await sock.recv()
            print(f"< {resp}")

asyncio.get_event_loop().run_until_complete(candle_stick_data())