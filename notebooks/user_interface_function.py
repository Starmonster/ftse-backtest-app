#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import pandas as pd

from ftse_functions import *

#CREATE A USER INTERFACE ASKING FOR USER TARGET PRICE AND STOP LOSS, WHICH WILL RETURN WIN AND LOSS METRICS
def user_interface():
    """
    A function to create a user interface
    
    """
    
    dfx = pd.read_csv("../data/ftse_static.csv", parse_dates=["time"])
   
    
    
    #A user input to confirm if a trade signal has been printed
    signal = input("\nHas a double tap signal been recorded on the 4hr timeframe? y/n: \n")
    
    #Conditional statements fed by the signal input
    if signal == 'y':
        print("\nThat's great! Let's see if you can make a profitable trade!!\n")
        direction = input("What is the trade direction, long or short?: ")
        
        if direction.lower() == "long" or direction.lower() == "short":
            None
        else:
            print("\nPlease type long or short depending on the trade signal")
            return user_interface()
       
        
        #Ask the user what there proposed trade target value is?
        target = input("\nWhat is your target value in points?: ")
        try: 
            target = int(target)
        except ValueError:
            print("I need a number greater than 0")
            return user_interface()
        
        
        #Ask the user what their required max drawdown (stop-loss) is
        drawdown = input("\nWhat is your maximum drawdown value?: ")
        try: 
            drawdown = int(drawdown)
        except ValueError:
            print("I need a number greater than 0")
            return user_interface()
        
        #call the outcome function on the target and drawdown recieved, add the values to master dataframe
        
        temp = dfx.join(outcome_gen(target, drawdown))
        
        
        
        #call the net profit function on the target, drawdown and outcome, add values to master dataframe
        
        temp = temp.join(profit_gen(target, drawdown))
        
       
        
#         new_dataset(df1)
        
        
        
        
        #Ask the user what trade size they would like?
        size = input("\nWhat is your trade size: ")
        try: 
            size = int(size)
        except ValueError:
            print("I need a number greater than 0")
            return user_interface()
        
        
        #Filter for wins and losses using the inputted values
        win_filter = temp[temp.outcome=="win"].profit
        loss_filter = temp[temp.outcome=="loss"].profit
        
        
        #store a win average
        win_ave = win_filter.mean()
        
        #store a loss average for losses below the drawdown
        loss_ave = loss_filter.mean()
        
        #store a win count
        win_count = win_filter.shape[0]
        
        #store a loss count for losses below the drawdown
        loss_count = loss_filter.shape[0]
        
        #store a total number of trades
        trade_count = win_count + loss_count
        
        #Calculate and store the average returns based on the user requirements
        ave_return = (((win_ave*win_count) + (loss_ave*loss_count)) / trade_count)*size
        
        
        #Create the main return output for user consideration
        return f"Across {trade_count} total trades there are {win_count} winning trades at an average of {round(win_ave)} points per winning trade. There are {loss_count} losing trades at an average loss of {round(loss_ave)} points. For a trade size of {size } the average trade return is {round(ave_return)}"
        
        
    
    #Close off residual responses to non trade inputs
    elif signal == "n":
        print("\nWithout a valid trade signal we can't calculate a potential profit!")
        print("please wait for a valid trade signal")
        return user_interface()
    
    else:
        print("Please enter only a 'y' or an 'n'")
        return user_interface()
        
#user_interface()         


##### APPLICATION INTERFACE ######
# This version of the user interface will take 5 arguments that will be specified by a user input form embedded in the
# streamlit app. The five arguments will mirror the 5 variables uses in the original user interface, as follows:
# signal (y/n), direction (long/short), target, drawdown, trade size

def app_interface(signal, direction, target, drawdown, size):
    """
    A function to create a user interface

    """

    dfx = pd.read_csv("..data/ftse_static.csv", parse_dates=["time"])

    # Conditional statements fed by the signal input
    if signal == 'Yes':

        # call the outcome function on the target and drawdown recieved, add the values to master dataframe

        temp = dfx.join(outcome_gen(target, drawdown))

        # call the net profit function on the target, drawdown and outcome, add values to master dataframe

        temp = temp.join(profit_gen(target, drawdown))

        # Filter for wins and losses using the inputted values
        win_filter = temp[temp.outcome == "win"].profit
        loss_filter = temp[temp.outcome == "loss"].profit

        # store a win average
        win_ave = win_filter.mean()

        # store a loss average for losses below the drawdown
        loss_ave = loss_filter.mean()

        # store a win count
        win_count = win_filter.shape[0]

        # store a loss count for losses below the drawdown
        loss_count = loss_filter.shape[0]

        # store a total number of trades
        trade_count = win_count + loss_count

        # Calculate and store the average returns based on the user requirements
        ave_return = (((win_ave * win_count) + (loss_ave * loss_count)) / trade_count) * size

        # Create the main return output for user consideration
        return f"Across {trade_count} total trades there are {win_count} winning trades at an average \
of {round(win_ave)} points per winning trade. There are {loss_count} losing trades at an average \
loss of {round(loss_ave)} points. For a trade size of {size} the average trade return is {round(ave_return)}"



    # Close off residual responses to non trade inputs
    elif signal == "No":
        print("\nWithout a valid trade signal we can't calculate a potential profit!")
        print("please wait for a valid trade signal")
        return None




