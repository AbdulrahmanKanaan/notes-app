from sqlalchemy.engine.base import Engine
from config.settings import get_settings
from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, Session

settings = get_settings()

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://" + \
    settings.DB_USERNAME + ":" + settings.DB_PASSWORD + \
    "@" + settings.DB_HOST + \
    ":" + settings.DB_PORT + "/" + settings.DB_DATABASE

engine: Engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def get_db() -> Session:
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# YOU CAN CHOOSE ONE
# Base = declarative_base()
# Base = automap_base()

# Base.prepare(engine, reflect=True)