import os
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
    email = Column(String, primary_key=True)
    account = Column(String)

    def __repr__(self):
        return f"<Subscription(email='{self.email}', account='{self.account}')>"


Base.metadata.create_all(engine)
