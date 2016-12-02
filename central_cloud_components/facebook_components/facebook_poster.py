import facebook
import logging
from time import *

# Class to post a status on user's Facebook wall given their token
class FBPoster(object):

    def __init__(self,token = None):
        self.user_token = token

    def post(self,text):
        ''' Posts 'text' as a status on user's Facebook wall. '''
        graph = facebook.GraphAPI(access_token=self.user_token)
        try:
            graph.put_wall_post(message=text, profile_id=graph.get_object('/me')['id'])
            logging.info('Status posted: %s', text)
            print "%s: Status posted: %s', "%(strftime("%H:%M:%S", gmtime()), text)
            return True
        except Exception, e:
            logging.error('Posting unsuccessful: %s', text)
            logging.error('ERROR: %s',str(e))
            return False
        return
