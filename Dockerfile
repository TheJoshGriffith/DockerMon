FROM ubuntu
MAINTAINER Joshua Griffith

RUN apt update
RUN apt install -y python3 python3-pip git
RUN git clone https://github.com/XtrmJosh/DockerMon.git
RUN pip3 install -r DockerMon/requirements.txt
WORKDIR DockerMon/

EXPOSE 8080

ENTRYPOINT python3 main.py --database db.sqlite3 --host http://docker.for.win.localhost:2375