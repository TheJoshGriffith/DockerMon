import database
import monitor
import webserver
import configparser
import cherrypy


cfg = configparser.ConfigParser()
cfg.read("config.ini")

dbw = database.Database(dbname=cfg.get("General", "DatabaseFileName"))
monitor = monitor.Monitor(cfg.get("Polling", "DockerHost"), dbw)

monitor.start()
cherrypy.server.socket_host = '0.0.0.0'
cherrypy.quickstart(webserver.APIServer(cfg.get("General", "DatabaseFileName")))
