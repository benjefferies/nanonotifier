from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Notification(Base):
    __tablename__ = 'notification'
    email = Column(String, primary_key=True)
    account = Column(String)


Base.metadata.create_all(engine)
