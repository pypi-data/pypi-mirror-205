from kfsd.apps.core.utils.http.cookie import Cookie
from kfsd.apps.core.utils.http.config import Config


class Request(Cookie, Config):
    def __init__(self, request=None):
        self.__request = request
        Cookie.__init__(self, request)
        Config.__init__(self, request)

    def getRequest(self):
        return self.__request

    def setRequest(self, request):
        self.__request = request
