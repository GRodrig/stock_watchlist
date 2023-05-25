
import asyncpg

POSTGRES_DB_POOL: asyncpg.Pool  = None

POSTGRES_DATABASE = {
    "HOST": "postgres",
    "NAME": "postgres",
    "DATABASE": "watchlist",
    "PORT": 5432,
    "USER": "postgres",
    "PASSWORD": "postgres",
}
