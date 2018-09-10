import sqlite3
from datetime import datetime
import monitor


class Database:
    def __init__(self, dbname):
        self.dbname = dbname
        self.db = sqlite3.connect(self.dbname)
        self.database_setup()

    # Standard SQL crap
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

    # Stuff for this application
    def database_setup(self):
        self.sql_edit("CREATE TABLE IF NOT EXISTS containers(id TEXT PRIMARY KEY, name TEXT);")
        self.sql_edit("CREATE TABLE IF NOT EXISTS metrics(id INTEGER PRIMARY KEY AUTOINCREMENT, container_id TEXT, name TEXT, cpu INT, mem INT, nrx INT, ntx INT, datetime TIMESTAMP, FOREIGN KEY(container_id) REFERENCES containers(id));")

    def container_exists(self, hash):
        self.db = sqlite3.connect(self.dbname)
        cursor = self.get_cursor()
        cursor.execute("SELECT COUNT(*) FROM containers WHERE id IS \"%s\"" % (hash,))
        return cursor.fetchone()[0] >= 1

    def get_stats(self, start, end):
        return self.sql_get("SELECT * FROM metrics WHERE datetime > %s AND datetime < %s" % (start, end,))

    def get_all(self):
        return self.sql_get("SELECT * FROM metrics;")

    def add_container(self, container_name, hash):
        self.sql_edit("INSERT INTO containers(id, name) values(\"%s\", \"%s\");" % (hash, container_name,))

    def get_containers(self):
        return self.sql_get("SELECT * FROM containers;")

    def add_metric(self, hash, stats):
        self.sql_edit("INSERT INTO metrics(container_id, name, cpu, mem, nrx, ntx, datetime) values(\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\");" % (hash, stats.name, stats.cpu, stats.mem, stats.nrx, stats.ntx, datetime.now()))

    def get_metrics(self, starttime, endtime, hash):
        return self.sql_get("SELECT * FROM metrics WHERE container_id is %s AND datetime > %s AND datetime < \"%s\"" % (hash, starttime, endtime,))

    def get_container_metrics(self, hash):
        return self.sql_get("SELECT cpu, mem, nrx, ntx, datetime FROM metrics WHERE container_id IS \"%s\" LIMIT 10" % (hash,))
