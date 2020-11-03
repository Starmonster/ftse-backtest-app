import streamlit as st

import pandas as pf
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')

from ftse_functions import *
from user_interface_function import *

#Create dictionary's for our user input
signal_dictionary = {"No":1, "Yes":2}
direction_dictionary = {"Long":1, "Short":2}

def main():
    """ FTSE trade strategy backtest """

    st.title("FTSE 4hr strategy back test web app")
    st.subheader("This app states the average return across various parameters")

    menu = ["Home", "Back-Test"]

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        st.text("What is the aim of this app")

    elif choice == "Back-Test":
        st.subheader("Back Test Form, Results and Analysis")

        st.text("Current up to date dataset on 4hr timeline showing \
period start time, open, high, low,\nclose, candle direction \
signal yes / no features:")

        # Read in our static dataframe and display
        df = pd.read_csv("ftse_static.csv", parse_dates=["time"])

        st.dataframe(df)

        # Create a form to enter in the trade details
        st.subheader("Please enter your requirements in the form below")

        signal = st.selectbox("Has a 4hr signal been printed?", tuple(signal_dictionary.keys()))
        direction = st.selectbox("What is the trade direction", tuple(direction_dictionary.keys()))
        target = st.number_input("What is your target value?", 5, 100)
        drawdown = st.number_input("What is your maximum drawdown?", 5, 100)
        size = st.number_input("What is your trade size?", 1, 50)

        # Display the results of the user input on the screen.
        st.subheader("The back test for this trade has yielded the following results:")
        st.write(app_interface(signal, direction, target, drawdown, size))

        # Display a visualisation of the average drawdown for backetest wins

        # Create a temp dataset to store user values
        trade = df

        # Generate outcome values and join to temp dataset
        outcome = outcome_gen(target, drawdown)
        trade = trade.join(outcome)

        # Generate profit values and join to temp dataset
        profit = profit_gen(target, drawdown)
        trade = trade.join(profit)

        # Generate drawdown values and join to temp dataset
        drawdown_vals = drawdown_gen(target, drawdown)
        trade = trade.join(drawdown_vals)

        # Display the dataframe
        st.subheader("Dataframe to show results based on your input:")
        st.dataframe(trade)

        # Data visual to show frequency of drawdown sizes across winning trades
        # First we set some drawdown levels to be counted using the drawdowns generated by our dynamic dataset
        drawdown_size = list(range(0, int(trade.max_drawdown.max() + 2), 2))

        # Next we set an empty list to hold the quantities of each of our drawdown value ranges
        drawdown_quantity = []
        for i in drawdown_size:
            drawdown_quantity.append(trade[(trade.max_drawdown > i) & (trade.max_drawdown <= i + 2)].shape[0])

        # Now we can plot the data


        fig, ax = plt.subplots()

        #plt.figure(figsize=(12, 7))
        ax.bar(drawdown_size, drawdown_quantity, width=0.7)
        plt.title('Graph to show drawdown size and frequency', fontsize=18)
        plt.xlabel('Drawdown Size', fontsize=12)
        # plt.xlim([0,5])
        plt.ylabel('Drawdown Frequency', fontsize=12)
        plt.legend(['Drawdown'])
        # plt.show()

        st.pyplot(fig)











if __name__ == '__main__':
    main()