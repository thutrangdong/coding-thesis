# Try to split up search requests to get daily Google Trend data
from datetime import datetime, timedelta
from pytrends.request import TrendReq
import pandas as pd
import os

path = ' '
os.chdir(path)
filename = ' '
step = 200  # This is not the maximum step size to get daily data, but I did not test to get the maximum yet
kw_list = [' ', ' ']
start_date = datetime(YYYY, MM, DD)

# Login to Google. Only need to run this once, the rest of requests will use the same session.
pytrend = TrendReq()

# Run the first time
today = datetime.today()
old_date = today.date()
# Go 200 days back in time
new_date = today.date() - timedelta(days=step)
# Create new timeframe for which we download data
timeframe = new_date.strftime('%Y-%m-%d') + ' ' + old_date.strftime('%Y-%m-%d')
pytrend.build_payload(kw_list=kw_list, timeframe=timeframe)
interest_over_time_df = pytrend.interest_over_time()

while new_date > start_date.date():
    # Save the new date from the previous iteration
    old_date = new_date
    # Update the new date to take a step into the past
    new_date = new_date - timedelta(days=step)
    # New timeframe
    timeframe = new_date.strftime('%Y-%m-%d') + ' ' + old_date.strftime('%Y-%m-%d')
    print(timeframe)
    # Download data
    pytrend.build_payload(kw_list=kw_list, timeframe=timeframe)
    temp_df = pytrend.interest_over_time()

    # Renormalize the dataset and drop last line
    for kw in kw_list:
        beg = new_date
        end = old_date - timedelta(days=1)
        if temp_df[kw].iloc[-1] != 0:
            scaling = interest_over_time_df[kw].iloc[0] / temp_df[kw].iloc[-1]
        elif temp_df[kw].iloc[-1] == 0:
            scaling = 0
            # Basically: if the trend falls to zero, assume that everything before is approximately zero. Not great, but someone should put more thought into this.
        temp_df.loc[beg:end, kw] = temp_df.loc[beg:end, kw] * scaling
    # drop the last row
    temp_df = temp_df[:-1]
    # Cocenate both datasets
    frames = [temp_df, interest_over_time_df]
    interest_over_time_df = pd.concat(frames)

# Save dataset
interest_over_time_df.to_csv(filename)