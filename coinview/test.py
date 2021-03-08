from binance.client import Client
from binance.enums import KLINE_INTERVAL_1MINUTE
from binance.websockets import BinanceSocketManager
import time


client = Client('gwunGspa1m5ci5C5LtzSX3sTKbttsx5Cj6vksdwkDgknf5Aa8DLvpN9IUhLz6JqB', '49ovX7oeOwc2kHJgbm3yk5UDmT1NNBNZbwNstjj7y9d4wNHETdWjtX1NNsNODhKQ', {"timeout": 10})
bm = BinanceSocketManager(client)
started = False

def process_message(msg):
    # Close connections after first message
    global bm
    print(msg)
    print('Stopping WebSocket for %s..' %  msg['s'])
    bm.stop_socket('%s@kline_1m' % msg['s'].lower())


while True:
    # Create ETHBTC connection if not connected already.
    if not 'ethbtc@kline_1m' in bm._conns:
        print('Creating WebSocket for ETHBTC..')
        conn = bm.start_kline_socket('ETHBTC', process_message, interval=KLINE_INTERVAL_1MINUTE)

    # Create ADABTC connection if not connected already.
    if not 'adabtc@kline_1m' in bm._conns:
        print('Creating WebSocket for ADABTC..')
        conn = bm.start_kline_socket('ADABTC', process_message, interval=KLINE_INTERVAL_1MINUTE)

    # Binance WebSocket Manager will start only once
    if not started:
        started = True
        bm.start()

    time.sleep(5)
