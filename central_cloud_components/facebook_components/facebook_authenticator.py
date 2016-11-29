
import urllib
import warnings
import webbrowser
import urlparse
import os

FB_CLIENT_ID = '328783980833383'
FB_CLIENT_SECRETS = 'e1f22facec652adbe102f7e1fa6e96f1'
REDIRECT_URI = 'https://pious-brothers.000webhostapp.com/'
FACEBOOK_GRAPH_URL = 'https://graph.facebook.com'

class FBOAuth(object):
    """
    Handles the OAuth phases of Facebook and creates a txt file with an authentication token, to be used for
    using the Facebook API.
    """

    def __init__(self, filename='user_token'):
        self.filename = filename
        self.AUTHENTICATION_CODE = ''
        self.ACCESS_TOKEN = ''

    def output_to_file(self,token):
        try:
            f = open(self.filename + '.txt', 'w')
            f.write(token)
            f.close()
            print 'Authentication token was saved into the file: %s.txt' % self.filename
        except:
            print 'Not able to open/write to the file.'


    def get_auth_code(self):
        ''' Fetches the authentication code in order to receive the token '''
        warnings.filterwarnings('ignore', category=DeprecationWarning)
        savout = os.dup(1)
        os.close(1)
        os.open(os.devnull, os.O_RDWR)
        try:
            webbrowser.open(FACEBOOK_GRAPH_URL + '/oauth/authorize?' + urllib.urlencode(
                {'client_id': FB_CLIENT_ID,
                 'redirect_uri': REDIRECT_URI,
                 'scope': 'user_friends, user_status, user_posts, publish_actions, public_profile'}))
        finally:
            os.dup2(savout, 1)

        self.AUTHENTICATION_CODE = raw_input("Authentication Code: ")
        return self.AUTHENTICATION_CODE


    def authenticate_user(self):
        ''' Retrieves the authentication token and saves it into a file. '''
        if not self.AUTHENTICATION_CODE:
            self.AUTHENTICATION_CODE = self.get_auth_code()

        args = {'redirect_uri': REDIRECT_URI,
                'client_id': FB_CLIENT_ID,
                'client_secret': FB_CLIENT_SECRETS,
                'code': self.AUTHENTICATION_CODE, }

        access_token = urllib.urlopen(
            FACEBOOK_GRAPH_URL + "/oauth/access_token?" + urllib.urlencode(args)).read()
        access_token = urlparse.parse_qs(access_token)
        self.ACCESS_TOKEN = access_token['access_token'][0]
        self.output_to_file(self.ACCESS_TOKEN)
        return



if __name__ =="__main__":
    username = raw_input("Enter your name: ")
    FBOAuth(username).authenticate_user()

