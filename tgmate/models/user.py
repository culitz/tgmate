__author__ = 'ivan.koryshkin@gmail.com'

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from tgmate.models import Base
from tgmate.config import TABLENAME_USER


class User(Base):
    __tablename__ = TABLENAME_USER
    id = Column(Integer, primary_key=True)
    login = Column(String(20))
    password = Column(String) # todo: change to encrypted
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)

    def __repr__(self):
        return str({
            'id': self.id,
            'login': self.login,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
        })
