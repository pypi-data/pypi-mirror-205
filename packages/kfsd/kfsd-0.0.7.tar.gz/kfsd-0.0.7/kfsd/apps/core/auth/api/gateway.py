from kfsd.apps.core.utils.http.base import HTTP
from kfsd.apps.core.utils.http.django.request import DjangoRequest


class APIGateway(HTTP):
    def __init__(self, request=None):
        self.__request = DjangoRequest(request)
        HTTP.__init__(self)

    def getApplicationAPIKey(self):
        return self.__request.findConfigs(["gateway.api_key"])[0]

    def getGatewayHost(self):
        return self.__request.findConfigs(["gateway.host"])[0]

    def getDjangoRequest(self):
        return self.__request

    def constructUrl(self, uri):
        return self.getGatewayHost() + uri
