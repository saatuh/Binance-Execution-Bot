# Binance Execution Bot 

I explored how binance client works through this python execution system project, which runs on the Binance Futures Testnet.

The main purpose of this algorithm is to allow users to place orders, view open orders, track positions, and simulate risk management features like Stop Loss and Take Profit.

I built this with a clean, modular structure and includes proper logging, validation, and error handling.


# Core Features:
1. Place MARKET and LIMIT orders
2. Support for both BUY and SELL side trades
3. Interaction on the Command Line Interface (CLI) with Argument Parsing
4. Features to fetch the OPEN orders and CURRENT positions.
5. Input Validation (through validator.py)
6. Advanced Logging (exec/exec.log)
7. Error handling for both input and API (various try/except/else loops in exec/orders.py, cli.py)

# Note: Limitations in Testnet:
Due to limitations in Binance Futures Testnet, the Stop Loss and Take Profit (MARKET) orders are not fully supported by currently used endpoints. 
As a workaround, I have used LIMIT order logic to partially simulate this.

# Project Map:
- execution-bot/
- │
- ├── exec/
- │   ├── orders.py           # API interaction layer (which is also the binance wrapper)
- │   ├── validator.py        # Input validation
- │   ├── logging.py          # setup for logging
- │   ├── exec.log            # Log file (auto-generated)
- │
- ├── cli.py                  # CLI entry point (where user types in command)
- ├── .env                    # API credentials
- ├── requirements.txt
- └── README.md

# Setup Instructions:
1. Clone the Repository:

```
git clone <repo link>
cd "execution-bot"
```

2. Install the Dependencies

```
pip install -r requirements.txt
```
3. Create the .env File

```
BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_api_secret
```

4. Setup the Binance Testnet
    a. Go to Binance Futures Testnet
    b. Generate API keys
    c. Ensure:
        i.  Futures enabled
        ii. No IP restrictions present (or configured correctly)

# How to use:
1. Placing MARKET order:
```
python cli.py --action place --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

2. Place LIMIT Order
```
python cli.py --action place --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 60000
```

3. Fetch Open Orders
```
python cli.py --action orders --symbol BTCUSDT
```

4. Fetch current Positions
```
python cli.py --action positions
```

5. Stop Loss / Take Profit (Conceptual)
```
python cli.py --action sl_tp --symbol BTCUSDT --stop_price 70000 --take_profit_price 80000
```

6. Logging

All API requests, responses, and errors are logged in: exec/exec.log


# Assumptions:
1. Only USDT-M Futures are supported
2. Only basic symbol validation (e.g., BTCUSDT)
3. SL/TP behavior is limited due to Testnet API constraints

# Dependencies (find here if not in requirements.txt)
1. requests
2. python-dotenv
3. python-binance

# Design Changes/Decisions:
1. I have used REST API over python-binance, as python-binance returned invalid API calls due to testnet inconsistencies. REST can be used even with live binance APIs.
