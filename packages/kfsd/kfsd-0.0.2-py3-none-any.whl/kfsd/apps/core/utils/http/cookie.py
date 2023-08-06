import http.cookies

from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.exceptions.exec import ExecException


class Cookie:
    KEY = 'key'
    COOKIE = 'cookie'
    EXPIRY_IN_MINS = 'expiry_in_mins'
    SECURE = 'secure'
    HTTP_ONLY = 'http_only'
    SAME_SITE = 'same_site'

    def __init__(self, httpObj):
        self.__httpObj = httpObj

    def getHttpObj(self):
        return self.__httpObj

    def setHttpObj(self, httpObj):
        self.__httpObj = httpObj

    def getAllCookies(self):
        return self.__httpObj.COOKIES

    def getCookie(self, key):
        return self.__httpObj.COOKIES.get(key)

    def setCookie(self, unset=False, **kwargs):
        if not unset:
            requiredKeys = [self.KEY, self.COOKIE, self.EXPIRY_IN_MINS, self.SECURE, self.HTTP_ONLY, self.SAME_SITE]
            if not DictUtils.key_exists_multi(kwargs, requiredKeys):
                raise ExecException("Required cookie settings keys does not exist, keys: {}".format(requiredKeys))

            self.getHttpObj().set_cookie(
                key=kwargs[self.KEY],
                value=kwargs[self.COOKIE],
                expires=kwargs[self.EXPIRY_IN_MINS]*60,
                secure=kwargs[self.SECURE],
                httponly=kwargs[self.HTTP_ONLY],
                samesite=kwargs[self.SAME_SITE]
            )
        else:
            self.getHttpObj().delete_cookie(
                key=kwargs[self.KEY]
            )

    def cookieToHeaderStr(self, rmCookieKeys=[]):
        cookie_string = ''
        if self.getAllCookies():
            cookie = http.cookies.SimpleCookie()
            filteredCookies = DictUtils.filter_by_keys_neg(self.getAllCookies(), rmCookieKeys)
            cookie.update(filteredCookies)
            for key, value in cookie.items():
                cookie_string += f'{key}={value}; '
            # remove the trailing '; '
            cookie_string = cookie_string[:-2]
        return cookie_string
