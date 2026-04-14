import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
from src.config import settings
import logging

logger = logging.getLogger(__name__)

pool = ThreadedConnectionPool(
    minconn=1,
    maxconn=10,
    host=settings.database_hostname,
    database=settings.database_name,
    user=settings.database_username,
    password=settings.database_password,
    port=settings.database_port,
    cursor_factory=RealDictCursor,
)

logger.info("Database connection pool created successfully")


def get_connection():
    return pool.getconn()


def release_connection(conn):
    pool.putconn(conn)
