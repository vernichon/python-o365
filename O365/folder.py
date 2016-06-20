from O365.contact import Contact
import logging
import json
import requests

logging.basicConfig(filename='o365.log',level=logging.DEBUG)

log = logging.getLogger(__name__)

class Folder( object ):
    '''
    Folder  manages lists

    '''


    def __init__(self, json=None, auth=None):
        '''
        Wraps all the informaiton for managing contacts.
        '''
        self.json = json
        self.auth = auth

        if json:
            log.debug('translating contact information into local variables.')
            self.folderId = json['Id']
            self.name = json['DisplayName']
            self.TotalItemCount = json['TotalItemCount']
        else:
            log.debug('there was no json, putting in some dumby info.')
            self.json = {'DisplayName':'Jebediah Kerman'}

