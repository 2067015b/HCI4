import urllib2


class LightSensor(object):
    """
    Takes a URL like
        http://pi3a.local:8666/light-sensor/0
    or
        http://localhost:8666/light-sensor/0

    Where the 0 is an index of a sensor on a corresponding Arduino connected to a Pi
    """

    def __init__(self, url):
        self.url = url

    def isOn(self):
        content = urllib2.urlopen(self.url).read()
        return self.__str2bool(content)

    @staticmethod
    def __str2bool(v):
        return v.lower() in ("yes", "true", "t", "1", "on")



