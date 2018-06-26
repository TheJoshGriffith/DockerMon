FROM ubuntu
MAINTAINER Josh Griffith

RUN apt-get install -y python python-software-properties git
RUN git clone https://github.com/XtrmJosh/DockerMon.git
RUN pip install -r DockerMon/requirements.txt

EXPOSE 8080

ENTRYPOINT python DockerMon/main.py
