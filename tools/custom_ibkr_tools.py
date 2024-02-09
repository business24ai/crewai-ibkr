from langchain.tools import tool
from ib_insync import *


class CustomTradingTools():

    @tool("Get the positions of the portfolio")
    def get_positions_of_portfolio(separator="and") -> str:
        """Useful wo get the ticker symbols of the positions in the portfolio.
           This function returns a string of the ticker symbols separated with 'and'.
           
           :param separator: str, separator to be used to separate the ticker symbols
           :return value: str, A string of ticker symbols
           """
        try:
            ib = IB()
            ib.connect("127.0.0.1", 7497, clientId=1)

            position_list = ib.positions()

            symbols = [position.contract.symbol for position in position_list]
            position_tickers = ' {separator} '.join(symbols)

            ib.disconnect()

            if position_tickers:
                return position_tickers
            else:
                return "No positions found"
        except Exception:
            return "No data available."
        

    @tool("Fetch live last stock price")
    def fetch_live_last_stock_price(ticker_symbol: str) -> str:
        """Useful to fetch the live last stock data when the markets are open.
           The last price of the stock with the given ticker will be returned.
           
           :param ticker_symbol: str, only one ticker symbol
           :return value: str, A string of the last price of the stock
           """
        try:
            ib = IB()
            ib.connect("127.0.0.1", 7497, clientId=2)

            stock = Stock(ticker_symbol, "SMART", "USD")

            market_data = ib.reqMktData(stock)
            ib.sleep(2)
            last = market_data.last
            ib.disconnect()
            
            # return the filename
            return f"Last price of {ticker_symbol} is {last}."
        except Exception:
            return "No data is available."
