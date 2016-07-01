import requests
import base64
import json
import logging
import time



logging.basicConfig(filename='o365.log',level=logging.DEBUG)

log = logging.getLogger(__name__)

class Task(object):
    time_string = '%Y-%m-%dT%H:%M:%SZ'
    #takes a calendar ID
    create_url = 'https://outlook.office365.com/api/beta/me/tasks'
    #takes current event ID
    update_url = "https://outlook.office365.com/api/beta/me/tasks('%s')"
    #takes current event ID
    delete_url = "https://outlook.office365.com/api/beta/me/tasks('%s')"

    def __init__(self, json=None, auth=None):
        if json:
            self.json = json

        else:
            self.json = { 'Body':{}}


        self.auth = auth

    def getCreatedTime(self):
        return self.json['CreatedDateTime']

    def getDueDate(self):
        res = None
        if self.json['DueDateTime'] and self.json['DueDateTime']['DateTime']:
            res = self.json['DueDateTime']['DateTime']
        return res

    def getReminderDateTime(self):
        res = None
        if self.json['ReminderDateTime'] and self.json['ReminderDateTime']['DateTime']:
            res = self.json['ReminderDateTime']['DateTime']
        return res

    def getId(self):
        return self.json['Id']

    def getOwner(self):
        return self.json['Owner']

    def getSubject(self):
        return self.json['Subject'].encode('utf-8')

    def getBody(self):
        return self.json['Body']['Content'].encode('utf-8')

    def setBody(self, val):
        self.json['Body'] = {'Content' : val,"ContentType":"HTML"}

    def setSubject(self, val):
        self.json['Subject']=  val

    def setDueDate(self, val, TZ="UTC"):
        if isinstance(val, time.struct_time):
            self.json['DueDateTime'] = {"DateTime":time.strftime(self.time_string, val), "TimeZone":TZ}
        elif isinstance(val, int):
            self.json['DueDateTime'] = {"DateTime":time.strftime(self.time_string, time.gmtime(val)), "TimeZone":TZ}
        elif isinstance(val, float):
            self.json['DueDateTime'] = {"DateTime":time.strftime(self.time_string, time.gmtime(val)), "TimeZone":TZ}
        else:
            # this last one assumes you know how to format the time string. if it brakes, check
            # your time string!
            self.json['DueDateTime'] = {"DateTime":val, "TimeZone":TZ}


    def getTask(self, task_id):
        log.debug('fetching task %s .' % task_id)
        response = requests.get("%s('%s')" % (self.create_url, task_id), auth=self.auth)
        log.info('Response from O365: %s', str(response))

        return Task(response.json(),self.auth)

    def delete(self):
        '''
        Delete's an event from the calendar it is in.

        But leaves you this handle. You could then change the calendar and transfer the event to
        that new calendar. You know, if that's your thing.
        '''
        if not self.auth:
            return False

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        response = None
        try:
            log.warning('sending delete request')
            response = requests.delete(self.delete_url % (self.json['Id']),headers=headers,auth=self.auth)
            print "delte ", response

        except Exception as e:
            if response:
                log.warning('response to deletion: %s',str(response))
            else:
                log.error('No response, something is very wrong with delete: %s',str(e))
            return False

        return response

    def create(self):
        if not self.auth:
            log.debug('failed authentication check when creating event.')
            return False


        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

        log.debug('creating json for request.')
        data = json.dumps(self.json)

        response = None
        try:
            log.debug('sending post request now')
            response = requests.post(self.create_url , data, headers=headers, auth=self.auth)
            log.debug('sent post request.')
        except Exception as e:
            if response:
                log.debug('response to event creation: %s', str(response))
            else:
                log.error('No response, something is very wrong with create: %s', str(e))
            return False

        log.debug('response to event creation: %s', str(response))
        return Task(response.json(), self.auth)


    def update(self, task_id):
        if not self.auth:
            log.debug('failed authentication check when creating event.')
            return False


        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

        log.debug('creating json for request.')
        data = json.dumps(self.json)

        response = None
        try:
            log.info('sending post request now')
            log.info(self.update_url % (task_id))
            log.info(data)
            response = requests.patch(self.update_url % (task_id) , data, headers=headers, auth=self.auth)
            log.info('response to Task creation: %s', str(response))
            log.info('sent post request.')
        except Exception as e:
            if response:
                log.info('response to event creation: %s', str(response))
            else:
                log.info('No response, something is very wrong with create: %s', str(e))
            return False

        log.debug('response to event creation: %s', str(response))
        return Task(response.json(), self.auth)