
class User(object):
    def __init__(self, FBsecret_code = None, FBaccessToken = None, name = None, id = None, bulbs = [], graph = None):
        self.name = name
        self.id = id
        self.FBsecret_code = FBsecret_code
        self.FBaccess_token = FBaccessToken
        self.bulbs = bulbs
        self.graph_api = graph

    def __unicode__(self):
        return unicode("Name: " + unicode(self.first_name) + " " + unicode(self.last_name) + \
                       " id: " + self.id )

    def __repr__(self):
        return self.__unicode__().encode('utf-8')

    def populate(self,bulbs = None):
        self.name = self.name or self.graph_api.get_object('/me')['name']
        self.id = self.id or self.graph_api.get_object('/me')['id']
        self.bulbs = bulbs or self.bulbs