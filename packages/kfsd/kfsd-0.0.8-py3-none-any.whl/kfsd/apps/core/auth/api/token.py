from http import HTTPStatus
from kfsd.apps.core.utils.http.headers.contenttype import ContentType
from kfsd.apps.core.auth.api.gateway import APIGateway
from kfsd.apps.core.utils.http.headers.base import Headers


class TokenAuth(Headers, APIGateway):
    def __init__(self, request=None):
        Headers.__init__(self)
        APIGateway.__init__(self, request)

    def setAPIGatewayHeaders(self):
        self.setCSRF(
            self.getDjangoRequest().getDjangoReqCookies().getCookie("csrftoken")
        )
        self.setAPIKey(self.getApplicationAPIKey())
        self.setContentType(ContentType.APPLICATION_JSON)

    def getTokenUserInfo(self):
        verifyTokenUri = self.getDjangoRequest().findConfigs(
            ["gateway.auth.token.verify_token"]
        )[0]
        verifyTokenCompleteUrl = self.constructUrl(verifyTokenUri)
        self.setAPIGatewayHeaders()
        self.post(
            verifyTokenCompleteUrl,
            HTTPStatus.OK,
            json={
                "cookies": self.getDjangoRequest().getDjangoReqCookies().getAllCookies()
            },
            headers=self.getReqHeaders(),
        )
        return self.getResponse().json()
