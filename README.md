# MLAB framework
![alt text](var/asserts/Mlab-Logo.png)
## Overview
Mlab is a framework tool designed for managing machine learning models in a production environment. This framework enables the developers to upload new machine learning models through a api-rest or in a manually way using the mlab dashboard. This lets the developers create full pipelines of training and release machine learning model . When a model is released in mlab architecture, we are able to active or deactive the model in a specific host in this way mlab allows us to create A/B test for the models. Once a model is released in a host, this can be consumed by the business applications through a web service.
Full documentation about web service is deployed by swagger as static documentation.

![alt text](var/asserts/Mlab-UseCasePipeline.png)

## Table of content
[TOC]

## Getting started
Is pretty simple, mlab have 2 main components, the workers and the orchestator/dashboard. One worker instance is as simple as webservice, who main goal is load machine learning models in memory and keep the sincronization with the orchestator. The orchestrator is in charge of controlling the workers machine learning algorithm loaded trough the dashboard or their REST-API.
## Architecture
![alt text](var/asserts/Mlab-Architecture.png)

## Requirements
```
sudo apt-get install -y python3-pip virtualenvwrapper  python3
```
## Dashboard Orchestrator

### Install
```
mkvirtualenv --python=/usr/bin/python mlab_dashboard_env
cd dashboard
#As mlab_dashboard_env virtual environment activated in the terminal session.
pip install .
```
### Usage

To run the server, please execute the following using mlab_dashboard_env.  
```
gunicorn -w 2 -b 0.0.0.0:5000 dashboard.app:app
```

Now we can open the dashboard, in the uri: http://localhost:5000/dashboard

## Worker

### Install
```
mkvirtualenv --python=/usr/bin/python mlab_worker_env
cd worker
#As mlab_worker_env virtual environment activated in the terminal session.
pip install .
```
### Usage

To run the server, please execute the following using mlab_dashboard_env.  
```
gunicorn -b 0.0.0.0:9090 -w 4 --config=python:worker.application.conf.gunicorn_conf worker.app:app
```

Now we can open the dashboard, in the uri: http://localhost:5000/dashboard

## Running with Docker

To run the server on a Docker container, please execute the following from the root directory:

```bash
# run docker-compose
docker-compose up --build
```