import requests
import base64
import json
import logging
import time



logging.basicConfig(filename='o365.log',level=logging.DEBUG)

log = logging.getLogger(__name__)

class Task(object):

    def __init__(self, json=None, auth=None):
        if json:
            self.json = json

        else:
            self.json = {'Task':{'Body':{}}}


        self.auth = auth

    def getCreatedTime(self):
        return self.json['CreatedDateTime']

    def getOwner(self):
        return self.json['Owner']

    def getSubject(self):
        return self.json['Subject']
