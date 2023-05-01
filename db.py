import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from config import DNS
from models import Viewed, drop_tables, create_tables
import random


def insert_db(engine, profile_id, worksheet_id):
    # self.engine = create_engine(DNS)
    Session = sessionmaker(bind=engine)
    with Session() as session:
        # to_db = Viewed(profile_id=123, worksheet_id=152)
        print(profile_id)
        session.add(Viewed(profile_id=profile_id, worksheet_id=worksheet_id))
        session.commit()


def get_worksheet(engine, worksheet_id):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        query_pub = session.query(Viewed).filter(Viewed.worksheet_id == worksheet_id).all()
        # for q in query_pub:
        # print(q)
        # return print(q)
        if query_pub:
            return True
        else:
            return False


def exists_table(engine):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        try:
            query_pub = session.query(Viewed).all()
            return 1
        except:
            return 0


class DB_tools():
    def __init__(self, DNS):
        self.engine = sq.create_engine(DNS)


if __name__ == '__main__':
    db_tools = DB_tools(DNS)
    # drop_tables(db_tools.engine)
    create_tables(db_tools.engine)
    # insert_db(db_tools.engine, None, 15548)
    if get_worksheet(db_tools.engine, 15548):
        print('True')
    # if exists_table(db_tools.engine):
    #     print('таблица существует')
    # else:
    #     print('таблица не найдна')


