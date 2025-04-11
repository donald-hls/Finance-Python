import pandas as pd 
import numpy as np 
import yfinance as yf
import datetime, time 

# This is a project that explores some of the key themes in eFX trading. 
# Some of the rules are outlined in the Framework file, please check it out. :) 


# Some Conventions:
pip = 0.0001

pair = "CAD=X" # - Equivalent to USD/CAD (used for buying USD)

num_of_pips = 4

def data_func(curr_pair):
    """
    Returns a list of information, the function takes a currency pair, that is curr_pair, 
    and writes to a text file (some_file) of the historical transaction. 
    
    data: Str Str -> listof(Int Str)
    """
    ticker = yf.Ticker(curr_pair)
    # Retrieving real-life bid and ask 
    bid = np.round(ticker.info["bid"], 5)
    ask = np.round(ticker.info["ask"], 5)
    spread = np.round(ask - bid, 5)
    transaction_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    info_list = [transaction_time, bid, ask, spread]
    return info_list

def trade_check(order_size):
    """
    Returns True, False, Int, but prints out a message to the screen, 
    showing the status if a trade is made. It returns 2 if algo orders are used 
    to handle transactions over the volume. The function consumes 
    a list containing price info and the size of the order.
    
    Effects: 
        - Prints a message onto the screen displaying trade status. 
    
    trade_check: Int -> Anyof (Bool, Int)
    """
    info = data_func(pair)
    spread = info[3]
    rolling_volume = 50000000 # rolling average volume
    # checking the order size & conditions. 
    if order_size > 50000000:
        print("Transfer to the Voice Sales")
        return False
    elif order_size> rolling_volume * 0.1: 
        print("Order exceeds 10% of rolling avg volume—potential slippage.")
        return False 
    elif order_size > 500000: # setting as a threshold limit. 
        return 2
    # checking conditions to buy 
    elif spread >= pip * num_of_pips: 
        print("The Bid-Ask Spread is too wide, no trade executed")
        return False
    else: # when a trade does occur
        return True
      
        
# Buying or Selling Market Orders: 
def market_buy(order_size):
    """
    Returns the amount of money spent after the transaction was executed. 
    
    market_buy: Float -> Float
    """
    if trade_check(order_size) == True: 
        info = data_func(pair)
        ask_price = info[2]
        cost_of_trade = ask_price * order_size
        print(f"Trade Executed Successfully:")
        print(" - Bought: {} USD".format(order_size))
        print(" - Paid: {} CAD at rate {}".format(cost_of_trade, ask_price))
        return cost_of_trade

def market_sell(position_size):
    """
    Returns the amount of money sold after the transaction was executed. 
    
    market_sell: Float -> Float
    """
    data = data_func(pair)
    bid = data[1]
    proceeds = position_size * bid
    return proceeds
  
# Algo-Orders
def algo_orders(order_size):
    """
    Effects: 
        - Prints a message onto the screen displaying trade status. 
    In the case of large order size, the function breaks the large orders into
    smaller algo orders to avoid triggering a slippage in the market. 
    
    algo_orders: Float -> Float 
    """
    if trade_check(order_size) == 2: 
        small_algo_order = 100000
        number_orders = order_size // small_algo_order
        remaining = order_size % small_algo_order
        print("This order is split into {} of USD each.".format(number_orders))
        total_cost = 0
        for i in range(0,number_orders): 
            info = data_func(pair)
            ask = info[2]
            spread = info[3]
            if spread < pip * num_of_pips: 
                cost_trade = ask * small_algo_order
                total_cost += cost_trade
                print(f"Trade Executed Successfully:")
                print("Algo Order {} - Bought: {} USD".format(i+1, small_algo_order))
                print(" - Paid: {} CAD at rate {}".format(cost_trade, ask))
            else: 
                print("Bid-Ask Spread too wide, delaying the trade...")
            time.sleep(1.5)
        # for the remaining amount: 
        if remaining > 0:
            info = data_func(pair)
            ask = info[2]
            spread = info[3]
            if spread < pip * num_of_pips: 
                cost_trade = ask * small_algo_order
                total_cost += cost_trade
                print(f"Trade Executed Successfully:")
                print("Algo Order {} - Bought: {} USD".format(i+1, small_algo_order))
                print(" - Paid: {} CAD at rate {}".format(cost_trade, ask))
            else: 
                print("Bid-Ask Spread too wide, delaying the trade...")
            time.sleep(1.5)
    
        print("All amounts processed... ")
        print("Total Cost in CAD: {}".format(total_cost))
    
        return total_cost
   
# Limit Orders     
def limit_order_buy(order_size, max_willing_price, max_waiting_time):
    """
    Returns None, the function executes an FX limit order to buy base at 
    or below a specified price (max_willing_price) for order_size amount.
    
    Effects: 
        - Prints a message onto the screen displaying trade status. 
    
    limit_order_buy: Int, Float, Int -> None
    
    """
    print("Placing limit order for {} USD at or below {} CAD/USD for {} seconds".
          format(order_size, max_willing_price, max_waiting_time))

    start_time = time.time()
    while time.time() - start_time < max_waiting_time:
        info = data_func(pair)
        ask  = info[2]
        spread = info[3]
        total_cost = 0
        executed = False 
        if ask <= max_willing_price and spread < pip * num_of_pips:
            # A limit order trade occurs
            total_cost = ask * order_size
            print("Trade Executed Successfully:")
            print(f"Bought: {order_size} USD at {ask} CAD/USD")
            print("Total Cost: {} CAD".format(total_cost))
            executed = True
            break
        else: 
            print("Delaying Transaction")
        time.sleep(1.5)
    if executed == False: 
        print("Limit Order expired -- No Execution")
        
def PnL_calculation(position_size):
    """
    The function calculates the total P&L of the transaction by converting value 
    of your currency position changes over time. To calculate profit, the function captures
    the profit of selling owned currency to base currency. If no trade executed, the pnl is 0. 
    
    PnL_calculation: Float Float Float -> Float
    """
    status = trade_check(position_size)
    if  status == True:
        total_cost = market_buy(position_size)
        time.sleep(5) # This only serves as an indication to wait some time 
        proceeds = market_sell(position_size)
        pnl = np.round(proceeds - total_cost, 3)
        print("Realized PnL: {}".format(pnl))
        return pnl
    elif status == 2:
        print("Order size too large, consider break into algo orders.")
        total_cost = algo_orders(position_size)
        time.sleep(5) # This only serves as an indication to wait some time 
        proceeds = market_sell(position_size)
        pnl = np.round(proceeds - total_cost, 3)
        print("Realized PnL: {}".format(pnl))
        return pnl
    else: 
        return 0
    
            
if __name__ == "__main__":
    pass
    # Working Functions :) 
    # trade_check(1000)
    # PnL_calculation(1000000)
    # limit_order_buy(1000, 1.4319, 100)


        

           