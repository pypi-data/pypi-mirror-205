import os
from importlib import import_module
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
import logging
import logging.handlers
from datetime import datetime
from .app_config import AppConfig
from .executer import ExecuterCaller
from .command_reciever import CommandsReciever
from .event_reciever import Command

__version__ = '0.0.1'

#Load configuration
configure = AppConfig(os.getcwd())
configure.from_pyfile('config.py')

#Set logging
"""
fileHandler = logging.handlers.TimedRotatingFileHandler(
    filename='./log.txt', 
    when = "D" ,
    backupCount= 7 , 
    atTime=None
    )

fileHandler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
                              "%Y-%m-%d %H:%M:%S")
fileHandler.setFormatter(formatter)
logging.basicConfig(handlers=[fileHandler])
"""

#Get flask handle
app = Flask(__name__)

#enable CORS for all routes 
CORS(app)

#REST API
api = Api(app, prefix="/api/v1")
api.add_resource(Command, '/command')

#local database
if not configure.get('SQLALCHEMY_DATABASE_URI'):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    configure['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'app.db')

app.config ['SQLALCHEMY_DATABASE_URI'] = configure['SQLALCHEMY_DATABASE_URI']

db = SQLAlchemy(app)

#Job Scheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

#Executer
executer = ExecuterCaller.instance(configure)

#Command Reciever (Web url polling)
reciever = None
if configure.get('COMMANDER_SERVER_URL'):
    reciever = CommandsReciever(configure['COMMANDER_SERVER_URL'])

#Table creation
from . import models
if configure.get('CUSTOM_MODELS_PATH'):
    mdl = import_module(configure['CUSTOM_MODELS_PATH'])
    cls_objs = [x for x in mdl.__dict__ if not x.startswith("_")]
    globals().update({k: getattr(mdl, k) for k in cls_objs})

with app.app_context():
    db.create_all()

#Start scheduled jobs
if configure.get('SCHEDULED_JOBS'):
    from .job_reciever import ScheduledJob
    ScheduledJob(configure['SCHEDULED_JOBS'])
