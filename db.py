import sqlalchemy as sq
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from config import DNS

#Схема ДБ
metadata = MetaData()
Base = declarative_base()

class Engine():
    def __init__(self, DNS):
        self.engine = sq.create_engine(DSN)

class Viewed(Base):
    __tablename__ = 'viewed'

    profile_id = sq.Column(sq.Integer, primary_key=True)
    worksheet_id = sq.Column(sq.Integer, unique=True)

def insret_db(self):
    engine = create_engine(db_url_object)
    Session = sessionmaker(bind=engine)
    session = Session()
    to_db = Viewed(profile_id=123,worksheet_id=3221)
    session.add(to_db)

def create_tables(engine):
    Base.metadata.create_all(engine)

def drop_tables(engine):
    Base.metadata.drop_all(engine)

if __name__ == '__main__':
    DSN = 'postgresql://postgres:wonder@localhost:5432/diplom'
    engine = sq.create_engine(DSN)

    drop_tables(engine)
    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()