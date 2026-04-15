import argparse
from exec.orders import fetchOpen,place,positions,place_SLTP
from exec.validator import validator
from exec.logging import setup
logger = setup()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--action",required=True,choices=["place","orders","positions","SL/TP"])
    parser.add_argument("--symbol",type=str)
    parser.add_argument("--side",type=str,choices=["BUY","SELL"])
    parser.add_argument("--type",type=str,choices=["LIMIT","MARKET"])
    parser.add_argument("--quantity",type=float)
    parser.add_argument("--price",type=float)
    parser.add_argument("--sl_price",type=float)
    parser.add_argument("--tp_price",type=float)

    argu = parser.parse_args()

    try: 
        if argu.action == "place":
            validator(argu)

            logger.info(f"Placing order: {vars(argu)}")

            print("\nPlacing order...")
            order = place(argu.symbol,argu.side,argu.type,argu.quantity,argu.price)

            if isinstance(order, dict) and "code" in order:
                print(f"\nAPI Error: {order.get('msg')}")
                return

            print("\nOrder Summary: ")
            print(f"Order ID: {order.get('orderId')}")
            print(f"Status: {order.get('status')}")
            print(f"Filled Quantity: {order.get('executedQty')}")
            print(f"Price: {order.get('price')}")

            print("\nOrder placed successfully")
        
        elif argu.action == "orders":
            print("\nFetching open orders")

            logger.info("Fetching open orders")

            orders = fetchOpen(argu.symbol)
            print(f"\nOpen Orders for {argu.symbol if argu.symbol else 'all symbols'}:")

            if not orders:
                print("No open orders")
            else:
                for _ in orders:
                    if isinstance(_, dict):
                        print(f"Order ID: {order.get('orderId')}, Symbol: {order.get('symbol')}, Side: {order.get('side')}, Type: {order.get('type')}, Quantity: {order.get('origQty')}, Price: {order.get('price')}, Status: {order.get('status')}")   

        elif argu.action == "positions": 
            print("\nFetching positions...") 
            logger.info("Fetching positions") 
            positions_data = positions(argu.symbol) 
            
            if isinstance(positions_data, dict) and positions_data.get("code"): 
                raise Exception(positions_data) 
            
            print("\nCurrent Positions:") 
            if not positions_data: 
                print("No open positions") 
            else: 
                for pos in positions_data: 
                    print( f"Symbol: {pos.get('symbol')} | " f"Size: {pos.get('positionAmt')} | " f"Entry: {pos.get('entryPrice')} | " f"PnL: {pos.get('unRealizedProfit')}" )

        elif argu.action == "SL/TP":
            if not argu.symbol:
                raise ValueError("Symbol is required for SL/TP action.")
            
            if not argu.sl_price and not argu.tp_price:
                raise ValueError("At least one of SL price or TP price must be provided.")
            
            print("\nPlacing SL/TP orders...")

            resu = place_SLTP(argu.symbol,argu.sl_price,argu.tp_price)

            print("\nSLTP Response(s): ")
            print(resu)

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()