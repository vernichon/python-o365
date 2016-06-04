import requests
import base64
import json
import logging
import time

from O365.task import Task

logging.basicConfig(filename='o365.log',level=logging.DEBUG)

log = logging.getLogger(__name__)



class Tasks( object ):
    '''
    Task manages lists of Tasks on an associated Task on office365.

    Methods:
        getName - Returns the name of the Task.
        getTaskId - returns the GUID that identifies the Task on office365
        getId - synonym of getTaskId
        getTasks - kicks off the process of fetching Tasks.
        fetchTasks - legacy duplicate of getTasks

    Variable:
        Tasks_url - the url that is actually called to fetch Tasks. takes an ID, start, and end.
        time_string - used for converting between struct_time and json's time format.
    '''
    Tasks_url = 'https://outlook.office365.com/api/beta/me/tasks/'
    time_string = '%Y-%m-%dT%H:%M:%SZ'

    def __init__(self, json=None, auth=None):
        '''
        Wraps all the informaiton for managing Tasks.
        '''
        self.json = json
        self.auth = auth
        self.Tasks = []

        if json:
            log.debug('translating Task information into local variables.')
            self.TaskId = json['Id']
            self.name = json['Name']


    def getName(self):
        '''Get the Task's Name.'''
        return self.json['Name']

    def getTaskId(self):
        '''Get Task's GUID for office 365. mostly used interally in this library.'''
        return self.json['Id']

    def getId(self):
        '''Get Task's GUID for office 365. mostly used interally in this library.'''
        return self.getTaskId()

    def fetchTasks(self,start=None,end=None):
        '''
        So I originally made this function "fetchTasks" which was a terrible idea. Everything else
        is "getX" except Tasks which were appearenty to good for that. So this function is just a
        pass through for legacy sake.
        '''
        return self.getTasks(start,end)


    def getTasks(self,start=None,end=None):
        '''
        Pulls Tasks in for this Task. default range is today to a year now.

        Keyword Arguments:
        start -- The starting date from where you want to begin requesting Tasks. The expected
        type is a struct_time. Default is today.
        end -- The ending date to where you want to end requesting Tasks. The expected
        type is a struct_time. Default is a year from start.
        '''

        #If no start time has been supplied, it is assumed you want to start as of now.
        if not start:
            start = time.strftime(self.time_string)

        #If no end time has been supplied, it is assumed you want the end time to be a year
        #from what ever the start date was.
        if not end:
            end = time.time()
            end += 3600*24*365
            end = time.gmtime(end)
            end = time.strftime(self.time_string,end)

        #This is where the actual call to Office365 happens.
        response = requests.get(self.Tasks_url,auth=self.auth)
        log.info('Response from O365: %s', str(response))

        #This takes that response and then parses it into individual Task Tasks.
        for task in response.json()['value']:
            try:
                duplicate = False
                #checks to see if the Task is a duplicate. if it is local changes are clobbered.
                for i,e in enumerate(self.Tasks):
                    if e.json['Id'] == task['Id']:
                        self.Tasks[i] = Task(task,self.auth)
                        duplicate = True
                        break

                if not duplicate:
                    self.Tasks.append(Task(task,self.auth))

                log.debug('appended Task: %s',task['Subject'])
            except Exception as e:
                log.info('failed to append Task: %',str(e))

        log.debug('all Tasks retrieved and put in to the list.')
        return True

#To the King!
