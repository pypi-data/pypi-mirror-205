import streamsync as ss

import yfinance as yf
import datetime
import pandas as pd
import altair as alt
# This is a placeholder to get you started or refresh your memory.
# Delete it or adapt it as necessary.

# Shows in the log when the app starts
print("Hello world!")


# If your code uses pandas_datareader and you want to download data faster, 
# you can "hijack" pandas_datareader.data.get_data_yahoo() 
# method to use yfinance while making sure the returned data is in the 
# same format as pandas_datareader's get_data_yahoo().
yf.pdr_override()

# Its name starts with _, so this function won't be exposed
# Original code
def _update_message(state):
    is_even = state["counter"] % 2 == 0
    message = "The number is " + ("even" if is_even else "odd")
    state["message"] = message

def decrement(state):
    state["counter"] -= 1
    _update_message(state)

def increment(state):
    state["counter"] += 1
    print(f"The counter has been incremented.")
    _update_message(state)
    
def zeroing(state):
    state["counter"] = 0
    _update_message(state)


# This function is a handler for a dropdown box on sidebar
# it would have a few stocks over there and the one we pick, will be downloads
def yf_picker(state, payload):
    # Pick last year
    today = datetime.date.today()
    date_from = (today - datetime.timedelta(days=366)).strftime("%Y-%m-%d")
    start = pd.to_datetime(date_from)
    end = pd.to_datetime(today)
    # Downlado the data
    data = yf.download(payload, start, end)
    # deleting a few columns, so it will be easier to play with altair
    del data["Open"]
    del data["High"]
    del data["Low"]
    del data["Volume"]
    del data["Close"]
    # make sure the data is on the right format, so Altair can't complain
    data.index = pd.to_datetime(data.index, format='%d-%m-%Y')
    # Assing the dataframe to the state.
    state["stock"] = data
    
    # Log
    print(data)

    # If we have new stock, we want to refresh the chart.
#    update_chart(state)
# Initialise the state

def update_chart(state):
    # Sample dataframe from Altair website
    source = pd.DataFrame({
        'x': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
        'y': [28, 55, 43, 91, 81, 53, 19, 87, 52]
    })

    # Working version for a chart
    base = alt.Chart(state["stock"].reset_index()).mark_line().encode(
        alt.X('Date:T', title = " "),
        alt.Y('Adj Close:Q', title = " ")
    )
    
    # Sample chart from Altair website
    #
    # HERE IT BREAKS
    # I forgot to revert to the source variable and instead I left the state["stock"]
    # base = alt.Chart(state["stock"]).mark_line().encode(
    #     x = 'x',
    #     y = 'y'
    # )
    

    state["altair"] = base

def ramiro_chart(state):
    source = pd.DataFrame({
        'a': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
        'b': [28, 55, 43, 91, 300, 53, 19, 87, 52]
    })

    state["altair"] = alt.Chart(source).mark_bar().encode(
        x='a',
        y='b'
    )

initial_state = ss.init_state({
    "my_app": {
        "title": "My App"
    },
    "message": None,
    "counter": 26,
})

_update_message(initial_state)
yf_picker(initial_state, "AAPL")
