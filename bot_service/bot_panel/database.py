import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def connect_db():
    return await asyncpg.create_pool(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('DB_NAME'),
        host=os.getenv('DB_HOST')
    )
