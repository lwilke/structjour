# import logging

from PyQt5.QtCore import QSettings
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, create_engine, Column, Integer, String, Sequence
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
Session = sessionmaker()


class MigrateModel(Base):
    '''
    A table to keep track of migrations that have run so that we may skip or
    partially run as needed.
    '''
    __tablename__ = 'migrate_model'
    id = Column(Integer, Sequence('migrate_model_id_seq'), primary_key=True)
    m_id = Column(String(4), nullable=False)
    date = Column(String(6), nullable=False)
    data_key = Column(String)
    data_val = Column(Integer)

    def __repr__(self):
        return f"<MigrateModel({self.m_id})>"


class ModelBase:
    '''
    Contains common methods for migration and static variables used by sqlalchemy stuff
    '''

    settings = QSettings('zero_substance', 'structjour')
    metadata = MetaData()
    db = None
    session = None
    engine = None

    conn = None
    cur = None

    # @classmethod
    # def checkDbStatus(cls):
    #     if cls.settings.value('tradeDb') is None:
    #         return
    #     if not os.path.exists(cls.settings.value('tradeDb')):
    #         msg = f"Database connection is not setup correctly: {cls.settings.value('tradeDb')}"
    #         # logging.error(msg)
    #         print(msg)
    #         cls.settings.remove('tradeDb')
    #         # raise ValueError(msg)
    #     else:
    #         print(f"Ready to update the database: {cls.settings.value('tradeDb')}")
    #         # logging.info(f"Ready to update the database: {cls.settings.value('tradeDb')}")

    @classmethod
    def connect(cls, new_session=False, con_str=None):
        if con_str is None:
            if cls.settings.value('tradeDb') is None:
                cls.engine = None
                cls.session = None
                return
            else:
                cls.db = "sqlite:///" + cls.settings.value('tradeDb')
        else:
            cls.db = con_str

        if cls.engine is None:
            cls.engine = create_engine(cls.db)
        if new_session:
            Session.configure(bind=cls.engine)
            cls.session = Session()

    @classmethod
    def checkVersion(cls, mv, v):
        if v < mv:
            raise ValueError(f'Incorrect version of structjour {v}. This code requires version >= {mv}')

    @classmethod
    def createAll(cls):
        if cls.engine is None:
            raise ValueError('ModelBase.connect() must be called prior to createAll()')
        Base.metadata.create_all(cls.engine)


def dostuff():
    pass


if __name__ == '__main__':
    dostuff()
