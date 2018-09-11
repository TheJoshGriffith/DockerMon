import cherrypy, database, json
from jinja2 import Environment, PackageLoader


class APIServer:
    def __init__(self, database_name):
        self.db = database.Database(database_name)

    @cherrypy.expose
    def index(self):
        return "Hello"

    @cherrypy.expose
    def get_container_stats(self, hash):
        stats = self.db.get_container_metrics(hash)
        print(stats)
        data = {}
        for row in stats:
            data[row[4]] = row[0], row[1], row[2], row[3]
        return json.dumps(data)

    @cherrypy.expose
    def get_stats(self, start, end):
        stats_out = {}
        stats = self.db.get_stats(start, end)
        for row in stats:
            stats_out[row[2]] = row[1]
        return json.dumps(stats_out)

    @cherrypy.expose
    def get_all_latest(self):
        stats_out = {}
        stats = self.db.get_all()
        for row in stats:
            stats_out[row[2]] = row
        return json.dumps(stats_out)

    @cherrypy.expose
    def get_all(self):
        return str(self.db.get_all())

    @cherrypy.expose
    def get_containers(self):
        containers_out = {}
        containers = self.db.get_containers()
        for container in containers:
            containers_out[container[1]] = container[0]
        return json.dumps(containers_out)

class WebServer(object):
    def __init__(self, database_name):
        super().__init__()
        self.db = database.Database(database_name)
        self.env = Environment(loader=PackageLoader('DockerMon', 'templates'))
        apiserver = APIServer(database_name=database_name)
        cherrypy.tree.mount(apiserver, '/api/',
                            {
                                '/api/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
                            }
                        )

    @cherrypy.expose
    def index(self):
        containers = self.db.get_containers()
        conts = []
        for container in containers:
            cont = {}
            cont["name"] = (container[1][:75] + '...') if len(container[1]) > 30 else container[1]
            cont["hash"] = container[0]
            conts.append(cont)
        return self.env.get_template('index.html').render(containers=conts)