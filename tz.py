from datetime import datetime, tzinfo,timedelta

class UTC(tzinfo):
    def __init__(self,offset = 0):
        self._offset = offset

    def utcoffset(self,dt):
        return timedelta(hours=self._offset)

    def tzname(self,dt):
        return "UTC +%s" % self._offset

    def dst(self,dt):
       return timedelta(hours=self._offset)