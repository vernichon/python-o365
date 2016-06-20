from O365.contact import Contact
import logging
import json
import requests
from folder import Folder

logging.basicConfig(filename='o365.log',level=logging.DEBUG)

log = logging.getLogger(__name__)


class Folders( object ):
    '''
    A wrapper class that handles all the contacts associated with a single Office365 account.

    Methods:
        constructor -- takes your email and password for authentication.
        getFolders -- download Folders Name.

    Variables:

        folder_url -- the url that is used for finding folders .
    '''

    folders_url = 'https://outlook.office365.com/api/v1.0/me/folders'

    def __init__(self, auth, folderName=None):
        '''
        Creates a group class for managing all contacts associated with email+password.

        Optional: folderName -- send the name of a contacts folder and the search will limit
        it'self to only those which are in that folder.
        '''
        log.debug('setting up for the folder %s',auth[0])
        self.auth = auth
        self.folders = []



    def getFolders(self):
        '''Begin the process of downloading contact metadata.'''

        log.debug('fetching contacts.')
        response = requests.get(self.folders_url,auth=self.auth)
        log.info('Response from O365: %s', str(response))


        for folder in response.json()['value']:
            duplicate = False
            log.debug('Got a folder Named: {0}'.format(folder['DisplayName'].encode('utf-8')))
            for existing in self.folders:
                if existing.json['Id'] == folder['Id']:
                    log.info('duplicate contact')
                    duplicate = True
                    break

            if not duplicate:
                self.folders.append(Folder(folder,self.auth))

            log.debug('Appended folder.')


        log.debug('all folder name retrieved and put in to the list.')
        return True

#To the King!
