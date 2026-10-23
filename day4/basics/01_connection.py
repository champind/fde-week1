import psycopg
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Connecting to database at: {DATABASE_URL}")

try:
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            result = cur.fetchone()
            print("Database connected successfully!")
            print("PostgreSQL version:", result[0])

except Exception as e:
    print("Database connection failed:", e)