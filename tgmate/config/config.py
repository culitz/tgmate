__author__ = 'ivan.koryshkin@gmail.com'

import os
from typing import Optional
from tgmate.config import DATABASE_DRIVER
from tgmate.config import DATABASE_HOST
from tgmate.config import DATABASE_NAME
from tgmate.config import DATABASE_USER
from tgmate.config import DATABASE_PASS
from tgmate.config import DATABASE_PORT


class Config:
    """
    A class for collecting environment variables and converting them to the form needed for work
    """
    def __init__(self) -> None:
        self._db_driver: Optional[str] = os.getenv(DATABASE_DRIVER, None)
        self._user: Optional[str] = os.getenv(DATABASE_USER, None)
        self._passwd: Optional[str] = os.getenv(DATABASE_PASS, None)
        self._host: Optional[str] = os.getenv(DATABASE_HOST, None)
        self._db: Optional[str] = os.getenv(DATABASE_NAME, None)
        self._port: Optional[str] = os.getenv(DATABASE_PORT, None)

    def get_db_url(self) -> Optional[str]:
        """
        Get database connection string for SQLAlchemy like:
        'postgresql://admin:password126854578@10.72.101.12:5432/database_name'
        """
        arr = (self._db_driver, self._user, self._passwd, self._host, self._db, self._port)
        check_arr = [item is not None for item in arr]
        
        is_ok: bool = all(check_arr)
        if is_ok:
            return f'{self._db_driver}://{self._user}:{self._passwd}@{self._host}:{self._port}/{self._db}'

    # Setters
    def set_db_driver(self, db_driver):
        self._db_driver = db_driver
    
    def set_user(self, user):        
        self._user = user
    
    def set_passwd(self, passwd):        
        self._passwd = passwd
    
    def set_host(self, host):        
        self._host = host
    
    def set_db(self, db):        
        self._db = db
    
    def set_port(self, port):        
        self._port = port

    
    # Getters
    def get_db_driver(self):
        return self._db_driver

    def get_user(self):        
        return self._user
    
    def get_passwd(self):        
        return self._passwd
    
    def get_host(self):        
        return self._host
    
    def get_db(self):        
        return self._db
    
    def get_port(self):        
        return self._port
