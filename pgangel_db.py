#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import psycopg2
import psycopg2.extras
import json


class DBConnection():

    def __init__(self, host, port, database, username=None, password=None):
        if not (username and password):
            auths = []
            try:
                pgpass = os.path.expanduser('~/.pgpass')
                auths = [re.sub('#.*$|\n', '', line) for line in open( pgpass, r'r') if not re.match('#.*', line.strip())]
                auths = [line.replace('*', '.*') for line in auths]   #pgpass *'s are converted to .*'s
            except Exception as e:
                print e
                pass
            for auth in auths:
                auth_parts = auth.split(':')    #host:port:database:user:pass
                if re.match(auth_parts[0], host) and re.match(auth_parts[1], port) and re.match(auth_parts[2], database):
                    username = username or auth_parts[3]
                    password = password or auth_parts[4]
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.connection = None

    def try_connect(self):
        try:
            self.connection = psycopg2.connect(host=self.host, port=self.port, dbname=self.database, user=self.username, password=self.password)
            self.connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            return True
        except Exception as e:
            print e
            return False

    def __exit__(self):
        if self.connection:
            self.connection.close()


class DBCursor():
    def __init__(self, dbconnection):
        self.dbconnection = dbconnection
        self.cursor = dbconnection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.columns = None

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            columns = [desc[0] for desc in cur.description]
            return True
        except Exception as e:
            print e
        return False

    def __exit__(self):
        self.cursor.close()
