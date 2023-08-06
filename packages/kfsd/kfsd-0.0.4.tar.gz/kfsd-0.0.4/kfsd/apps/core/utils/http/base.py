from kfsd.apps.core.utils.http.request import Request
from kfsd.apps.core.utils.http.response import Response


class HTTP(Request, Response):
    def __init__(self, request=None, response=None):
        Request.__init__(self, request)
        Response.__init__(self, response)

    def formatUrl(self, args):
        return "/".join(args)
