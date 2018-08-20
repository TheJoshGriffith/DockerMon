import database
import monitor
import webserver
import configparser
import cherrypy
import os


cfg = configparser.ConfigParser()
cfg.read("config.ini")

dbw = database.Database(dbname=cfg.get("General", "DatabaseFileName"))
monitor = monitor.Monitor(cfg.get("Polling", "DockerHost"), dbw)

monitor.start()
cherrypy.server.socket_host = '0.0.0.0'
staticdir = dir_path = os.path.dirname(os.path.realpath(__file__)) + '/DockerMon/static'
cherrypy.quickstart(webserver.WebServer(cfg.get("General", "DatabaseFileName")),config={
    '/': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': staticdir
    }
})

cherrypy.quickstart(webserver.APIServer(cfg.get("General", "DatabaseFileName")),config={
    '/': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': staticdir
    }
})
