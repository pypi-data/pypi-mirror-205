
class BaseUser:
    def __init__(self):
        self.__userInfo = {}

    def setUserInfo(self, userInfo):
        self.__userInfo = userInfo

    def getUserInfo(self):
        return self.__userInfo

    def is_authenticated(self):
        if not self.__userInfo:
            return False
        return True
