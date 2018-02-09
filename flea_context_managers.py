# -*- coding: utf-8 -*-
# Created: 06.01.18
# Changed: 06.01.18

import sqlite3


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
