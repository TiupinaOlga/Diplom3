import psycopg2
from pprint import pprint

class VKinder_DB():
    def __init__(self, DNS):
        self.engine = sq.create_engine(DSN)