import database
import monitor
import webserver
import configparser
import cherrypy


cfg = configparser.ConfigParser()
cfg.read("config.ini")

dbw = database.Database(dbname=cfg.get("General", "DatabaseFileName"))
monitor = monitor.Monitor(cfg.get("General", "DockerHost"), dbw)

monitor.start()
cherrypy.quickstart(webserver.APIServer(cfg.get("General", "DatabaseFileName")))