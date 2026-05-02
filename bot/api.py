from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field,field_validator
from bot.order import place_market_order,place_limit_order
from bot.client import get_client
from bot.logging import logger

app=FastAPI()

# Base Model
class LimitOrderRequest(BaseModel):
    symbol:str=Field(...,description="Enter Symbol you want to trade in")
    side:str=Field(...,description="Order: Buy/Sell")
    quantity:float=Field(...,gt=0,description="Enter quantity you want to buy")
    price:float=Field(...,gt=0,description="Enter price for limit order")
    
    @field_validator("side")
    @classmethod
    def validate_side(cls,side):
        side=side.upper()
        if side not in ["BUY","SELL"]:
            raise ValueError("Invalid input for side")
        
        return side 
    
    @field_validator("symbol")
    @classmethod
    def validate_symbol(cls,symbol):
        symbol=symbol.upper()
        
        return symbol
    
class MarketOrderRequest(BaseModel):
    symbol:str=Field(...,description="Enter Symbol you want to trade in")
    side:str=Field(...,description="Order: Buy/Sell")
    quantity:float=Field(...,gt=0,description="Enter quantity you want to buy")
    
    @field_validator("side")
    @classmethod
    def validate_side(cls,side):
        side=side.upper()
        if side not in ["BUY","SELL"]:
            raise ValueError("Invalid input for side")
        
        return side  
    @field_validator("symbol")
    @classmethod
    def validate_symbol(cls,symbol):
        symbol=symbol.upper()
        
        return symbol
    
# endpoints
@app.post("/order/market")
def create_market_order(input_request:MarketOrderRequest):
    
    logger.info(
        f"MARKET ORDER REQUEST | "
        f"symbol={input_request.symbol} | "
        f"side={input_request.side} | "
        f"quantity={input_request.quantity}"
    )
    
    response=place_market_order(symbol=input_request.symbol,side=input_request.side,quantity=input_request.quantity)
    
    if not response['success']:
        logger.error(
            f"MARKET ORDER FAILED | "
            f"symbol={input_request.symbol} | "
            f"error={response['error']}"
        )
        raise HTTPException(status_code=400,detail=response['error'])

    response_data=response['data']
    
    status="Order Processed"
    if response_data['status']=="FILLED":
        status="Order executed successfully"
    elif response_data['status']=="NEW":
        status="Order placed and waiting for execution"
    elif response_data['status']=="PARTIALLY_FILLED":
        status="Order partially executed"
        
        
    client=get_client()
    # current price
    ticker=client.futures_symbol_ticker(symbol=input_request.symbol)
    current_price=ticker['price']
    
    return {
        "success":True,
        "order_id":response_data['orderId'],
        "symbol":input_request.symbol,
        "side":input_request.side,
        "order_type":"Market",
        "status":status,
        "executed_quantity":response_data['executedQty'],
        "average_price":"Pending Execution" if response_data['avgPrice']=="0.00" else response_data['avgPrice'],
        "current_price":current_price
    }

@app.post("/order/limit")
def create_limit_order(input_request:LimitOrderRequest):
    logger.info(
        f"LIMIT ORDER REQUEST | "
        f"symbol={input_request.symbol} | "
        f"side={input_request.side} | "
        f"quantity={input_request.quantity} | "
        f"price={input_request.price}"
    )
    
    response=place_limit_order(symbol=input_request.symbol,side=input_request.side,quantity=input_request.quantity,price=input_request.price)
    
    if not response['success']:
        logger.error(
            f"LIMIT ORDER FAILED | "
            f"symbol={input_request.symbol} | "
            f"error={response['error']}"
        )
        raise HTTPException(status_code=400,detail=response['error'])

    response_data=response['data']
    
    status="Order Processed"
    if response_data['status']=="FILLED":
        status="Order executed successfully"
    elif response_data['status']=="NEW":
        status="Order placed and waiting for execution"
    elif response_data['status']=="PARTIALLY_FILLED":
        status="Order partially executed"
        
        
    client=get_client()
    # current price
    ticker=client.futures_symbol_ticker(symbol=input_request.symbol)
    current_price=ticker['price']
    
    return {
        "success":True,
        "order_id":response_data['orderId'],
        "symbol":input_request.symbol,
        "side":input_request.side,
        "order_type":"Limit",
        "status":status,
        "executed_quantity":response_data['executedQty'],
        "average_price":"Pending Execution" if float(response_data['avgPrice'])==0 else response_data['avgPrice'],
        "current_price":current_price
    }
