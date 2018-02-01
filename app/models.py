import os
import uuid

from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_url = os.getenv('DATABASE_URL')
engine = create_engine(db_url, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Subscription(Base):
    __tablename__ = 'subscription'
    id = Column(String, primary_key=True, default=uuid.uuid4)
    email = Column(String)
    account = Column(String)

    def __init__(self, email, account):
        self.id = str(uuid.uuid4())
        self.email = email
        self.account = account

    def __repr__(self):
        return f"<Subscription(email='{self.email}', account='{self.account}')>"


Base.metadata.create_all(engine)
