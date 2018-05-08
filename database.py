import sqlite3
from datetime import datetime


class Database:
    def __init__(self, dbname):
        self.dbname = dbname
        self.db = sqlite3.connect(self.dbname)
        self.database_setup()

    def get_cursor(self):
        return self.db.cursor()

    def sql_edit(self, sql):
        self.db = sqlite3.connect(self.dbname)
        cursor = self.get_cursor()
        cursor.execute(sql)
        self.db.commit()

    def sql_get(self, sql):
        self.db = sqlite3.connect(self.dbname)
        cursor = self.get_cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def sql_count(self, sql):
        self.db = sqlite3.connect(self.dbname)
        cursor = self.get_cursor()
        cursor.execute(sql)
        return cursor.rowcount()

    def table_exists(self, table_name):
        self.db = sqlite3.connect(self.dbname)
        cursor = self.get_cursor()
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type=table AND name=\"%s\"" % (table_name,))
        return cursor.fetchone() >= 1

    def container_exists(self, hash):
        self.db = sqlite3.connect(self.dbname)
        cursor = self.get_cursor()
        cursor.execute("SELECT COUNT(*) FROM containers WHERE id IS \"%s\"" % (hash,))
        return cursor.fetchone()[0] >= 1

    def database_setup(self):
        self.sql_edit("CREATE TABLE IF NOT EXISTS containers(id TEXT PRIMARY KEY, name TEXT);")
        self.sql_edit("CREATE TABLE IF NOT EXISTS metrics(id INTEGER PRIMARY KEY AUTOINCREMENT, container_id TEXT, perfstring TEXT, datetime TIMESTAMP, FOREIGN KEY(container_id) REFERENCES containers(id));")

    def get_stats(self, start, end):
        return self.sql_get("SELECT * FROM metrics WHERE datetime > %s AND datetime < %s" % (start, end,))

    def get_all(self):
        return self.sql_get("SELECT * FROM metrics;")

    def add_container(self, container_name, hash):
        self.sql_edit("INSERT INTO containers(id, name) values(\"%s\", \"%s\");" % (hash, container_name,))

    def add_metric(self, hash, metric_string):
        self.sql_edit("INSERT INTO metrics(container_id, perfstring, datetime) values(\"%s\", \"%s\", \"%s\");" % (hash, metric_string, datetime.now()))

    def get_metrics(self, starttime, endtime, hash):
        return self.sql_get("SELECT perfstring FROM metrics WHERE hash is %s AND datetime > %s AND datetime < \"%s\"", (hash, starttime, endtime,))