import facebook
import urllib
import warnings
import webbrowser
import dbmanager
import urlparse
import settings
import os
from user import User
from twython import Twython



#class TwOAuth(object):


class FBOAuth(object):
    """
    Handles the OAuth phases of Facebook and returns an authenticated GrapApi object, to be used for
    using the Facebook API.
    """
    FACEBOOK_GRAPH_URL = settings.FACEBOOK_GRAPH_URL
    CLIENT_ID = settings.FB_CLIENT_ID
    CLIENT_SECRET = settings.FB_CLIENT_SECRETS
    REDIRECT_URI = settings.REDIRECT_URI

    SECRET_CODE = None
    ACCESS_TOKEN = None

    def __init__(self):
        self.database = dbmanager.DBManager()
        FBOAuth.SECRET_CODE = self.get_secret_code()
        FBOAuth.ACCESS_TOKEN = self.get_access_token()

    def get_secret_code(self):
        try:
            return  self.database.get('USER').secret_code
        except AttributeError:
            return None #self.database.get('SECRET_CODE') or

    def save_secret_code(self, secret_code):
        self.database.save('SECRET_CODE', secret_code)

    def get_access_token(self):
        try:
            return self.database.get('USER').access_token
        except AttributeError:
            return None #self.database.get('ACCESS_TOKEN') or

    def save_access_token(self, access_token):
        self.database.save('ACCESS_TOKEN', access_token)

    def authorize(self):

        warnings.filterwarnings('ignore', category=DeprecationWarning)
        savout = os.dup(1)
        os.close(1)
        os.open(os.devnull, os.O_RDWR)
        try:
            webbrowser.open(FBOAuth.FACEBOOK_GRAPH_URL + '/oauth/authorize?' + urllib.urlencode(
                {'client_id': FBOAuth.CLIENT_ID,
                 'redirect_uri': FBOAuth.REDIRECT_URI,
                 'scope': 'user_friends, user_status, user_posts, publish_actions, public_profile'}))
        finally:
            os.dup2(savout, 1)

        FBOAuth.SECRET_CODE = raw_input("Secret Code: ")
        user = User(FBsecret_code= FBOAuth.SECRET_CODE)
        self.database.save('USER', user)

        return FBOAuth.SECRET_CODE

    def authenticate_user(self):

        if not FBOAuth.SECRET_CODE:
            FBOAuth.SECRET_CODE = self.authorize()

        args = {'redirect_uri': FBOAuth.REDIRECT_URI,
                'client_id': FBOAuth.CLIENT_ID,
                'client_secret': FBOAuth.CLIENT_SECRET,
                'code': FBOAuth.SECRET_CODE, }

        access_token = urllib.urlopen(
            FBOAuth.FACEBOOK_GRAPH_URL + "/oauth/access_token?" + urllib.urlencode(args)).read()
        access_token = urlparse.parse_qs(access_token)
        FBOAuth.ACCESS_TOKEN = access_token['access_token'][0]
        #self.save_access_token(FBOAuth.ACCESS_TOKEN)
        user = self.database.get('USER')
        user.FBaccess_token = FBOAuth.ACCESS_TOKEN
        user.graph_api = facebook.GraphAPI(FBOAuth.ACCESS_TOKEN)
        user.populate()
        self.database.save('USER', user)
        return user

    def get_graph_api(self):

        if not FBOAuth.ACCESS_TOKEN:
            self.authenticate_user()

        return facebook.GraphAPI(FBOAuth.ACCESS_TOKEN)

    def invalidate_login(self):
        self.save_access_token(None)
        self.save_secret_code(None)
        exit(0)

