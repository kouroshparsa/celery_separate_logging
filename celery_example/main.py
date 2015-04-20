from __future__ import absolute_import
import json
import os
import logging
import time
import tempfile
from celery import Celery
from celery.signals import after_setup_task_logger

class myFileHandler(logging.FileHandler):

    def __init__(self, logfile, mode):
        self.logfile = logfile
        super(myFileHandler,self).__init__(self.logfile,mode)

    def getlogfile(self):
        return self.logfile


celery = Celery()
celery.config_from_object('celeryconfig')


# Return a filename of the form imagebuild_.log
def getfilename():
    time_now = str(time.time()).split('.')
    logfile = tempfile.gettempdir() + '/imagebuild_{0:s}.log'.format(time_now[0]+time_now[1])
    return logfile


@after_setup_task_logger.connect
def augment_celery_log(**kwargs):
    logger = logging.getLogger('imagebuilder')
    logfile = getfilename()
    handler = myFileHandler(logfile,'w')
    formatter = logging.Formatter('%(asctime)s - %(message)s')

    if not logger.handlers:
        formatter = logging.Formatter(logging.BASIC_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = 0

        logger.setLevel(logging.DEBUG)


import mylib.fire as fire

@celery.task
def build(buildconfig, kickstart):

    logger = logging.getLogger('imagebuilder')
    logfile = getfilename()
    handler = myFileHandler(logfile,'w')
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)

    # replace the handler
    logger.handlers[0] = handler
    logger.info("this is a task %s" % kickstart)
    #import dna.aligner as aligner
    fire.burn(">>>> %s" % kickstart)
