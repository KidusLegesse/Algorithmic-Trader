# Algorithmic-Trading

**What is Algorithmic trading?** It is the use of mathematical models to inform trading decisions and typically utilizes computers (that have software which implements the strategy) to execute these trades. What is Mean reversion? [Wikipedia] (https://en.wikipedia.org/wiki/Mean_reversion_(finance)) defines it as "a financial term for the assumption that an asset's price will tend to converge to the average price over time. Using mean reversion as a timing strategy involves both the identification of the trading range for a security and the computation of the average price using quantitative methods.”


👷‍♂️**What does this program do?** This program implements a mean reversion trading strategy for a pair of stocks. The User inputs the two stocks then a timeframe to download the data along with some additional preferences. The program will produce a graph(s) depending on user input which will display information of price signals and spread.


**Example using AAPL and MSFT tickers** (Note AAPL and MSFT are not the most correlated tickers)
First open the command line and type
`make run`


Then follow the prompts to inputting all the necessary values


3. You will then get the following output




4. Finally when you exit the program will return the following



🧰🛠️**Libraries and Tools:** Pandas, Yfinance, Matplotlib, Statsmodels, Inquirer, Rich.

<h3>Important information:</h3>
-Make sure the stock ticker you input exists in [Yahoo Finance](https://finance.yahoo.com) since that is the api yfinance uses to get stock data.
-If you decide to run a cointegration test on a pair of uncorrelated stocks then the  program may exit notifying of this. In this case it may be helpful to run the program without the test to see the result regardless if they are cointegrated. 
-None of this is financial advice. This program is a personal project I had fun creating and wanted to share and was never intended to be used to execute any real trades on the stock market.
