from sqlalchemy import engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from database.database import SessionLocal, engine
from abc import ABC

class Repository(ABC):

    db: Engine = None

    def __init__(self):
        self.db = engine