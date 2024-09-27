import pandas as pd
import numpy as np
import yfinance as yf
from matplotlib import pyplot as plt

#read in limit order book data (hint: pd.read_csv('FILENAME'))
limit_book = pd.read_csv("BTCUSD_2019_09_01.csv")
limit_book.tail() 
sell = limit_book[["s_price", "s_amount"]]
buy = limit_book[["b_price", "b_amount"]]

def plotting_buy_sell():
    '''
    This function would plot the buy and 
    sell prices in the limit book on a graph 
    '''
    plt.plot(sell.s_price, color='b', label='Sell orders')
    plt.plot(buy.b_price, color='r', label='buy orders')
    plt.legend(loc='best')
    plt.title('Limit Order Book Prices')
    plt.xlabel('Order Number')
    plt.ylabel('Value (USD)')
    plt.show()
    
# to plot the graph
# plotting_buy_sell()

def buy_order_market(order_size, out_file):
    '''
    Writes to a file and display any related information
    on this buy market order transaction, by consuming the 
    order size (the number of shares want to buy)
    
    buy_order_market: anyof(Int Float) anyof(Int Float) File -> None
    
    '''
    shares=0
    count=0
    cost=0
    diff=0
    while shares < order_size:
        shares= shares + sell.s_amount[count] 
        if shares > order_size:
            diff = shares - order_size 
            shares = order_size
        cost+=sell.s_price[count]*(sell.s_amount[count] - diff)
        count+=1
        
    info = open(out_file, "w")
    info.write("total shares {}".format(shares) + "\n")
    info.write("Total Cost: $ {}".format(str(np.round(cost, decimals=2))) + "\n")
    info.write("Average Price Paid: ${}".format(str(np.round(cost/order_size, decimals=2)))+ "\n")
    info.write("Last Transaction Price BOUGHT: ${}".format(np.round(sell.s_price[count-1], decimals=2))+ "\n")
    info.write("Price Movement: {}".format(sell.s_price[count - 1] - sell.s_price[0])+ "\n")
    info.close()
    
# write to file about details of this transaction
# buy_order_market(500, "buy_order_info.txt")

def sell_order_market(order_size, outfile):
    '''
    Writes to a file and display any related information
    on this sell market order transaction, by consuming the 
    order size (the number of shares want to sell)
    
    sell_order_market: anyof(Int Float) anyof(Int Float) File -> None
    
    '''
    shares=0
    count=0
    proceeds =0
    diff=0
    while shares < order_size:
        shares= shares + buy.b_amount[count] 
        if shares > order_size:
            diff = shares - order_size
            shares = order_size
        proceeds+=buy.b_price[count]*(buy.b_amount[count] - diff)
        count+=1
        
    info = open(outfile, "w")
    info.write("total shares {}".format(shares) + "\n")
    info.write("Total Proceeds: $ {}".format(str(np.round(proceeds, decimals = 2))) + "\n")
    info.write("Average Price SOLD: ${}".format(str(np.round(proceeds/order_size, decimals=2)))+ "\n")
    info.write("Last Transaction Price SOLD: ${}".format(np.round(buy.b_price[count-1], decimals=2))+ "\n")
    info.write("Price Movement: {}".format(buy.b_price[count - 1] - buy.b_price[0])+ "\n")
    info.close()
     
# write to file about details of this transaction
# sell_order_market(300, "sell_order_info.txt")


def limit_order_buy(order_size, price_willing, outfile):
    '''
    Writes to a file and display any related information
    on this limit order buy transaction by consuming the 
    order size and the max price willing to buy
    
    limit_order_buy: anyof(Int Float) anyof(Int Float) File -> None
    
    '''
    shares_bought = 0
    count = 0
    cost = 0
    diff = 0
    while shares_bought < order_size and sell.s_price[count] <= price_willing:
        shares_bought = shares_bought + sell.s_amount[count]
        if shares_bought > order_size:
            diff = shares_bought - order_size
            shares_bought = order_size 
        cost += sell.s_price[count] * (sell.s_amount[count] - diff)
        count +=1
    
    f = open(outfile, "w")
    f.write("Total shares bought is {}".format(np.round(shares_bought, decimals=2)) + "\n")
    f.write("Total Cost is {}".format(np.round(cost, decimals = 2)) + "\n")
    try:
        average_price = np.round(cost / shares_bought, decimals = 2)
        price_movement = np.around(sell.s_price[count -1] - sell.s_price[0])
        f.write("Average Price bought is {}".format(average_price) + "\n")
        f.write("Price Movement is {}".format(price_movement) + "\n")
    except:
        f.write("No average Price bought is available")
    f.close()
    
limit_order_buy(500,9800, "limit_order_buy.txt")


def limit_order_sell(order_size, price_willing, outfile):
    '''
    Writes to a file and display any related information
    on this sell limit order transaction, by consuming the 
    order size (the number of shares want to buy) and the 
    lowest price willing to sell. 
    
    limit_order_sell: anyof(Int Float) anyof(Int Float) File -> None
    '''
    shares_sold = 0
    proceeds = 0
    diff = 0
    count = 0
    while shares_sold < order_size and buy.b_price[count] >= price_willing:
        shares_sold = shares_sold + buy.b_amount[count]
        if shares_sold > order_size:
            diff = shares_sold - order_size
            shares_sold = order_size 
        proceeds += buy.b_price[count] * (buy.b_amount[count] - diff)
        count += 1
    f = open(outfile, "w")
    f.write("Total shares sold is {}".format(np.round(shares_sold, decimals=2)) + "\n")
    f.write("Total Proceeds is {}".format(np.round(proceeds, decimals = 2)) + "\n")
    try:
        average_price = np.round(proceeds/ shares_sold, decimals = 2)
        price_movement = np.around(buy.b_price[count -1] - buy.b_price[0])
        f.write("Average Price sold is {}".format(average_price) + "\n")
        f.write("Price Movement is {}".format(price_movement) + "\n")
    except:
        f.write("No average Price sold is available")
    f.close()
    
    
# limit_order_sell(50,9400, "limit_order_sell.txt")