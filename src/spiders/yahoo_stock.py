import yfinance
from decimal import *


from schemas import YahooStock

getcontext().prec = 5

async def get_stock(symbol: str):
    try:
        yahoo_data = yfinance.Ticker(symbol)
        yahoo_stock = YahooStock(
            symbol=yahoo_data.info['symbol'],
            name=yahoo_data.info['longName'],
            price_close=Decimal(yahoo_data.info['regularMarketPreviousClose']),
            current_price=Decimal(yahoo_data.info['currentPrice']),
            fiftyDayAverage=Decimal(yahoo_data.info['fiftyDayAverage']) * Decimal(1),
            volume=yahoo_data.info['volume'],
            avg_volume=yahoo_data.info['averageVolume'],
            market_cap=yahoo_data.info['marketCap'],
            pe_ratio=Decimal(yahoo_data.info['forwardPE']) * Decimal(1),
            dividend_yield=Decimal(yahoo_data.info['dividendYield']) * Decimal(100)
        )
        return yahoo_stock
    except Exception:
        return None

