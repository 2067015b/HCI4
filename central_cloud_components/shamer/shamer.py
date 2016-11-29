from .. import FBPoster
from .. import BulbStates

class Shamer(object):

    def __init__(self,fb_user_token, shaming_rate = 0.8):
        self.token = fb_user_token
        self.FBPoster = FBPoster(fb_user_token)
        self.TwitterPoster = None
        self.shaming_rate = shaming_rate
        self.format_types = {BulbStates.IN_BED: "%s went to sleep for %s and forgot to switch my %s lights off.",
               BulbStates.NOT_HOME: "%s left my home for %s and didn't switch my %s lights off.",
               BulbStates.NOT_AROUND: "%s left my %s lights on for %s while I wasn't around."
               }

    def shame_user(self, data = {}, days = 1):
        ''' Decides on what to post, possibly aggregates several posts into one.'''
        bulbs = data.keys()
        bulbs_to_shame = {}
        for bulb in bulbs:
            reason, period = self.get_worst_state(data[bulb])
            if (period/data[bulb][BulbStates.NOT_WASTED]>(1-self.shaming_rate)) or \
                (period > (days*4*60)):
                bulbs_to_shame[bulb] = {'reason':reason,'period':period }
        message = self.format_post(bulbs_to_shame, days)
        if message:
            return self.FBPoster.post(message)
        return



    def format_post(self, bulbs_to_shame, days = 1):
        ''' Formats the post given the reason(s) provided. '''
        time_window = [" And I", " I also"]
        if (days == 1):
            time_window.append("Yesterday I")
        elif (days == 7):
            time_window.append("Last week I")
        else:
            time_window.append("In the last %d days I" % days)

        bulbs = bulbs_to_shame.keys()

        if (len(bulbs)==0):
            return ""
        elif (len(bulbs)==1):
            reason = bulbs_to_shame[bulbs[0]]['reason']
            period = bulbs_to_shame[bulbs[0]]['period']
            if reason==BulbStates.NOT_AROUND:
                message = self.format_types[reason] % (time_window.pop(), bulbs[0].lower(), self.get_formatted_time(period))
            else:
                message = self.format_types[reason] % (time_window.pop(), self.get_formatted_time(period),bulbs[0].lower())
        else:
            wasted_asleep = ["",0]
            wasted_not_home = ["",0]
            wasted_not_around = ["",0]
            for bulb in bulbs:
                if bulbs_to_shame[bulb]['reason'] == BulbStates.NOT_AROUND :
                    wasted_not_around[0]+= str(bulb).lower() + " and "
                    wasted_not_around[1] += bulbs_to_shame[bulb]['period']

                elif bulbs_to_shame[bulb]['reason'] == BulbStates.NOT_HOME:
                    wasted_not_home[0]+= str(bulb).lower() + " and "
                    wasted_not_home[1] += bulbs_to_shame[bulb]['period']

                elif bulbs_to_shame[bulb]['reason'] == BulbStates.IN_BED :
                    wasted_asleep[0]+= str(bulb).lower() + " and "
                    wasted_asleep[1] += bulbs_to_shame[bulb]['period']

            message = ""
            if wasted_asleep[0]:
                message += self.format_types[BulbStates.IN_BED]  \
                           %(time_window.pop(), self.get_formatted_time(wasted_asleep[1]), wasted_asleep[0][:-5])
            if wasted_not_home[0]:
                message += self.format_types[BulbStates.NOT_HOME]  \
                           %(time_window.pop(), self.get_formatted_time(wasted_not_home[1]), wasted_not_home[0][:-5])
            if wasted_not_around[0]:
                message += self.format_types[BulbStates.NOT_AROUND]  \
                           %(time_window.pop(), wasted_not_around[0][:-5], self.get_formatted_time(wasted_not_around[1]))

        return message

    def get_formatted_time(self, minutes):
        if int(minutes / 60) == 1:
            time = '%d hour and %d minutes' % (minutes / 60, (minutes % 60))
        elif int(minutes /60) > 1:
            time = '%d hours and %d minutes' % (minutes / 60, (minutes % 60))
        else:
            time = '%d minutes' % minutes
        return time

    def get_worst_state(self, bulb_tuple):
        '''Returns the state and the value that should be shamed the most.'''
        if (bulb_tuple[BulbStates.NOT_AROUND] >= bulb_tuple[BulbStates.NOT_HOME]) and \
                (bulb_tuple[BulbStates.NOT_AROUND] >= bulb_tuple[BulbStates.IN_BED]):
            return BulbStates.NOT_AROUND, bulb_tuple[BulbStates.NOT_AROUND]

        elif (bulb_tuple[BulbStates.NOT_HOME] >= bulb_tuple[BulbStates.NOT_AROUND]) and \
                (bulb_tuple[BulbStates.NOT_HOME] >= bulb_tuple[BulbStates.IN_BED]):
            return BulbStates.NOT_HOME, bulb_tuple[BulbStates.NOT_HOME]

        elif (bulb_tuple[BulbStates.IN_BED] >= bulb_tuple[BulbStates.NOT_AROUND]) and \
                (bulb_tuple.IN_BED >= bulb_tuple[BulbStates.NOT_HOME]):
            return BulbStates.IN_BED, bulb_tuple[BulbStates.IN_BED]
