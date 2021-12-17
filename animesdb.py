from sqlalchemy import Column, String, BigInteger, Integer
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


Base = declarative_base()

class Anime(Base):
    __tablename__ = 'anime'
    id = Column(Integer, primary_key=True, autoincrement=True)
    att = Column(String)


class ChannelFrom(Base):
    __tablename__ = 'channel_from'
    id = Column(Integer, primary_key=True, autoincrement=True)
    att = Column(BigInteger)


class ChannelTo(Base):
    __tablename__ = 'channel_to'
    id = Column(Integer, primary_key=True, autoincrement=True)
    att = Column(BigInteger)


tables = ('anime', 'channel_from', 'channel_to')


def asign(table: str):

    if table == tables[0]:
        obj = Anime
    elif table == tables[1]:
        obj = ChannelFrom
    else:
        obj = ChannelTo
    return obj


class DBHelper:
    def __init__(self, dbname: str):
        if dbname.startswith('postgres://'):
            dbname = dbname.replace('postgres://', 'postgresql://', 1)

        self.engine = create_engine(dbname)

        Base.metadata.bind = self.engine
        Base.metadata.create_all(checkfirst=True)

    def get_items(self, table: str):
        session: Session = sessionmaker(self.engine)()
        try:
            db_item = session.query(asign(table)).all()
            session.close()
            return db_item

        except Exception as e:
            session.close()
            print(f'An error occurred retrieving items. Item was\n{id}')
            raise e

    def add_items(self, table: str, attributes: list):
        session: Session = sessionmaker(self.engine)()
        try:
            obj = asign(table)
            for element in attributes:
                if not session.query(obj).filter_by(att=element).first():
                    session.add(obj(att=element))
            session.commit()
            session.close()
            return True
        except Exception as e:
            session.close()
            print(f'An error occurred in insertion. The item to insert was\n' +f'{id}')
            print(e)
            return False

    def del_items(self, table: str, list_id: list):
        session: Session = sessionmaker(self.engine)()
        try:

            for element in list_id:
                db_item = session.query(asign(table)).filter_by(id=element).first()
                if db_item:
                    session.delete(db_item)

            session.commit()
            session.close()
            return True

        except Exception as e:
            session.close()
            print(f'An error occurred updating. The item to update was\n{id}')
            return False
