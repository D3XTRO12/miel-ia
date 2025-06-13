import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URI")
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("Database URI:", DATABASE_URL)
        print("✅ Database connection successful! Result:", result.scalar())
except Exception as e:
    print("❌ Database connection failed:", e)