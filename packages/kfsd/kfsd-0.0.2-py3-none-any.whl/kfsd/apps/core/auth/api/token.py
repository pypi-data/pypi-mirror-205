from kfsd.apps.core.auth.api.gateway import APIGateway


class TokenAuth(APIGateway):
    def __init__(self, request=None, response=None):
        APIGateway.__init__(self, request, response)

    def getTokenUserInfo(self):
        pass
        # uri = self.findConfigs(["gateway.auth.token.verify_token"])[0]
        # headers = {
        #     'Content-Type': 'application/json',
        #     'X-CSRFToken': self.getCookie('csrftoken'),
        #     'Cookie': self.cookieToHeaderStr(),
        #     'X-APIKey': self.getApplicationAPIKey()
        # }
        # self.post(uri, HTTPStatus.OK, headers=headers)
