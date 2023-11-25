import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import coint
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.traceback import install

install(show_locals=True)

console = Console()

# Function to fetch historical stock data
def get_stock(stock, start_date, end_date):
    stock_data = yf.download(stock, start=start_date, end=end_date)
    return stock_data['Adj Close']
 
# Function to test for cointegration
def cointegration_pair(stock1_info, stock2_info):
    _, pvalue, _ = coint(stock1_info, stock2_info)
    return pvalue

# Pairs trading strategy
def MeanReversion_strategy(stock1, stock2, start_date, end_date, coint, show_spread, num_sample_datapoints=30, entry_zscore=2.0, min_zscore=0.5):
    if start_date>end_date:
        start = start_date.replace("-01-01", "")
        end= end_date.replace("-01-01", "")
        return console.print((Panel.fit("[bold bright_red]:bangbang: The [bold green]Start year[/bold green] is greater then the [bold yellow]End year[/bold yellow] [bold bright_red]:bangbang:",title =f"[bold green]{start}[/bold green]" + ">" + f"[bold yellow]{end} [/bold yellow]")))
    #data for the two stocks
    stock1_info = get_stock(stock1, start_date, end_date)
    stock2_info = get_stock(stock2, start_date, end_date)

    # test the cointegration only if user wants

    if coint == True:
        pvalue = cointegration_pair(stock1_info, stock2_info)
        if pvalue > 0.05:
            console.print("The assets are not cointegrated.")
            return None, None, None

    # Difference in price of stock1 and stock2
    spread = stock1_info - stock2_info


    # Find the z-score using the spread
    z_score = (spread - spread.rolling(window=num_sample_datapoints).mean()) / spread.rolling(window=num_sample_datapoints).std()

    # Determining whether to enter (short or long) and exit a trade
    long_stock = z_score < -entry_zscore
    short_stock = z_score > entry_zscore
    exit_position = np.abs(z_score) < min_zscore

    # Create a dataframe of prices based on trade signals
    long_positions = pd.concat([stock1_info[long_stock], stock2_info[short_stock]])
    short_positions = pd.concat([stock1_info[short_stock], stock2_info[long_stock]])
    exit_prices = pd.concat([stock1_info[exit_position], stock2_info[exit_position]])

    #Plot two graphs ax2 shows the spread the ax1 shows the prices to enter and exit
    if (show_spread):
        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(14, 6), gridspec_kw={'width_ratios': [1, 1], 'hspace': 0.5})
        ax1.plot(stock1_info.index, stock1_info, label=stock1, color='#F55C47')
        ax1.plot(stock2_info.index, stock2_info, label=stock2, color='#F1F6F5')
        ax1.set_ylabel('Stock Price ($USD)', color='#F1F6F5')
        ax1.set_xlabel('Date(YYYY-MM)', color='#F1F6F5')
        ax1.set_title("Stock Graph", color='#F1F6F5')
        ax1.scatter(long_positions.index, long_positions, marker='^',color='#00FF00', label='Enter Long')
        ax1.scatter(short_positions.index, short_positions, marker='v', color='#FF0000', label='Enter Short')
        ax1.scatter(exit_prices.index, exit_prices, marker='o', color='#3AB4F2', label='Exit')
        legend=ax1.legend()
        legend.set_frame_on(True)
        legend.get_frame().set_facecolor('#51C4D3')
        ax1.set_facecolor('#272829')
        ax1.tick_params(axis='x', colors="#F55C47")
        ax1.tick_params(axis='y', colors="#F55C47")

        mean_spread = spread.rolling(window=num_sample_datapoints).mean()
        std_spread = spread.rolling(window=num_sample_datapoints).std()
        ax2.plot(spread.index, spread, color='#6C00FF')
        ax2.plot(mean_spread.index, mean_spread, label='Mean Spread', linestyle='-', color='#FF0063')
        ax2.fill_between(mean_spread.index, mean_spread - 2 * std_spread, mean_spread + 2 * std_spread, color='#D8E3E7', alpha=0.2)
        ax2.set_ylabel('Amount ($USD)', color="#6C00FF")
        ax2.set_xlabel('Date (YYYY-MM)', color="#6C00FF")
        ax2.set_title("Spread", color='#6C00FF')
        legend=ax2.legend()
        legend.set_frame_on(True)
        legend.get_frame().set_facecolor('#51C4D3')
        ax2.set_facecolor('#272829')
        ax2.tick_params(axis='x', colors="#FF0063")
        ax2.tick_params(axis='y', colors="#FF0063")
        fig.set_facecolor('#272829')
        plt.show()
    #Plot only one graph of the price to enter and exit    
    else:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(stock1_info.index, stock1_info, label=stock1, color='#F55C47')
        ax.plot(stock2_info.index, stock2_info, label=stock2, color='#F1F6F5')
        ax.set_ylabel('Stock Price ($USD)', color='#F1F6F5')
        ax.set_xlabel('Date(YYYY-MM)', color='#F1F6F5')
        ax.set_title("Stock Graph", color='#F1F6F5')
        ax.scatter(long_positions.index, long_positions, marker='^',color='#00FF00', label='Enter Long')
        ax.scatter(short_positions.index, short_positions, marker='v', color='#FF0000', label='Enter Short')
        ax.scatter(exit_prices.index, exit_prices, marker='o', color='#3AB4F2', label='Exit')
        legend=ax.legend()
        legend.set_frame_on(True)
        legend.get_frame().set_facecolor('#51C4D3')
        ax.set_facecolor('#272829')
        ax.tick_params(axis='x', colors="#F55C47")
        ax.tick_params(axis='y', colors="#F55C47")
        fig.set_facecolor('#272829')

        plt.show()
    #Creates three tabes of prices to long , short, and exit and the dates limitted to the past 5 data points
        
    long = long_positions.to_frame()

    short = short_positions.to_frame()

    exit = exit_prices.to_frame()

    def gen_tables(data, string, headerstyle, style):

        console = Console()
        data_table = Table(show_header=True, header_style=headerstyle)
        data_table.add_column("Date", style="cyan")
        data_table.add_column(string+" Prices", style=style)

        for index, row in data.tail().iterrows():
            date_str = index.strftime("%Y-%m-%d")
            data_table.add_row(date_str, str(row['Adj Close']))

        console.print(data_table)

    gen_tables(long, "Long", "green", "magenta")
    gen_tables(short, "Short", "cyan", "magenta")
    gen_tables(exit, "Exit", "red", "magenta")
    console.print((Panel.fit("[bold bright_red] NOT FINANCIAL ADIVICE [bold bright_red] :bangbang:", title="[bold yellow1]Great Work[/bold yellow1] :confetti_ball: :trophy:", subtitle="[bold light_green]Thank you[/bold light_green] :smiley:")))
