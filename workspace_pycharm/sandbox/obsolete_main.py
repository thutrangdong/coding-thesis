from pytrends.request import TrendReq
import datetime
import pandas as pd
import matplotlib as plt

MAX_INTERVAL = 270
pytrends = TrendReq(hl='en-US', tz=360)


def get_daily_data(keyword, starting_date, ending_date):

    unadjusted_daily_data = get_unnormalized_daily_dataframe(keyword, starting_date, ending_date)
    adjusted_weekly_data = get_normalized_weekly_dataframe(keyword, starting_date, ending_date)
    adjusted_daily_data = compute_adjusted_daily_data(unadjusted_daily_data, adjusted_weekly_data)
    return 1


def get_timeframes_in_slices(starting_date, ending_date):

    starting_slices = list()
    ending_slices = list()
    while starting_date < ending_date:
        starting_slices.append(starting_date)

        starting_date = starting_date + datetime.timedelta(days=MAX_INTERVAL-1)
        if starting_date > ending_date:
            ending_slices.append(ending_date)
        else:
            ending_slices.append(starting_date)
            starting_date = starting_date + datetime.timedelta(days=1)
    return list(zip(starting_slices, ending_slices))


def get_unnormalized_daily_dataframe(keyword, starting_date, ending_date):

    timeframes_in_slices = get_timeframes_in_slices(starting_date, ending_date)
    unnormalized_daily_dataframe = pd.DataFrame()
    for slice in timeframes_in_slices:
        dataframe = api_request(keyword, slice[0], slice[1])
        unnormalized_daily_dataframe = unnormalized_daily_dataframe.append(dataframe)
    return unnormalized_daily_dataframe


def get_normalized_weekly_dataframe(keyword, starting_date, ending_date):
    weekday = starting_date.weekday()
    starting_date = starting_date - datetime.timedelta(days=weekday+1)
    return api_request(keyword, starting_date, ending_date)

def compute_adjusted_daily_data(unadjusted_daily_data, adjusted_weekly_data):

    data = pd.concat([unadjusted_daily_data, adjusted_weekly_data], axis=1)
    data.columns = ['bitcoin_daily', 'bitcoin_weekly']
    #with pd.option_context('display.max_rows', None, 'display.max_columns', 3):
    print(data)

def api_request(keyword, starting_date, ending_date):

    keywords = [keyword]
    starting_date = starting_date.strftime('%Y-%m-%d')
    ending_date = ending_date.strftime('%Y-%m-%d')
    timeframe = starting_date + ' ' + ending_date
    pytrends.build_payload(keywords, cat=0, timeframe=timeframe, geo='', gprop='')
    dataframe = pytrends.interest_over_time()
    dataframe.drop(['isPartial'], axis=1, inplace=True)

    return dataframe


if __name__ == "__main__":

    keyword = 'bitcoin'
    starting_date = datetime.date(2010, 1, 1)
    ending_date = datetime.date(2011, 9, 27)

    data = get_daily_data(keyword, starting_date, ending_date)