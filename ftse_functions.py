#!/usr/bin/env python
# coding: utf-8

# # Functions

# We'll save our ftse dynamic feature functions in this file

# In[ ]:
import pandas as pd

def dataframe():
    data = pd.read_csv("ftse_static.csv", parse_dates=["time"])
    df1 = DataFrame(data)
   
    
    return df1



# Function to state the outcome of a trade based on target and drawdown levels specified
def outcome_gen(target, drawdown):
   
    df1 = pd.read_csv("ftse_static.csv", parse_dates=["time"])
    
    
    #We'll add a print report to show the progress we're making mid function execute
#     if x%200 == 0: 
#         print("processing row {}".format(x))
    
    
    #create variables for each of the rows we may need to iterate over
    high = df1["high"]
    low = df1["low"]
    close = df1["close"]
    open_ = df1["open"]
    signal = df1["signal"]
    direction = df1["direction"]
    
   
    #Set an empty list to hold each of our outcome strings
    outcome = []
    
    
    for x in list(range(0, df1.shape[0])):
        
        #set an empty list to store potential winning trades
        can_list = []
    
    #let's first check what the trade signal is and store it in our local long_short variable. 
        if signal[x] == "no_trade":
      
            outcome.append("no_trade")
        
        elif signal[x] == "unknown":
        
            outcome.append("no_trade")
            
        elif x > df1.shape[0]-2:
            
            outcome.append("unknown")
            
        else:
            for y in list(range(1,3)):
                
                if signal[x] == "trade" and direction[x] == "long":
                    
                    if low[x+y] < close[x]-drawdown: #We check out if the low of the next 30minute candle is lower than our signal candle

                        can_list.append('loss')#if so then add this to the temp_list
                    
                    elif high[x+y] - close[x] > target: #Determine whether we've hit the target

                        can_list.append('win')
            
                    elif close[x+y] < close[x]:
                
                        can_list.append('loss')
                    
                    else:

                        can_list.append('no_score')
                
                elif signal[x] == "trade" and direction[x] == "short":
                    
                    if high[x+y] > close[x]+drawdown: #We check if the high of the next 30minute candle is higher than our signal candle high

                        can_list.append('loss') #add sub_outcome 'loss' to our value_list container. 
                    
                    elif close[x] - low[x+y] > target: #Determines whether we've hit the target

                        can_list.append('win')
                
                    elif close[x] < close[x+y]: #Determines whether a reversal signal has been printed
                
                        can_list.append('loss')
                
                    else:

                        can_list.append('no_score') #applicable for a minor retrace or small winning position < 10
        
            result = 'no_score'
            for i in can_list:
                if i == "loss":
                    result = i
                    break
                elif i == "win":
                    result = i
                    break
                else:
                    continue
            outcome.append(result)
        
        
        
    
    
           
    #print(x, can_list)
    
    df2 = pd.DataFrame(outcome, columns=["outcome"])
    
    
    return df2




#Funtion to state the profit of the trade based on the outcome and the target, drawdown specified. 
def profit_gen(target, drawdown):
    """
    In this function we'll store all the profits in a list and then join them to the master dataframe
    """
    #store the static dataframe in a variable our function can use
    df1 = pd.read_csv("ftse_static.csv", parse_dates=["time"]).join(outcome_gen(target, drawdown))
    
    #create a list that holds only the first 0 value for the first row of our profit
    profit = []
    
    #create variables for each of the rows we may need to iterate over
    high = df1["high"]
    low = df1["low"]
    close = df1["close"]
    open_ = df1["open"]
    signal = df1["signal"]
    direction = df1["direction"]
    outcome = df1["outcome"]
    
    
    
    for x in list(range(0, df1.shape[0])):
        
        can_list = [target]
        
        if x == 0:
            profit.append(0)
        
        elif x > df1.shape[0]-5:
            profit.append(0)
            
        elif signal[x] == "no_trade":
            profit.append(0)
            
        elif direction[x] == "neutral":
            profit.append(0)
            
        elif direction[x] == "short" and outcome[x] == "loss":
            
            #drawdown loss
            if high[x+1] > close[x]+drawdown:
                profit.append(-drawdown)
                
            #reversal loss
            elif high[x+1] < (close[x]+drawdown) and direction[x] != direction[x-1]:
                profit.append(close[x-1] - close[x])
                
            
        elif direction[x] == "long" and outcome[x] == "loss":
            
            #drawdown loss
            if low[x+1] < close[x]-drawdown:
                profit.append(-drawdown)
                
            
            #reversal loss
            elif low[x+1] > (close[x]-drawdown) and direction[x] != direction[x-1]:
                profit.append(close[x+1] - close[x])
        
#         else:
#             profit.append((x, "not loss"))
        
        
        else: 
            for y in list(range(1, 7)):
            
            
            
                if direction[x] == direction[x+y]:
            
                    if outcome[x] == "win" and direction[x] == "short":
                    
                        can_list.append(abs(close[x] - low[x+y]))
                
                    elif outcome[x] == "win" and direction[x] == "long":
                    
                        can_list.append(abs(high[x+y] - close[x]))
            
                elif direction[x] != direction[x+y]:
                
                    break
                
            #print(x, can_list)
        
            profit.append(max(can_list))
    

    
    print(f'the length of profit list is {len(profit)}')
    
    df3 = pd.DataFrame(profit, columns=["profit"])
    
#     df4 = pd.concat([df, df3], ignore_index=True)
    
    return df3


###### BUILD A DRAWDOWN GENERATOR TO SHOW POTENTIAL DRWADOWN LEVELS IN A WINNING TRADE ######
def drawdown_gen(target, drawdown):
    # Give function access to the global variable, x.

    df1 = pd.read_csv("ftse_static.csv",
                      parse_dates=["time"]).join(outcome_gen(target, drawdown)).join(profit_gen(target, drawdown))

    # Create our iterable variables
    high = df1['high']
    low = df1['low']
    close = df1['close']
    open_ = df1['open']
    outcome = df1['outcome']
    direction = df1['direction']
    signal = df1['signal']

    # set a list that will hold all our drawdown values against each data point.
    max_drawdown = []

    for x in list(range(0, df1.shape[0])):

        # set a list that will hold our maximum drawdown
        can_list = [0]

        if x == 0:
            max_drawdown.append(0)

        elif x > df1.shape[0] - 5:
            max_drawdown.append(0)

        elif signal[x] == "no_trade":
            max_drawdown.append(0)

        elif direction[x] == "neutral":
            max_drawdown.append(0)

        elif outcome[x] == "loss":
            max_drawdown.append(0)

        else:
            for y in list(range(1, 7)):

                if direction[x] == direction[x + y]:

                    if outcome[x] == "win" and direction[x] == "long":

                        can_list.append(close[x] - low[x + y])

                    elif outcome[x] == "win" and direction[x] == "short":

                        can_list.append(high[x + y] - close[x])

                elif direction[x] != direction[x + y]:

                    break

            max_drawdown.append(max(can_list))

    df_draw = pd.DataFrame(max_drawdown, columns=["max_drawdown"])

    return df_draw


