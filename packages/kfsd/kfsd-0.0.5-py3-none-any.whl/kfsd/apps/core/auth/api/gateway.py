from kfsd.apps.core.utils.http.base import HTTP


class APIGateway(HTTP):
    def __init__(self, request=None, response=None):
        HTTP.__init__(self, request, response)

    def getApplicationAPIKey(self):
        return self.findConfigs(["gateway.api_key"])[0]

    def post(self, uri, expStatus, **kwargs):
        gatewayHost = self.findConfigs(["gateway.host"])[0]
        url = gatewayHost + uri
        super().post(url, expStatus, **kwargs)
