import cherrypy, database


class APIServer(object):
    def __init__(self, database_name):
        super().__init__()
        self.db = database.Database(database_name)

    @cherrypy.expose
    def index(self):
        return "Hello"

    @cherrypy.expose
    def get_stats(self, start, end):
        return self.db.get_stats(start, end)

    @cherrypy.expose
    def get_all(self):
        stats_out = {}
        stats = self.db.get_all()
        for row in stats:
            stats_out[row[2]] = row[1]
        return stats_out