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
            position_dat = positions()
            logger.info("Fetching positions")
            print("\nCurrent Positions:")
            if isinstance(position_dat, dict) and "code" in position_dat:
                print(f"\nAPI Error: {position_dat.get('msg')}")
                return
            set_active = False
            for position in position_dat:
                size = float(position.get('positionAmt', 0))

                if size != 0:
                    print(f"Symbol: {position.get('symbol')}, Position Size: {position.get('positionAmt')}, Entry Price: {position.get('entryPrice')}, Unrealized PnL: {position.get('unRealizedProfit')}")
                    set_active = True

            if not set_active:
                    print("No open positions")

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