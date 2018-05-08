import cherrypy, database, json


class APIServer(object):
    def __init__(self, database_name):
        super().__init__()
        self.db = database.Database(database_name)

    @cherrypy.expose
    def index(self):
        return "Hello"

    @cherrypy.expose
    def get_stats(self, start, end):
        stats_out = {}
        stats = self.db.get_stats(start, end)
        for row in stats:
            stats_out[row[2]] = row[1]
        return json.dumps(stats_out)

    @cherrypy.expose
    def get_all(self):
        stats_out = {}
        stats = self.db.get_all()
        for row in stats:
            stats_out[row[2]] = row[1]
        return json.dumps(stats_out)

    @cherrypy.expose
    def get_containers(self):
        containers_out = {}
        containers = self.db.get_containers()
        for container in containers:
            containers_out[container[1]] = container[0]
        return json.dumps(containers_out)