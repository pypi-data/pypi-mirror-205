from kfsd.apps.core.auth.base import BaseUser
from kfsd.apps.core.auth.api.token import TokenAuth


class TokenUser(BaseUser, TokenAuth):
    def __init__(self, request):
        TokenAuth.__init__(self, request)
        self.setUserInfo(self.getTokenUserInfo())
