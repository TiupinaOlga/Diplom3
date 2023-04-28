import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from config import DNS
from models import Viewed, drop_tables, create_tables

def insert_db(engine):
    # self.engine = create_engine(DNS)
    Session = sessionmaker(bind=engine)
    with Session() as session:
        # to_db = Viewed(profile_id=123, worksheet_id=152)
        session.add(Viewed(profile_id=102, worksheet_id=532))
        session.commit()


def get_worksheet(engine, profile_id):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        query_pub = session.query(Viewed).filter(Viewed.profile_id == profile_id).all()
        for q in query_pub:
            print(q)


class DB_tools():
    def __init__(self, DNS):
        self.engine = sq.create_engine(DNS)


if __name__ == '__main__':
    db_tools = DB_tools(DNS)
    # drop_tables(db_tools.engine)
    # create_tables(db_tools.engine)
    # db_tools.inset_db(db_tools.engine)
    get_worksheet(db_tools.engine, 152)

