def validator(argu):
    if not argu.symbol:
        raise ValueError("Symbol is required for this action.")
    if not argu.side:
        raise ValueError("Side is required for this action.")
    if argu.side not in ['BUY','SELL']:
        raise ValueError("Side must be either 'BUY' or 'SELL'.")
    if not argu.type:
        raise ValueError("Type is required for this action.")
    if argu.type not in ['LIMIT','MARKET']:
        raise ValueError("Type must be either 'LIMIT' or 'MARKET'.")
    if not argu.quantity:
        raise ValueError("Quantity is required for this action.")
    if argu.quantity <= 0:
        raise ValueError("Quantity must be greater than zero.")
    if argu.type == 'LIMIT':
        if argu.price is None:
            raise ValueError("Price is required for LIMIT orders.")
        if argu.price <= 0:
            raise ValueError("Price must be greater than zero for LIMIT orders.")
        
