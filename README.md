# DockerMon
A Docker container performance monitoring tool.

# What?
DockerMon is a tool to track the resource consumption of Docker containers over time.
By default, the Docker API only exposes metrics instantly, which is only really useful
during forensic examination or diagnosis of runtime issues. This tool is designed to be
used during the development lifecycle of products, to track performance metrics and 
provide critical feedback about performance bottlenecks.

# Why?
This project was started by Josh Griffith after finding that the majority of tools 
which do a similar job have severe limitations. Typically, they either exclude critical
data from the endpoint or simply don't run cross platform. Docker is a cross platform
tool, and provides a host of useful information. The intention of this tool is to make
full use of those facts.

# How?
The tool is very simple. It polls `docker stats` regularly to extract metrics, then 
stores them in a database. A CherryPy server then serves these metrics via a RESTful
API. Currently the API is limited in scope, but it intends to eventually serve data 
from time ranges (e.g start/end time), from time history (e.g seconds ago), or from
any other reasonable time period. It's all pretty simple in that sense.

# I'm sold, how do I use it?
Just pip install -r the requirements, copy config.ini.sample and edit it to your own
configuration, then run `python ./main.py` and hit the endpoint. By default it runs on
port 8080.