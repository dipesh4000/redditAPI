import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Access the variables using os.getenv()
DB_HOST = os.getenv("DATABASE_HOSTNAME")
DB_NAME = os.getenv("DATABASE_NAME")
DB_USER = os.getenv("DATABASE_USERNAME")
DB_PASS = os.getenv("DATABASE_PASSWORD")
DB_PORT = os.getenv("DATABASE_PORT")

try:
    conn = psycopg2.connect(host=DB_HOST,
                            database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            port=DB_PORT,
                            cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database Connected Successfully")
except Exception as error:
    print("Database not connected")
    print("Error: ", error)


