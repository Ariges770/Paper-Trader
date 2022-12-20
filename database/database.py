from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, DeclarativeBase

import os

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{os.environ.get('USERNAME')}:{os.environ.get('PASSWORD')}@{os.environ.get('DEV_HOSTNAME')}:{os.environ.get('PORT')}/{os.environ.get('DB')}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True, pool_recycle=60, echo_pool=False,
    pool_size=5, pool_timeout=30
)

db_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_SessionLoc = scoped_session(db_SessionLocal)

class Base(DeclarativeBase):
    pass

