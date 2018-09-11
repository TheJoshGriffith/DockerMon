import database
import monitor
import webserver
import configparser
import cherrypy
import os
import argparse

parser = argparse.ArgumentParser(description='DockerMon performance metric tool')
parser.add_argument('--config', metavar='c', help='Specify configuration file', default='config.ini')
parser.add_argument('--database', metavar='d', help='Specify a database file to use')
parser.add_argument('--host', metavar='h', help='Specify a host to monitor')
args = parser.parse_args()

if os.path.exists(args.config) and os.path.isfile(args.config):
    cfg = configparser.ConfigParser()
    cfg.read("config.ini")
    dbw = database.Database(dbname=cfg.get("General", "DatabaseFileName"))
    monitor = monitor.Monitor(cfg.get("Polling", "DockerHost"), dbw)
else:
    if args.database is not None and args.database is not "":
        dbfilename = args.database
    else:
        dbfilename = "db.sqlite3"
    if args.host is not None and args.host is not "":
        dhost = args.host
    else:
        dhost = ''.join(['http://', os.environ.get('DOCKER_HOST'), ':2375'])

dbw = database.Database(dbname=dbfilename)
monitor = monitor.Monitor(dhost, dbw)
cherrypy.server.socket_host = '0.0.0.0'
staticdir = dir_path = os.path.dirname(os.path.realpath(__file__)) + '/DockerMon/static'

monitor.start()

cherrypy.quickstart(webserver.WebServer(dbfilename),config={
    '/': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': staticdir
    }
})

cherrypy.quickstart(webserver.APIServer(dbfilename),config={
    '/': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': staticdir
    }
})
