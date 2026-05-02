import argparse #to read terminal arguments
from bot.validators import validate_side,validate_order_type,validate_quantity,validate_price,validate_symbol
from bot.order import place_market_order,place_limit_order
from datetime import datetime
from bot.client import get_client
from bot.logging import logger 

# parse object which converts it into a valid response
parser=argparse.ArgumentParser()

# adding arguments
parser.add_argument("--symbol",required=True)
parser.add_argument("--side",required=True)
parser.add_argument("--type",required=True)
parser.add_argument("--quantity",required=True)
parser.add_argument("--price")

args=parser.parse_args()

# print(args.symbol)

symbol=args.symbol
side=args.side
order_type=args.type
quantity=args.quantity
price=args.price

validated_symbol=validate_symbol(symbol)
validated_side=validate_side(side)
validated_order_type=validate_order_type(order_type)
validated_quantity=validate_quantity(quantity)


if validated_order_type=="LIMIT":
    if price is None:
        raise ValueError("Price should be provided with Limit Order")
    validated_price=validate_price(price)
    logger.info(
        f"CLI LIMIT ORDER REQUEST | "
        f"symbol={validated_symbol} | "
        f"side={validated_side} | "
        f"quantity={validated_quantity} | "
        f"price={validated_price}"
    )
    response=place_limit_order(symbol=validated_symbol,side=validated_side,quantity=validated_quantity,price=validated_price)
    if not response['success']:
        logger.error(
            f"LIMIT ORDER FAILED | "
            f"symbol={validated_symbol} | "
            f"error={response['error']}"
        )
        raise ValueError(response['error'])
else:
    logger.info(
        f"CLI MARKET ORDER REQUEST | "
        f"symbol={validated_symbol} | "
        f"side={validated_side} | "
        f"quantity={validated_quantity}"
    )
    response=place_market_order(symbol=validated_symbol,side=validated_side,quantity=validated_quantity)
    if not response['success']:
        logger.error(
            f"MARKET ORDER FAILED | "
            f"symbol={validated_symbol} | "
            f"error={response['error']}"
        ) 
        raise ValueError(response['error'])
   
    
client=get_client()

# current price
ticker=client.futures_symbol_ticker(symbol=validated_symbol)
current_price=ticker['price']
    
# order request
print("========== ORDER REQUEST ==========")
print(f"Symbol        : {validated_symbol}")
print(f"Side          : {validated_side}")
print(f"Order Type    : {validated_order_type}")
print(f"Quantity      : {validated_quantity}")
print(f"Current Price : {current_price}")
if validated_order_type == "LIMIT":
    print(f"Price         : {validated_price}")
else:
    print("Price         : MARKET PRICE")
print("===================================")


# order response
print("==============ORDER===============")
print(f"Order ID          : {response['orderId']}")

status="Order Processed"
if response['status']=="FILLED":
    status="Order executed successfully"
elif response['status']=="NEW":
    status="Order placed and waiting for execution"
elif response['status']=="PARTIALLY_FILLED":
    status="Order partially executed"
    
print(f"Status            : {status}")
print(f"Executed Quantity : {response['executedQty']}")
if response['avgPrice']!="0.00":
    print(f"Average Price     : {response['avgPrice']}")
else:
    print(f"Average Price     : Pending Execution")
print("==================================")


