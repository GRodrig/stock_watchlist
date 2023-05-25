
from decimal import Decimal, getcontext
from fastapi import FastAPI, HTTPException
from loguru import logger
from db.models import create_pool, db_add_stock_watchlist, db_list_watchlist
from exception import InvalidFields, StockNotFound
from schemas import WatchListStock
import settings
from spiders.yahoo_gainers import StockType, get_gainer_loser
from spiders.yahoo_stock import get_stock
import asyncpg
getcontext().prec = 4

app = FastAPI(title="Stocks API",
              description="Stocks API retrives metadata from several stocks. 🚀",
              version="1.0.0")


@app.on_event("startup")
async def startup_event():
    settings.POSTGRES_DB_POOL = await create_pool(min_size=10,max_size=10)
    print("up")
    


@app.get("/stock/{stock_symbol}")
async def get_stock_info(
    stock_symbol: str,
):
    try:
        result = await get_stock(stock_symbol)
        if result is None:
            raise StockNotFound()
        return result
    except StockNotFound:
        raise HTTPException(status_code=404, detail='Stock not found')
    except Exception as e:
        logger.exception(f'Spider error for stock {stock_symbol}.') 
        raise HTTPException(status_code=500, detail='Server Error') from e


@app.get("/stocks/{stock_type}")
async def get_stocks_gainers_losers(
    stock_type: StockType = StockType.GAINERS,
    offset: int = 0,
    limit: int = 100,
):
    try:
        if offset < 0 or limit < 0:
            raise InvalidFields()
        result = await get_gainer_loser(stock_type, offset, limit)
        return result
    except InvalidFields:
        raise HTTPException(status_code=400, detail='Invalid fields')
    except Exception as e:
        logger.exception(f'Spider error for stock {stock_type}.') 
        raise HTTPException(status_code=500, detail='Server Error') from e


@app.post("/watchlist/{stock_symbol}")
async def add_stock_watchlist(
    stock_symbol: str,
):
    try:
        result = await get_stock(stock_symbol)
        if result is None:
            raise StockNotFound()
            
        stock_watchlist = WatchListStock(
            symbol=result.symbol,
            name=result.name,
            price_close=result.price_close,
            current_price=result.current_price,
            change=result.current_price - result.price_close,
            percent_change= (Decimal(result.current_price/result.price_close) - Decimal(1)) * Decimal(100),
            fiftyDayAverage=result.fiftyDayAverage,
            )
        await db_add_stock_watchlist(stock_watchlist)
        return {'status': 'success'}
    except StockNotFound:
        raise HTTPException(status_code=404, detail='Stock not found')
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=409, detail='Stock already exists in watchlist')
    except Exception as e:
        logger.exception(f'Spider error for stock {stock_symbol}.') 
        raise HTTPException(status_code=500, detail='Server Error') from e


@app.get("/watchlist/list")
async def list_watchlist():
    try:
        result = await db_list_watchlist()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail='Server Error') from e