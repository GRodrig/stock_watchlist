import asyncpg
from schemas import WatchListStock
import settings
import functools


async def create_pool(min_size: int, max_size: int) -> asyncpg.Pool:
    return await asyncpg.create_pool(
        host=settings.POSTGRES_DATABASE['HOST'],
        port=settings.POSTGRES_DATABASE['PORT'],
        user=settings.POSTGRES_DATABASE['USER'],
        password=settings.POSTGRES_DATABASE['PASSWORD'],
        database=settings.POSTGRES_DATABASE['DATABASE'],
        min_size=min_size,
        max_size=max_size
        )

def db_session(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        conn = await settings.POSTGRES_DB_POOL.acquire() 
        try:
            return await func(conn, *args, **kwargs)
        finally:
            await settings.POSTGRES_DB_POOL.release(conn)
    return wrapper

@db_session
async def db_add_stock_watchlist(conn: asyncpg.Connection, stock: WatchListStock) -> None:
    try:
        sql_query = (
            "INSERT INTO watchlist (symbol, name, price_close, current_price, change, percent_change, fiftyDayAverage)"
            "VALUES ($1, $2, $3, $4, $5, $6, $7)"
        )
        await conn.execute(
            sql_query,
            stock.symbol,
            stock.name,
            stock.price_close,
            stock.current_price,
            stock.change,
            stock.percent_change,
            stock.fiftyDayAverage,
        )
    except Exception as e:
        raise e
    
@db_session
async def db_list_watchlist(conn: asyncpg.Connection) -> None:
    try:
        sql_query = (
            "SELECT symbol, price_close, current_price, percent_change,fiftyDayAverage,  date_created  FROM watchlist"
        )
        return await conn.fetch(sql_query)
    except Exception as e:
        raise e