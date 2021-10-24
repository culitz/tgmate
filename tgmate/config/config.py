__author__ = 'ivan.koryshkin@gmail.com'

import os
from typing import Optional
from pathlib import Path
from logging import Logger
from dotenv import load_dotenv
from .config_varibles import DATABASE_DRIVER
from .config_varibles import DATABASE_HOST
from .config_varibles import DATABASE_NAME
from .config_varibles import DATABASE_USER
from .config_varibles import DATABASE_PASS
from .config_varibles import DATABASE_PORT
from .config_varibles import TELEGRAM_TOKEN


class Config:
    """
    A class for collecting environment variables and converting them to the form needed for work
    """
    def __init__(self, logger: Optional[Logger] = None, **kwargs) -> None:
        self.__logger = logger
        use_dotenv: bool = kwargs.get('DotEnv', False)
        if use_dotenv:
            dotenv_file = Path().cwd() / '.env'
            load_dotenv(dotenv_file)
            self.__logger.info(f'[.env] {dotenv_file}')

        self.__db_driver: Optional[str] = os.getenv(DATABASE_DRIVER, None)
        self.__user: Optional[str] = os.getenv(DATABASE_USER, None)
        self.__passwd: Optional[str] = os.getenv(DATABASE_PASS, None)
        self.__host: Optional[str] = os.getenv(DATABASE_HOST, None)
        self.__db: Optional[str] = os.getenv(DATABASE_NAME, None)
        self.__port: Optional[str] = os.getenv(DATABASE_PORT, None)
        self.__token: Optional[str] = os.getenv(TELEGRAM_TOKEN, None)

    def get_db_url(self) -> Optional[str]:
        """
        Get database connection string for SQLAlchemy like:
        'postgresql://admin:password126854578@10.72.101.12:5432/database_name'
        """
        if self.check_env_vars():
            return f'{self.__db_driver}://{self.__user}:{self.__passwd}@{self.__host}:{self.__port}/{self.__db}'

    def check_env_vars(self) -> bool:
        """
        Check environment variables, in system.
        :return: If all variables is exist return True, else False
        """       
        vars = {
            DATABASE_DRIVER: self.__db_driver,
            DATABASE_USER: self.__user,
            DATABASE_PASS: self.__passwd,
            DATABASE_HOST: self.__host,
            DATABASE_NAME: self.__db,
            DATABASE_PORT: self.__port,
            TELEGRAM_TOKEN: self.__token
        }

        for varname in vars:
            var: Optional[str] = vars.get(varname, None)
            is_not_exist: bool = var is None
            if is_not_exist:
                self.__logger.error(f'[{varname}] not found')
                return False

        return True

    # Setters
    def set_db_driver(self, db_driver):
        self.__db_driver = db_driver
    
    def set_user(self, user):        
        self.__user = user
    
    def set_passwd(self, passwd):        
        self.__passwd = passwd
    
    def set_host(self, host):        
        self.__host = host
    
    def set_db(self, db):        
        self.__db = db
    
    def set_port(self, port):        
        self.__port = port

    
    # Getters
    def get_db_driver(self) -> str:
        return self.__db_driver

    def get_user(self) -> str:        
        return self.__user
    
    def get_passwd(self) -> str:        
        return self.__passwd
    
    def get_host(self) -> str:        
        return self.__host
    
    def get_db(self) -> str:        
        return self.__db
    
    def get_port(self) -> int:        
        return self.__port

    def get_token(self) -> str:
        return self.__token