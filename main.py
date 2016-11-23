
import facebook
from dbmanager import DBManager
import access
import datetime


class Bulb(object):
    def __init__(self, name, id=None, times_on=[], user_near=[]):
        self.id = id
        self.name = name
        self.times_on = times_on  # array of tuples (datetime switch_ON,datetime switch_OFF)
        self.user_near = user_near  # array of tuples (datetime user_came,datetime user_left)

    def getStats(self, days=1):
        ''' Returns a list of tuples of timedeltas
        [(timedelta that the lamp was on,timedelta that the user was nearby),(...)]'''
        i = len(self.times_on) - 1
        stats = []
        time_ago = datetime.datetime.now() - datetime.timedelta(days=days + 1)

        # while lights were switched off in the past week/day
        #   while user left the bulb after it was switched on
        #     total time at the bulb += the time user was at the bulb then
        #     if user came to the bulb before it was switched on
        #       subtract that period from the total
        j = max((len(self.user_near) - 1), 0)
        while (i >= 0 and (self.times_on[i][1] > time_ago)):
            time_near_bulb = datetime.timedelta(0)
            while (j >= 0 and (self.user_near[j][1] >= self.times_on[i][0])):
                if self.user_near[j][0] > self.times_on[i][1]:
                    j-=1
                    continue
                time_near_bulb += self.user_near[j][1] - self.user_near[j][0]
                if (self.user_near[j][0] < self.times_on[i][0]):
                    time_near_bulb -= max(self.times_on[i][0] - self.user_near[j][0], datetime.timedelta(0))
                j -= 1

            timeOn = self.times_on[i][1] - self.times_on[i][0]
            stats.append((timeOn, time_near_bulb))
            i -= 1
        return stats


class FBPostManager(object):
    def __init__(self, user, spendRate=0.8):
        self.user = user
        self.graph_api = user.graph_api
        self.postTypes = ['In the past day I left my %s lights on for %s while nobody was around.',
                          'This week I left my %s lights on at home for %s while nobody was around. '
                          'I could have saved %s of power by turning them off.']
        self.spendRate = spendRate

    def formatPost(self, weekly, bulbTimes):
        post_type = self.postTypes[1] if weekly else self.postTypes[0]
        bulbs = bulbTimes.keys()
        lights = ""
        total_wasted = 0
        total_used = 0
        for bulb in bulbs:
            lights += bulb + ", "
            for pair in bulbTimes[bulb]:
                total_wasted += (pair[0] - pair[1])
                total_used += pair[0]

        if lights:
            lights = lights[:-2]

        if int(total_wasted / 3600) == 1:
            time = '%d hour and %d minutes' % (total_wasted / 3600, (total_wasted % 3600) / 60)
        elif int(total_wasted / 3600) > 1:
            time = '%d hours and %d minutes' % (total_wasted / 3600, (total_wasted % 3600) / 60)
        else:
            time = '%d minutes' % (total_wasted / 60)

        if weekly:
            percentage = '%d%%' % ((total_wasted/total_used)*100)
            return self.postTypes[1] % (lights.lower(), time, percentage)
        else:
            return self.postTypes[0] % (lights.lower(), time)

    def post(self, weekly, bulbTimes):

        post = self.formatPost(weekly, bulbTimes)

        graph = facebook.GraphAPI(access_token=self.user.FBaccess_token)

        try:
            self.graph_api.put_wall_post(message=post, profile_id=self.user.id)
            print 'Status posted: %s' % post
            return True
        except Exception, e:
            print 'Posting unsuccessful: %s' % post
            print str(e)
            return False

    def checkBulbs(self, weekly=False):
        ''' Returns a dictionary in the form
        dict[bulb_name] = [(total seconds it was used, total seconds used while unattended),...]'''
        bulbs = self.user.bulbs
        days = 7 if weekly else 1
        post = {}
        for bulb in bulbs:
            total_used = 0
            total_attended = 0
            for pair in bulb.getStats(days):
                total_used +=pair[0].total_seconds()
                total_attended += pair[1].total_seconds()
            print total_attended / float(total_used)
            if ((total_attended / float(total_used)) < self.spendRate):

                if post.get(bulb.name, None):
                    post[bulb.name].append((total_used, total_attended))
                else:
                    post[bulb.name] = [(total_used, total_attended)]
        return post

    def checkAndPost(self, weekly=False):
        bulbTimes = self.checkBulbs(weekly)
        if bulbTimes:
            self.post(weekly, bulbTimes)

def postToFacebookDaily():

    dbmanager = DBManager()
    user = dbmanager.get('USER') or access.FBOAuth().authenticate_user()
    post_manager = FBPostManager(user=user)
    post_manager.checkAndPost(weekly=False)

def postToFacebookWeekly():

    dbmanager = DBManager()
    user = dbmanager.get('USER') or access.FBOAuth().authenticate_user()
    post_manager = FBPostManager(user=user)
    post_manager.checkAndPost(weekly=True)


if __name__ == "__main__":
    """
    graph = access.FBOAuth().get_graph_api()

    friends_manager = FriendsManager(graph)
    greeter = Greeter()

    friends_manager.greet_friends(greeter)


"""

    postToFacebookDaily()
    postToFacebookWeekly()

    # try to get the user from db if not there, authenticate
    # self.graph_api.get_object('/me/friends')['data']





    # ---------------------------------------------------------------------------
