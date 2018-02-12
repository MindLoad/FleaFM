# -*- coding: utf-8 -*-
# Created: 06.01.18
# Changed: 04.02.18

import sqlite3
import logging
import datetime


class DBConnection:
    """ Context manager: default settings """

    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        if exc_val:
            raise sqlite3.ProgrammingError


def logs(func):
    """ Setup logging decorate function """

    def wrapper(message):

        LOG_FORMAT = "%(levelname)s %(asctime)s :: %(message)s"
        logging.basicConfig(filename="error.log",
                            level=logging.DEBUG,
                            format=LOG_FORMAT)
        logger = logging.getLogger()
        logger.error(message)
        return func(message)

    return wrapper
