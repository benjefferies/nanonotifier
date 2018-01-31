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

    def __repr__(self):
        return f"<Notification(email='{self.email}', account='{self.account}')>"


Base.metadata.create_all(engine)
