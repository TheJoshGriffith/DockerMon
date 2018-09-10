#!/usr/bin/env bash
echo $DOCKER_HOST

sleep 50000000

python3 main.py --database db.sqlite3 --host http://host.docker.internal:2375