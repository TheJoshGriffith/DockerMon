import database
import monitor
import webserver
import configparser
import cherrypy
import os
import argparse
import logging

_LOG_LEVEL_STRINGS = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']


def _log_level_string_to_int(log_level_string):
    if not log_level_string in _LOG_LEVEL_STRINGS:
        message = 'invalid choice: {0} (choose from {1})'.format(log_level_string, _LOG_LEVEL_STRINGS)
        raise argparse.ArgumentTypeError(message)

    log_level_int = getattr(logging, log_level_string, logging.INFO)
    # check the logging log_level_choices have not changed from our expected values
    assert isinstance(log_level_int, int)

    return log_level_int


parser = argparse.ArgumentParser(description='DockerMon performance metric tool')
parser.add_argument('--config', metavar='c', help='Specify configuration file', default='config.ini')
parser.add_argument('--database', metavar='d', help='Specify a database file to use')
parser.add_argument('--host', metavar='h', help='Specify a host to monitor')
parser.add_argument('--log-level', default='WARNING', dest='log_level', type=_log_level_string_to_int, nargs='?',
                    help='Set the logging output level. {0}'.format(_LOG_LEVEL_STRINGS))
args = parser.parse_args()

if os.path.exists(args.config) and os.path.isfile(args.config):
    cfg = configparser.ConfigParser()
    cfg.read("config.ini")
    dbfilename = dbname=cfg.get("General", "DatabaseFileName")
    dbw = database.Database(dbname=cfg.get("General", "DatabaseFileName"))
    dhost = cfg.get("Polling", "DockerHost")
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

if args.log_level is not None and args.log_level is not "":
    logging.basicConfig(level=args.log_level)

dbw = database.Database(dbname=dbfilename)
monitor = monitor.Monitor(dhost, dbw)
cherrypy.server.socket_host = '0.0.0.0'
staticdir = dir_path = os.path.dirname(os.path.realpath(__file__)) + '/DockerMon/static'

monitor.start()

cherrypy.quickstart(webserver.WebServer(dbfilename), config={
    '/': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': staticdir
    }
})

cherrypy.quickstart(webserver.APIServer(dbfilename), config={
    '/': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': staticdir
    }
})
