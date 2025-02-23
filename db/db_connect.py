import os

from sqlalchemy import create_engine, sql
from sqlalchemy.orm import sessionmaker


DATABASE_NAME = os.environ.get("SQL_DATABASE")
DATABASE_URL = f'postgresql+psycopg2://{os.environ.get("SQL_USER")}:{os.environ.get("SQL_PASSWORD")}@{os.environ.get("SQL_HOST")}:{os.environ.get("SQL_PORT")}/'  # server
print(DATABASE_URL)

try:
    engine = create_engine(DATABASE_URL+DATABASE_NAME, max_overflow=-1)
    Session = sessionmaker(engine, autoflush=True, expire_on_commit=False)
    Base.metadata.create_all(engine)
except:
    with create_engine(DATABASE_URL, isolation_level='AUTOCOMMIT').connect() as connection:
        connection.execute(sql.text(f'CREATE DATABASE {DATABASE_NAME}'))

    engine = create_engine(DATABASE_URL+DATABASE_NAME, max_overflow=-1)
    Session = sessionmaker(engine, autoflush=True, expire_on_commit=False)
    Base.metadata.create_all(engine)


def create_all():
    Base.metadata.create_all(engine)
