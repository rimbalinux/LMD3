#from django.utils.thread_support import currentThread 
from django.utils._threading_local import currentThread
_requests = {}

def get_request():
    return _requests[currentThread()]

class GlobalRequestMiddleware(object):
    def process_request(self, request):
        _requests[currentThread()] = request

