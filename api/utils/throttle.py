from rest_framework.throttling import SimpleRateThrottle


class VisitThrottle(SimpleRateThrottle):
    scope = "Luffy"

    def get_cache_key(self, request, view):
        return self.get_ident(request)


class UserThrottle(SimpleRateThrottle):
    scope = "LuffyUser"

    def get_cache_key(self, request, view):
        return request.user.username

"""
from rest_framework.throttling import BaseThrottle
import time
VISIT_RECORD = {}

class VisitThrottle(BaseThrottle):

    def __init__(self):
        self.history = None

    def allow_request(self, request, view):
        # remote_addr = request._request.META.get('REMOTE_ADDR')
        # remote_addr = request.META.get('REMOTE_ADDR')
        remote_addr = self.get_ident(request) ## same as the two above but use parent get identity function
        ctime = time.time()
        if remote_addr not in VISIT_RECORD:
            VISIT_RECORD[remote_addr] = [ctime,]
            return True

        history = VISIT_RECORD.get(remote_addr)
        self.history = history

        while history and history[-1] < ctime - 60:  ## only 3 visits per 10 seconds allowed
            history.pop()

        if len(history) < 3:
            history.insert(0, ctime)
            return True
        # return True # return false meaning visit freqency too high, being limited 
        # return True

    def wait(self):
        ctime = time.time()
        return 60 - (ctime - self.history[-1])
"""