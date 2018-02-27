import uuid

from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Subscription(Base):
    __tablename__ = 'subscription'
    id = Column(String, primary_key=True, default=uuid.uuid4)
    email = Column(String)
    webhook = Column(String)
    account = Column(String)

    def __init__(self, email, webhook, account):
        self.id = str(uuid.uuid4())
        self.email = email
        self.webhook = webhook
        self.account = account

    def __repr__(self):
        return f"<Subscription(email='{self.email}', webhook='{self.webhook}', account='{self.account}')>"


Base.metadata.create_all(engine)
