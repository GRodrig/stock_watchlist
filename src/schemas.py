from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel

class StockType(str, Enum):
    GAINERS = 'gainers'
    LOSERS = 'losers'

class WatchListStock(BaseModel):
    symbol: str
    name: str
    price_close: Decimal
    current_price: Decimal
    fiftyDayAverage: Decimal
    change: Decimal 
    percent_change: Decimal


class YahooStock(BaseModel):
    symbol: str
    name: str
    price_close: Decimal
    current_price: Decimal
    fiftyDayAverage: Decimal
    volume: int
    avg_volume: int
    market_cap: int
    pe_ratio: Decimal
    dividend_yield: Decimal    


class YahooGainLoser(BaseModel):
    symbol: str
    name: str
    price: str
    change: str
    percent_change: str
    volume: str
    avg_volume: str
    market_cap: str
    pe_ratio: str
   