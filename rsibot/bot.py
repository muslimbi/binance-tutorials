# import websocket, json, pprint, talib, numpy
import websocket, json, pprint, numpy
import config
from binance.client import Client
from binance.enums import *
from datetime import datetime

SOCKET = "wss://stream.binance.com:9443/ws/xvsusdt@kline_1d"

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'XVSUSDT'
TRADE_QUANTITY = 0.05

closes = []
in_position = False

client = Client(config.API_KEY, config.API_SECRET, tld='us')

def order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
    try:
        print("sending order")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True

    
def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

def on_message(ws, message):
    global closes, in_position
    
    print('received message')
    json_message = json.loads(message)
    pprint.pprint(json_message)


    print("--------------------------------------------")
    radio = json_message['k']
    
    radioc = float(radio['c'])
    radioo = float(radio['o'])
    radioh = float(radio['h'])
    radiol = float(radio['l'])
    
    print("Current Close Price is {}".format(radioc))
    print("Current Low Price is {}".format(radiol))
    print("--------------------------------------------")
    print("Current Open Price is {}".format(radioo))
    print("Current High Price is {}".format(radioh))
    
    print("--------------------------------------------")
    timestampt = int(radio['t'])/1000
    date_timet = datetime.fromtimestamp(timestampt)

    timestamptt = int(radio['T'])/1000
    date_timett = datetime.fromtimestamp(timestamptt)

    print ('Opening date/time: {}'.format(date_timet))
    print ('Closing date/time: {}'.format(date_timett))
    print("--------------------------------------------")

    ratiok = ( float(radio['c']) - float(radio['l']) ) / ( float(radio['h']) - float(radio['l']) ) * 100    
    
    if ratiok < 10:
        print("Current Ratio from Low is -------------------------------------------------------- {}".format(ratiok))
    else:
        print("Current Ratio from Low is {}".format(ratiok))
         
    ratiok = ( float(radio['h']) - float(radio['l']) ) / float(radio['h']) * 100    
    print("Maximum Loss Ratio from High is {}".format(ratiok))
    
    ratiok = ( float(radio['h']) - float(radio['l']) ) / float(radio['l']) * 100    
    print("Maximum Profit Ratio from Low is {}".format(ratiok))
    
    
    candle = json_message['k']

    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        print("candle closed at {}".format(close))
        closes.append(float(close))
        print("closes")
        print(closes)

        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print("all rsis calculated so far")
            print(rsi)
            last_rsi = rsi[-1]
            print("the current rsi is {}".format(last_rsi))

            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print("Overbought! Sell! Sell! Sell!")
                    # put binance sell logic here
                    order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeeded:
                        in_position = False
                else:
                    print("It is overbought, but we don't own any. Nothing to do.")
            
            if last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("It is oversold, but you already own it, nothing to do.")
                else:
                    print("Oversold! Buy! Buy! Buy!")
                    # put binance buy order logic here
                    order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeeded:
                        in_position = True

                
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()