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
	dbfilename = args.database
	dhost = args.host

dbw = database.Database(dbname=dbfilename)
monitor = monitor.Monitor(dhost, dbw)

monitor.start()
cherrypy.quickstart(webserver.APIServer(dbfilename))
