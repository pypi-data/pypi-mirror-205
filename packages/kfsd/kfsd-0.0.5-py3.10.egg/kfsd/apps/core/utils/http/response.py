import requests
from rest_framework import status

from kfsd.apps.core.exceptions.api import KubefacetsAPIException


class Response():
    def __init__(self, response):
        self.__response = response

    def getResponse(self):
        return self.__response

    def setResponse(self, response):
        self.__response = response

    def getStatusCode(self):
        return self.getResponse().status_code

    def isRespValid(self, expStatusCode):
        if isinstance(expStatusCode, int) and not expStatusCode == self.getStatusCode():
            raise KubefacetsAPIException(
                self.getResponse().json()["detail"], self.getResponse().json()["code"], self.getStatusCode()
            )

        if isinstance(expStatusCode, list) and self.getStatusCode() not in expStatusCode:
            raise KubefacetsAPIException(
                self.getResponse().json()["detail"], self.getResponse().json()["code"], self.getStatusCode()
            )

        return True

    def request(self, method, url, expStatus, **kwargs):
        try:
            resp = method(url, **kwargs)
            if self.isRespValid(expStatus, resp.status_code, resp):
                return resp
        except requests.exceptions.Timeout:
            raise KubefacetsAPIException(
                "The server took too long to respond to your request. Please try again later.",
                "server_timed_out",
                status.HTTP_408_REQUEST_TIMEOUT
            )
        except requests.exceptions.ConnectionError:
            raise KubefacetsAPIException(
                "Service temporarily unavailable. Please try again later.",
                "service_unavailable",
                status.HTTP_503_SERVICE_UNAVAILABLE
            )

    def post(self, url, expStatus, **kwargs):
        return self.request(requests.post, url, expStatus, **kwargs)

    def get(self, url, expStatus, **kwargs):
        return self.request(requests.get, url, expStatus, **kwargs)

    def delete(self, url, expStatus, **kwargs):
        return self.request(requests.delete, url, expStatus, **kwargs)
