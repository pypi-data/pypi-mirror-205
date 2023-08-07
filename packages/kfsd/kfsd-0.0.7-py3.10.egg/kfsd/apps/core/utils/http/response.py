from kfsd.apps.core.exceptions.api import KubefacetsAPIException
from kfsd.apps.core.utils.http.headers.cookie import Cookie


class Response(Cookie):
    def __init__(self):
        self.__response = None

    def getResponse(self):
        return self.__response

    def setResponse(self, response):
        self.__response = response
        self.setCookiesHttpObj(response)

    def getStatusCode(self):
        return self.__response.status_code

    def isRespValid(self, expStatusCode):
        if isinstance(expStatusCode, int) and not expStatusCode == self.getStatusCode():
            raise KubefacetsAPIException(
                self.getResponse().json()["detail"],
                self.getResponse().json()["code"],
                self.getStatusCode(),
            )

        if (
            isinstance(expStatusCode, list)
            and self.getStatusCode() not in expStatusCode
        ):
            raise KubefacetsAPIException(
                self.getResponse().json()["detail"],
                self.getResponse().json()["code"],
                self.getStatusCode(),
            )

        return True
