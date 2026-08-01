import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect

load_dotenv()
url = os.getenv("DATABASE_URL")
print("DATABASE_URL=", url)
if not url:
    raise SystemExit("No DATABASE_URL")
engine = create_engine(url)
print("tables=", inspect(engine).get_table_names())
