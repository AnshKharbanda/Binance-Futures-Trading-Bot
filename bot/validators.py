def validate_symbol(symbol):
    if not symbol:
        raise ValueError("Some value should be assigned to symbol")
    
    return symbol.upper()

def validate_side(side):
    side=side.upper()
    
    if side not in ["BUY","SELL"]:
        raise ValueError("Wrong input for side direction")
    
    return side

def validate_order_type(order_type):
    order_type=order_type.upper()
    
    if order_type not in ["MARKET","LIMIT"]:
        raise ValueError("Wrong order type")
    
    return order_type

def validate_quantity(quantity):
    try:
        quantity=float(quantity)
    except ValueError:
        raise ValueError("Enter a numeric value")
    
    if quantity<=0:
        raise ValueError("Quantity should be greater than zero")
    
    return quantity

def validate_price(price):
    try:
        price=float(price)
    except ValueError:
        raise ValueError("Enter numeric value")
    
    if price<=0:
        raise ValueError("Enter Price greater than zero")
    
    return price

        