# imports
import os
from dotenv import load_dotenv
from binance.client import Client
import time

load_dotenv()

api_key=os.getenv("API_KEY")
secret_key=os.getenv("SECRET_KEY")

def get_client():
    # connect app->binance api
    client=Client(api_key,secret_key)
    
    # sync
    server_time=client.get_server_time()
    sys_time=int(time.time()*1000)
    offset=server_time['serverTime']-sys_time
    client.timestamp_offset=offset
    
    # access testnet instead of real server
    client.FUTURES_URL="https://testnet.binancefuture.com/fapi"
    
    return client