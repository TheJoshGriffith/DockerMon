import threading, time, requests, json


class Monitor(threading.Thread):
    def __init__(self, host, db):
        threading.Thread.__init__(self)
        self.host = host
        self.db = db

    def api_path(self, *args):
        path = '/'.join(args)
        return ''.join([self.host, '/', path])

    def get_stats(self, hash):
        body = { "stream":False }
        res = requests.get(self.api_path("containers", hash, "stats"), params=body)
        if res.status_code == 200:
            return json.loads(res.content)
        else:
            print("Web request error, check your path, yo")

    def get_containers(self):
        res = requests.get(self.api_path("containers", "json"))
        if res.status_code == 200:
            return json.loads(res.content)

    def run(self):
        container_list = {}
        for container in self.get_containers():
            container_list[container['Id']] = container
        for k,p in container_list.items():
            if not self.db.container_exists(p['Id']):
                self.db.add_container(container_name=p['Names'][0].lstrip('/'), hash=k)
        while True:
            for k,p in container_list.items():
                self.db.add_metric(k, self.get_stats(k))
            time.sleep(5)