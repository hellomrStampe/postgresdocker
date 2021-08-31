from typing import Optional
from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import pandas as pd

# Configuration to local Postgres.
config = dotenv_values("containers/postgres/postgres.env")
HOST = "127.0.0.1"  # localhost
PORT = 5432
user_name = config.get("POSTGRES_USER", "postgres")
user_password = config.get("POSTGRES_PASSWORD", "admin")

# connection string to our service
CONNECTION_STRING = f"postgresql://{user_name}:{user_password}@{HOST}:{PORT}"


class Engine:

    """context managing engine
    Args:
        connection_string: string uri to postgres services
        database: databas name. default to None
    """

    def __init__(self, connection_string: str, database: Optional[str] = None) -> None:
        self.connection_string = connection_string
        self.database = database

    def __enter__(self) -> create_engine:
        if self.database is not None:
            self.connection_string = f"{self.connection_string}/{self.database}"

        self.engine = create_engine(self.connection_string)
        return self.engine

    def __exit__(self, type, value, traceback) -> None:
        self.engine.dispose()


# executing raw SQL query e.g. create database
DB_NAME = "weapons"
print(f"[+] Creating DB named {DB_NAME}")
with Engine(CONNECTION_STRING) as engine:
    autoengine = engine.execution_options(isolation_level="AUTOCOMMIT")
    with autoengine.connect() as conn:
        conn.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
        conn.execute(f"CREATE DATABASE {DB_NAME}")

# send CSVs, excels or any tabular data to Postgres
# sending dataframe to database weapons, replacing if it exists
dataf = pd.DataFrame(
    {
        "bullets": ["kolibri", "bonecrusher", "tranter"],
        "damage": [0.8, 0.76, 0.98],
        "date": pd.date_range(start="18/03/2021", periods=3),
    }
)

TABLE_NAME = "bullets"
print(f"[+] Sending dataf to DB: {DB_NAME}, Table: {TABLE_NAME}")
with Engine(CONNECTION_STRING, database=DB_NAME) as conn:
    # Send data to postgres
    dataf.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)

# read data from postgres

query = """
        SELECT * FROM "bullets"
        WHERE damage >= 0.78
        """
with Engine(CONNECTION_STRING, database=DB_NAME) as conn:
    # retrieve data from Postgres
    result = pd.read_sql_query(query, conn)


print("\nResults")
print(result)

print("\nResults Tables")
print(result.dtypes)

# cleaning up ;)
print(f"[+] Dropping DB named {DB_NAME}")
#with Engine(CONNECTION_STRING) as engine:
#    autoengine = engine.execution_options(isolation_level="AUTOCOMMIT")
#    with autoengine.connect() as conn:
#        conn.execute(f"DROP DATABASE {DB_NAME}")

print("Tasks completed")
