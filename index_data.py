import json
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from yahoo_fin.stock_info import get_data, get_quote_data


def gather_data():
    with open("ticker.json", "r") as ticker_file:
        ticker_list = json.load(ticker_file)['ticker_list']
    start_date = dt.datetime(2012, 1, 1)
    end_date = dt.datetime(2022, 1, 1)
    data_list = {}
    for index in ticker_list:
        ticker = ticker_list[index]
        try:
            index_data = get_data(ticker=ticker, start_date=start_date, end_date=end_date, interval="1mo")
            monthly_return = index_data['close'].pct_change()
            monthly_return = monthly_return.drop(monthly_return.index[0])
            mean_monthly_return = monthly_return.mean()  
            mean_yearly_return = mean_monthly_return * 12 
            monthly_standard_dev = monthly_return.std()
            yearly_standard_dev = monthly_standard_dev * np.sqrt(12)
            data_list[index] = {"Ticker": ticker, "Mean Monthly Return": mean_monthly_return, "Mean Yearly Return": mean_yearly_return, "Monthly Volatility": monthly_standard_dev, "Yearly Volatility": yearly_standard_dev}
        except:
            continue
    
    return data_list


def end_money(start_cash, duration, data):
    if duration.find("mo") != -1:
        period = "Monthly"
        number = int(duration.replace("mo", ""))
    else:
        period = "Yearly"
        number = int(duration.replace("y", ""))
    for index in data:
        pct_return = data[index].get(f"Mean {period} Return")
        cash = start_cash
        for i in range(number):
            cash = cash + pct_return*cash
        data[index]["End Cash"] = cash
    return data


def get_graph(data_list, duration):
    x = [index for index in data_list]
    yearly_returns = [data_list[index]["Mean Yearly Return"]*100 for index in data_list]
    variance = [((data_list[index]["Yearly Volatility"])**2)*100 for index in data_list]
    end_cash = [data_list[index]["End Cash"] for index in data_list]
    x_pos = [i for i, _ in enumerate(x)]

    plt.figure(figsize=(10, 12))
    plt.barh(x_pos, yearly_returns, color='green', xerr=variance)
    plt.ylabel("Index")
    plt.xlabel("Yearly Return in %")
    plt.title("Yearly Return for Various Indices")

    plt.yticks(x_pos, x)
    plt.show()
    plt.figure(figsize=(10, 12))
    plt.barh(x_pos, end_cash, color='green')
    plt.ylabel("Index")
    plt.xlabel("Cash")
    plt.title(f"End cash after {duration}")

    plt.yticks(x_pos, x)
    plt.show()

def get_index_details(index_data, starting_cash):
    ticker = index_data['Ticker']

    invested_pct = starting_cash / index_data['End Cash'] * 100  
    cash_return_pct = 100 - invested_pct
    labels = 'Invested', 'Cash Return'
    sizes = [invested_pct, cash_return_pct]
    explode = (0, 0.1)

    fig1, ax1 = plt.subplots()
    _, autotexts, _ = ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis("equal")
    for autotext in autotexts:
            autotext.set_color("white")
    plt.show()

    quote_data = get_quote_data(ticker)
    full_exchange_name = quote_data["fullExchangeName"]
    current_price = quote_data["regularMarketPreviousClose"]
    df = pd.DataFrame([[full_exchange_name, ticker, current_price]], columns=["Full Exchange Name", "Ticker", "Current Price"])

    return df
