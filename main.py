import database
import monitor
import webserver
import configparser
import cherrypy
import argparse
import os


parser = argparse.ArgumentParser(description='DockerMon performance metric tool')
parser.add_argument('--config', metavar='c', help='Specify configuration file', default='config.ini')
parser.add_argument('--database', metavar='d', help='Specify a database file to use')
parser.add_argument('--host', metavar='h', help='Specify a host to monitor')
args = parser.parse_args()

if os.path.exists(args.config) and os.path.isfile(args.config):
    cfg = configparser.ConfigParser()
    cfg.read(args.config)
    dbfilename = cfg.get("General", "DatabaseFileName")
    dhost = cfg.get("General", "DockerHost")
else:
    if args.database is not None and args.database is not "":
        dbfilename = args.database
    else:
        dbfilename = 'db.sqlite3'
    if args.host is not None:
        dhost = args.host
    else:
        dhost = ''.join(['http://', os.environ.get('DOCKER_HOST'), ':2375'])

print(''.join(['Database file: ', dbfilename]))
print(''.join(['Docker host  : ', dhost]))

dbw = database.Database(dbname=dbfilename)
monitor = monitor.Monitor(dhost, dbw)

monitor.start()
cherrypy.server.socket_host = '0.0.0.0'
cherrypy.quickstart(webserver.APIServer(dbfilename))
