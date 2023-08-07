from kfsd.apps.core.utils.dict import DictUtils


class BaseUser:
    def __init__(self):
        self.__userInfo = {}

    def setUserInfo(self, userInfo):
        self.__userInfo = userInfo

    def getUserInfo(self):
        return self.__userInfo

    def is_authenticated(self):
        return DictUtils.get(self.__userInfo, "verified")
