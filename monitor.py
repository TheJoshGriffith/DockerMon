import threading, time, requests, json, logging
from sys import platform


class stats_metric:
    def __init__(self, name, cpu, mem, nrx, ntx):
        self.name = name
        self.cpu = cpu
        self.mem = mem
        self.nrx = nrx
        self.ntx = ntx


class Monitor(threading.Thread):
    def __init__(self, host, db):
        threading.Thread.__init__(self)
        self.host = host
        self.db = db

    def api_path(self, *args):
        path = '/'.join(args)
        return ''.join([self.host, '/', path])

    def extract_stats(self, stat_string):
        name = stat_string['name']
        cpu = stat_string['cpu_stats']['cpu_usage']['total_usage']
        if platform == 'win32':
            mem = stat_string['memory_stats']['commitbytes']
        else:
            mem = stat_string['memory_stats']['usage']
        nrx = stat_string['networks']['eth0']['rx_bytes'] if 'networks' in stat_string and 'eth0' in stat_string['networks'] else 0
        ntx = stat_string['networks']['eth0']['tx_bytes'] if 'networks' in stat_string and 'eth0' in stat_string['networks'] else 0
        return stats_metric(name, cpu, mem, nrx, ntx)

    def get_stats(self, hash):
        body = { "stream":False }
        res = requests.get(self.api_path("containers", hash, "stats"), params=body)
        if res.status_code == 200:
            jstats = json.loads(res.content.decode('utf-8'))
            name = jstats['name']
            cpu = jstats['cpu_stats']['cpu_usage']['total_usage']
            mem = jstats['memory_stats']['usage']
            nrx = jstats['networks']['eth0']['rx_bytes'] if 'networks' in jstats and 'eth0' in jstats['networks'] else 0
            ntx = jstats['networks']['eth0']['tx_bytes'] if 'networks' in jstats and 'eth0' in jstats['networks'] else 0
            return self.extract_stats(json.loads(res.content.decode('utf-8')))
        else:
            print("Web request error, check your path, yo")

            # Fields to extract:
            # name
            # cpu_stats/cpu_usage/total_usage
            # memory_stats/usage
            # networks/eth0/rx_bytes
            # networks/eth0/tx_bytes

    def get_containers(self):
        res = requests.get(self.api_path("containers", "json"))
        if res.status_code == 200:
            return json.loads(res.content.decode('utf-8'))
        else:
            print("Web request error, check your path, yo")

    def get_container_list(self):
        container_list = {}
        for container in self.get_containers():
            container_list[container['Id']] = container
        for k,p in container_list.items():
            if not self.db.container_exists(p['Id']):
                self.db.add_container(container_name=p['Names'][0].lstrip('/'), hash=k)
        return container_list

    def run(self):
        while True:
            container_list = self.get_container_list()
            logging.debug(str(container_list))
            for k,p in container_list.items():
                logging.debug(k)
                logging.debug(p)
                logging.debug(self.get_stats(k))
                self.db.add_metric(k, self.get_stats(k))
            time.sleep(5)
